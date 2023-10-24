<template>
  <section class="component-wrapper">
    transcriptionIsLoading: {{ transcriptionIsLoading }}
    <FileRecorder></FileRecorder>
    <FileUploader
      :transcription-is-loading="transcriptionIsLoading"
      :transcription-error="transcriptionError"
      :upload-progress="uploadProgress"
      :error-message="errorMessage"
      @start-upload="customUploaderXHR"
    ></FileUploader>

    <Accordion :activeIndex="0">
      <AccordionTab header="Transkribierter Text">
        <Textarea
          :disabled="transcriptionIsLoading || transcription.length < 1 || transcriptionError"
          v-model="transcription"
          autoResize
          rows="1"
        />
      </AccordionTab>
    </Accordion>

    <button @click="abortUpload()">Abort</button>
  </section>
</template>

<script setup lang="ts">
import { getHumanFileSize } from '@/composables/util';
import { ref } from 'vue';
import FileUploader from './FileUploader.vue';
import { StateFlag } from '@/model/interfaces';
import FileRecorder from './FileRecorder.vue';

// state
const transcriptionError = ref(false);
const transcriptionIsLoading = ref(false);
const errorMessage = ref('');

// data
const fileName = ref('');
const fileSize = ref();
const uploadProgress = ref(0);
const transcription = ref('');
const apiUrl = 'http://localhost:8000/api/transcribe/file';
let activeXHR: XMLHttpRequest | null = null;

function abortUpload() {
  if (activeXHR) {
    activeXHR.abort();
    console.log('Upload aborted');
    activeXHR = null;
  }
}

function customUploaderXHR(files: File[]) {
  console.log('Starting file upload');
  // Set file state
  const file = files[0];
  if (!file) {
    setState(StateFlag.ERROR, 'Die Datei konnte nicht gefunden werden');
    console.log('No file provided for upload.');
    return;
  }
  setState(StateFlag.INITIAL);

  fileName.value = file.name;
  uploadProgress.value = 0;
  fileSize.value = getHumanFileSize(file.size);
  transcription.value = '';

  // Create form data and open xhr request
  const data = new FormData();
  data.append('file', file);
  activeXHR = new XMLHttpRequest();

  // Event listener for progress
  activeXHR.upload.onprogress = function (e) {
    if (e.lengthComputable) {
      const percentComplete = (e.loaded / e.total) * 100;
      uploadProgress.value = Math.round(percentComplete);
      console.log(`Upload progress: ${percentComplete}%`);
    }
  };

  // Event listener for the server side streaming response
  let lastReadPosition = 0;
  activeXHR.onreadystatechange = function () {
    if (this.readyState === XMLHttpRequest.LOADING) {
      const newText = this.responseText.substring(lastReadPosition);
      if (this.status !== 200) {
        // Response not good, set error state
        const detail = JSON.parse(newText).detail;
        if (detail) {
          setState(StateFlag.ERROR, `${detail}`);
        } else {
          setState(
            StateFlag.ERROR,
            `Bei der Anfrage ist ein Fehler aufgetreten. HTTP-Code ${this.status}: ${this.statusText}`
          );
        }
      }
      // Response good, get data chunk by chunk
      else {
        console.log(`New stream chunk received [${this.status}]: ${newText}`);
        transcription.value = transcription.value + ' ' + newText;
        lastReadPosition = this.responseText.length;
      }
    }
    if (this.readyState === XMLHttpRequest.DONE) {
      transcriptionIsLoading.value = false;
      console.log('Request finished');
    }
  };

  // Event listener for errors during the request
  activeXHR.onerror = function () {
    setState(
      StateFlag.ERROR,
      `Bei der Anfrage ist ein Fehler aufgetreten. HTTP-Code ${this.status}: ${this.statusText}`
    );
    console.error('XHR error.');
  };

  activeXHR.open('POST', apiUrl, true);
  activeXHR.send(data);
}

function setState(state: StateFlag, error: string = '') {
  switch (state) {
    case StateFlag.ERROR:
      transcriptionIsLoading.value = false;
      transcriptionError.value = true;
      errorMessage.value = error;

      fileName.value = '';
      fileSize.value = 0;
      uploadProgress.value = 0;
      transcription.value = '';
      break;
    case StateFlag.INITIAL:
      transcriptionIsLoading.value = true;
      transcriptionError.value = false;
      errorMessage.value = '';

      fileName.value = '';
      fileSize.value = 0;
      uploadProgress.value = 0;
      transcription.value = '';
      break;
    case StateFlag.SUCCESS:
      transcriptionIsLoading.value = false;
      transcriptionError.value = false;
      errorMessage.value = '';
      break;
  }
}
</script>

<style scoped>
.component-wrapper {
  width: 80%;
  display: flex;
  gap: 1rem;
  flex-direction: column;
}

.p-inputtextarea {
  width: 100%;
}
</style>
