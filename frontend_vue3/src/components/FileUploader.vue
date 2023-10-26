<template>
  <section class="upload-wrapper">
    <ProgressBar v-if="!transcriptionError" :value="uploadProgress"></ProgressBar>
    <ProgressBar v-else style="background-color: var(--danger)"></ProgressBar>
    <div class="file-wrapper">
      <FileUpload
        :disabled="transcriptionIsLoading"
        mode="basic"
        name="file"
        url="http://localhost:8000/uploadfile"
        :auto="true"
        accept="audio/*"
        chooseLabel="Hochladen"
        customUpload
        @uploader="handleUpload($event.files as File[])"
      />
      <p v-if="transcriptionError" style="color: var(--danger)">{{ transcriptionError }}</p>
      <p v-else-if="fileSize && fileName">{{ fileName }} ({{ fileSize }})</p>
    </div>
  </section>
</template>

<script setup lang="ts">
import { getHumanFileSize } from '@/composables/util';
import { type FileTranscriptionProps } from '@/model/interfaces';
import { ref } from 'vue';
/**
 * With this component a user can upload a file to the web-application.
 * This file can then be passed to the transcriber component, that uploads it to the backend
 */

const emit = defineEmits(['startUpload']);
defineProps<FileTranscriptionProps>();
const transcriptionError = defineModel<string>('transcriptionError', {
  required: true
});

const fileName = ref('');
const fileSize = ref('');

function handleUpload(files: File[]) {
  // Reset state
  fileName.value = '';
  fileSize.value = '';

  const file = files[0];
  console.log('Got File from user: ', file);
  if (!file) {
    transcriptionError.value = 'Die Datei konnte nicht gefunden werden';
    console.log('no file error');
    return;
  }
  fileName.value = file.name;
  fileSize.value = getHumanFileSize(file.size);

  emit('startUpload', files);
}
</script>

<style scoped>
.upload-wrapper {
  border-radius: var(--custom-border-radius);
  display: flex;
  flex-direction: column;
  background-color: var(--surface-card);
  border: 1px solid var(--surface-border);
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

:deep(.p-progressbar-label) {
  display: none;
}
</style>
