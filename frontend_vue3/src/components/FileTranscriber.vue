<template>
  <section class="component-wrapper">
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

const transcriptionError = ref(false);
const transcriptionIsLoading = ref(false);

// set state
const fileName = ref('');
const fileSize = ref();
const uploadProgress = ref(0);
const transcription = ref('');
const errorMessage = ref('');
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
    //TODO: handle correctly
    console.log('No file provided for upload.');
    return;
  }
  transcriptionIsLoading.value = true;
  transcriptionError.value = false;
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

  //TODO: handle if response from server is an error
  // Event listener for the server side streaming response
  let lastReadPosition = 0;
  activeXHR.onreadystatechange = function () {
    if (this.readyState === XMLHttpRequest.LOADING) {
      const newText = this.responseText.substring(lastReadPosition);
      if (this.status !== 200) {
        // Response not good, set error state
        transcriptionIsLoading.value = false;
        transcriptionError.value = true;
        const detail = JSON.parse(newText).detail;
        if (detail) {
          errorMessage.value = `${detail}`;
        } else {
          errorMessage.value = `Bei der Anfrage ist ein Fehler aufgetreten. HTTP-Code ${this.status}: ${this.statusText}`;
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
      console.log('Request finished');
      transcriptionIsLoading.value = false;
    }
  };

  // Event listener for errors during the request
  activeXHR.onerror = function () {
    console.error('XHR error.');
    transcriptionIsLoading.value = false;
    transcriptionError.value = true;
    errorMessage.value = `Bei der Anfrage ist ein Fehler aufgetreten. HTTP-Code ${this.status}: ${this.statusText}`;
  };

  activeXHR.open('POST', apiUrl, true);
  activeXHR.send(data);
}
</script>

<style>
.component-wrapper {
  width: 80%;
  display: flex;
  gap: 1rem;
  flex-direction: column;
}

.upload-wrapper {
  border-radius: 6px;
  display: flex;
  flex-direction: column;
  background-color: var(--surface-card);
}

.file-wrapper {
  padding: 1rem;
  display: flex;
  flex-direction: row;
  gap: 1rem;
  align-items: center;
}

.file-wrapper p {
  word-break: break-all;
}

.p-progressbar-determinate .p-progressbar-value-animate {
  transition: width 0.1s ease-in-out;
}

.p-progressbar {
  border-bottom-left-radius: 0;
  border-bottom-right-radius: 0;
  height: 8px;
}

.p-progressbar-label {
  display: none;
}

.p-inputtextarea {
  width: 100%;
}
</style>
