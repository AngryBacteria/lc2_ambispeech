<template>
  <section class="component-wrapper">
    <section class="upload-wrapper">
      <ProgressBar v-if="!error" :value="uploadProgress"></ProgressBar>
      <ProgressBar v-else style="background-color: var(--danger)"></ProgressBar>
      <div class="file-wrapper">
        <FileUpload
          mode="basic"
          name="file"
          url="http://localhost:8000/uploadfile"
          :auto="true"
          accept="audio/wav"
          chooseLabel="Hochladen"
          customUpload
          @uploader="customUploaderXHR($event)"
        />
        <p v-if="error" style="color: var(--danger)">{{ error }}</p>
        <p v-else-if="fileSize && fileName">{{ fileName }} ({{ fileSize }})</p>
      </div>
    </section>
    <Accordion :activeIndex="0">
      <AccordionTab header="Transkribierter Text">
        <Textarea
          :disabled="requestIsLoading || transcription.length < 1"
          v-model="transcription"
          autoResize
          rows="1"
        />
      </AccordionTab>
    </Accordion>
  </section>
</template>

<script setup lang="ts">
import type { FileUploadUploaderEvent } from 'primevue/fileupload';
import { ref } from 'vue';

const fileName = ref('');
const fileSize = ref();
const uploadProgress = ref(0);
const requestIsLoading = ref(false);
const error = ref<string | boolean>(false);
const transcription = ref('');

function customUploaderXHR(event: FileUploadUploaderEvent) {
  // Set file state
  const file = (event.files as File[])[0];
  if (!file) {
    throw new Error('No file provided for upload.');
  }
  requestIsLoading.value = true;
  error.value = false;
  fileName.value = file.name;
  uploadProgress.value = 0;
  fileSize.value = humanFileSize(file.size);
  transcription.value = '';

  // Create form data and open xhr request
  const data = new FormData();
  data.append('file', file);
  const xhr = new XMLHttpRequest();

  // Event listener for progress
  xhr.upload.onprogress = function (e) {
    if (e.lengthComputable) {
      const percentComplete = (e.loaded / e.total) * 100;
      uploadProgress.value = Math.round(percentComplete);
      console.log(`Upload progress: ${percentComplete}%`);
    }
  };

  // Event listener for the server side streaming response
  let lastReadPosition = 0;
  xhr.onreadystatechange = function () {
    if (xhr.readyState === XMLHttpRequest.LOADING) {
      const newText = xhr.responseText.substring(lastReadPosition);
      console.log('New chunk received:', newText);
      transcription.value = transcription.value + ' ' + newText;
      lastReadPosition = xhr.responseText.length;
    }
    if (xhr.readyState === XMLHttpRequest.DONE) {
      console.log('Request finished');
      requestIsLoading.value = false;
    }
  };

  // Event listener for errors during the request
  xhr.onerror = function () {
    console.error('XHR error.');
    requestIsLoading.value = false;
    error.value = `XHR error. Status: ${this.status} Status text: ${this.statusText}`;
  };

  xhr.open('POST', 'http://localhost:8000/uploadfile', true);
  xhr.send(data);
}

/**
 * Format bytes as human-readable text.
 *
 * @param bytes Number of bytes.
 * @param si True to use metric (SI) units, aka powers of 1000. False to use
 *           binary (IEC), aka powers of 1024.
 * @param dp Number of decimal places to display.
 *
 * @return Formatted string.
 */
function humanFileSize(bytes: number, si = false, dp = 1) {
  const thresh = si ? 1000 : 1024;

  if (Math.abs(bytes) < thresh) {
    return bytes + ' B';
  }

  const units = si
    ? ['kB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']
    : ['KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB'];
  let u = -1;
  const r = 10 ** dp;

  do {
    bytes /= thresh;
    ++u;
  } while (Math.round(Math.abs(bytes) * r) / r >= thresh && u < units.length - 1);

  return bytes.toFixed(dp) + ' ' + units[u];
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
