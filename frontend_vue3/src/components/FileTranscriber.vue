<template>
  <section class="upload-wrapper">
    <ProgressBar :value="uploadProgress"></ProgressBar>
    <div class="file-wrapper">
      <FileUpload
        mode="basic"
        name="file"
        url="http://localhost:8000/uploadfile"
        :auto="true"
        chooseLabel="Hochladen"
        customUpload
        @uploader="customUploaderXHR($event)"
      />
      <p v-if="fileSize && fileName">{{ fileName }} ({{ fileSize }})</p>
    </div>
  </section>
</template>

<script setup lang="ts">
import type { FileUploadUploaderEvent } from 'primevue/fileupload'
import { ref } from 'vue'

const fileName = ref('')
const fileSize = ref()
const uploadProgress = ref(0)

function customUploaderXHR(event: FileUploadUploaderEvent) {
  // Set file state
  const file = (event.files as File[])[0]
  fileName.value = file.name
  uploadProgress.value = 0
  fileSize.value = humanFileSize(file.size)

  // Create form data and open xhr request
  const data = new FormData()
  data.append('file', file)
  const xhr = new XMLHttpRequest()

  // Event listener for progress
  xhr.upload.onprogress = function (e) {
    if (e.lengthComputable) {
      const percentComplete = (e.loaded / e.total) * 100
      uploadProgress.value = Math.round(percentComplete)
      console.log(`Upload progress: ${percentComplete}%`)
    }
  }

  // Event listener for the server side streaming response
  let lastReadPosition = 0
  xhr.onreadystatechange = function () {
    if (xhr.readyState === XMLHttpRequest.LOADING) {
      const newText = xhr.responseText.substring(lastReadPosition)
      console.log('New chunk received:', newText)
      lastReadPosition = xhr.responseText.length
    }
    if (xhr.readyState === XMLHttpRequest.DONE) {
      console.log('Streaming done')
    }
  }

  // Event listener for errors during the request
  xhr.onerror = function () {
    console.error('XHR error.')
  }

  xhr.open('POST', 'http://localhost:8000/uploadfile', true)
  xhr.send(data)
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
  const thresh = si ? 1000 : 1024

  if (Math.abs(bytes) < thresh) {
    return bytes + ' B'
  }

  const units = si
    ? ['kB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']
    : ['KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB']
  let u = -1
  const r = 10 ** dp

  do {
    bytes /= thresh
    ++u
  } while (Math.round(Math.abs(bytes) * r) / r >= thresh && u < units.length - 1)

  return bytes.toFixed(dp) + ' ' + units[u]
}
</script>

<style>
.upload-wrapper {
  border-radius: 6px;
  min-width: 80%;
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
</style>
