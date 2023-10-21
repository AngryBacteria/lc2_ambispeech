<template>
  <section class="upload-wrapper">
    <ProgressBar v-if="!transcriptionError" :value="uploadProgress"></ProgressBar>
    <ProgressBar v-else style="background-color: var(--danger)"></ProgressBar>
    <div class="file-wrapper">
      <FileUpload
        mode="basic"
        name="file"
        url="http://localhost:8000/uploadfile"
        :auto="true"
        accept="audio/*"
        chooseLabel="Hochladen"
        customUpload
        @uploader="handleUpload($event.files as File[])"
      />
      <p v-if="transcriptionError" style="color: var(--danger)">{{ errorMessage }}</p>
      <p v-else-if="fileSize && fileName">{{ fileName }} ({{ fileSize }})</p>
    </div>
  </section>
</template>

<script setup lang="ts">
import { type FileTranscriptionProps } from '@/model/interfaces';
import { ref } from 'vue';

const emit = defineEmits(['startUpload']);
defineProps<FileTranscriptionProps>();

const fileName = ref('');
const fileSize = ref(0);

function handleUpload(files: File[]) {
  // Reset state
  fileName.value = '';
  fileSize.value = 0;

  const file = files[0];
  console.log('Got File from user: ', file);
  if (!file) {
    //TODO: handle this
    console.log('no file error');
  }
  fileName.value = file.name;
  fileSize.value = file.size;

  emit('startUpload', files);
}
</script>
