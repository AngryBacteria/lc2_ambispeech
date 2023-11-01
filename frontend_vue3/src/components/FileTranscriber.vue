<template>
  <section class="component-wrapper">
    <FileUploader
      v-model:transcriptionError="transcriptionError"
      :transcription-is-loading="transcriptionIsLoading"
      :upload-progress="uploadProgress"
      @start-upload="customUploaderXHR"
      v-if="$route.params.type == 'upload'"
    />

    <FileRecorder
      v-model:transcriptionError="transcriptionError"
      :transcription-is-loading="transcriptionIsLoading"
      :upload-progress="uploadProgress"
      @start-upload="customUploaderXHR"
      v-else
    />

    <Accordion :activeIndex="0">
      <AccordionTab>
        <template #header>
          <span>Transkribierter Text</span>
        </template>
        <Textarea
          :disabled="
            transcriptionIsLoading || transcription.length < 1 || transcriptionError.length > 0
          "
          v-model="transcription"
          autoResize
          rows="1"
        />
      </AccordionTab>
    </Accordion>

    <div class="action-row">
      <Button @click="abortUpload()" v-show="transcriptionIsLoading" severity="warning"
        >Transkription stoppen</Button
      >
      <Button v-show="!transcriptionIsLoading && transcription.length > 0" severity="success"
        >Analyse starten</Button
      >
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import FileUploader from './FileUploader.vue';
import FileRecorder from './FileRecorder.vue';
import { useUserStore } from '@/stores/user';
/**
 * This component transcribes the contents of an audio file with the backend.
 * It receives audio data, uploads it to the backend and retrieves the transcribed text
 */

enum StateFlag {
  INITIAL,
  ERROR,
  SUCCESS,
  ABORTED
}

// dependencies
const store = useUserStore();

// state
const transcriptionError = ref('');
const transcriptionIsLoading = ref(false);

// data
const uploadProgress = ref(0);
const transcription = ref('');
let activeXHR: XMLHttpRequest | null = null;

function abortUpload() {
  if (activeXHR) {
    activeXHR.abort();
    console.log('Upload aborted');
    activeXHR = null;
    setState(StateFlag.ABORTED);
  }
}

/**
 * Uploads files to the backend and tracks various state
 * @param files One or more files
 */
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
        transcription.value = transcription.value + newText;
        lastReadPosition = this.responseText.length;
      }
    }
    if (this.readyState === XMLHttpRequest.DONE) {
      transcription.value = transcription.value.trim();
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

  let service = store.useCloudS2T ? 'azure' : 'whisper';
  console.log(`Starting a speech to text request with ${service}`);
  activeXHR.open(
    'POST',
    `http://localhost:8000/api/transcribe/file/${service}?diarization=${store.useDiarization}&language=${store.transcriptionLanguage}`,
    true
  );
  activeXHR.send(data);
}

/**
 * Helper function to better manage state
 * @param state The state to switch to
 * @param error The optional error message to set
 */
function setState(state: StateFlag, error: string = '') {
  switch (state) {
    case StateFlag.ERROR:
      transcriptionIsLoading.value = false;
      transcriptionError.value = error;

      uploadProgress.value = 0;
      transcription.value = '';
      break;
    case StateFlag.INITIAL:
      transcriptionIsLoading.value = true;
      transcriptionError.value = '';

      uploadProgress.value = 0;
      transcription.value = '';
      break;
    case StateFlag.SUCCESS:
      transcriptionIsLoading.value = false;
      transcriptionError.value = '';
      break;
    case StateFlag.ABORTED:
      transcriptionIsLoading.value = false;
      transcriptionError.value = '';
      uploadProgress.value = 0;
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
