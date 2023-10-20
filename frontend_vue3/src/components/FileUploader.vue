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
        accept="audio/wav"
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
import { ref } from 'vue';

const emit = defineEmits(['startUpload']);
defineProps<{
  transcriptionError: boolean;
  transcriptionIsLoading: boolean;
  uploadProgress: number;
  errorMessage: string;
}>();

const fileName = ref('');
const fileSize = ref();

function handleUpload(files: File[]) {
  const file = files[0];
  if (!file) {
    //TODO: handle this
    console.log('handle this');
  }
  fileName.value = file.name;
  fileSize.value = file.size;

  emit('startUpload', files);
}
</script>
