<template>
  <section class="component-wrapper">
    <FileUploader
      v-model:transcriptionError="transcriptionError"
      :transcription-is-loading="store.transcriptionIsLoading"
      :upload-progress="uploadProgress"
      @start-upload="customUploaderXHR"
      v-if="$route.params.type == 'upload'"
    />

    <FileRecorder
      v-model:transcriptionError="transcriptionError"
      :transcription-is-loading="store.transcriptionIsLoading"
      :upload-progress="uploadProgress"
      @start-upload="customUploaderXHR"
      v-else
    />

    <Accordion v-model:activeIndex="activeTab">
      <AccordionTab>
        <template #header>
          <section style="display: flex; align-items: center; width: 100%">
            <div>Transkribierter Text</div>
            <Button
              @click="
                $event.stopPropagation();
                abortUpload();
              "
              :label="store.isMobile ? '' : 'Abbrechen'"
              severity="warning"
              icon="pi pi-stop "
              size="small"
              :class="{ hidden: !store.transcriptionIsLoading }"
              style="margin-left: auto"
            />
          </section>
        </template>
        <Textarea
          :disabled="
            !store.isDebug &&
            (store.transcriptionIsLoading ||
              store.transcriptionText.length < 1 ||
              transcriptionError.length > 0)
          "
          v-model="store.transcriptionText"
          style="max-width: 100%; width: 100%"
          rows="6"
        />
      </AccordionTab>
    </Accordion>
  </section>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import FileUploader from '@/components/s2t/FileUploader.vue';
import FileRecorder from '@/components/s2t/FileRecorder.vue';
import { useUserStore } from '@/stores/user';
import { StorageSerializers, useSessionStorage } from '@vueuse/core';
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
const activeTab = useSessionStorage('activeTabFileTranscriber', null, {
  serializer: StorageSerializers.number
});

// data
const uploadProgress = ref(0);
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

  activeXHR.onload = function () {
    if (activeXHR?.status == 200) {
      setState(StateFlag.SUCCESS);
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
        store.transcriptionText = store.transcriptionText + newText;
        lastReadPosition = this.responseText.length;
      }
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
      store.transcriptionIsLoading = false;
      transcriptionError.value = error;
      uploadProgress.value = 0;
      store.transcriptionText = '';
      break;
    case StateFlag.INITIAL:
      store.extractedInfoText = '';
      store.extractedInfoObject = null;
      store.analysisIsLoading = false;
      store.transcriptionIsLoading = true;
      transcriptionError.value = '';
      uploadProgress.value = 0;
      store.transcriptionText = '';
      break;
    case StateFlag.SUCCESS:
      store.transcriptionIsLoading = false;
      transcriptionError.value = '';

      store.transcriptionText = store.transcriptionText.trim();
      console.log('Request finished');
      break;
    case StateFlag.ABORTED:
      store.transcriptionIsLoading = false;
      transcriptionError.value = '';
      uploadProgress.value = 0;
      store.transcriptionText = '';
      break;
  }
}
</script>

<style scoped>
.p-inputtextarea {
  width: 100%;
}
</style>
