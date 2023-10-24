<template>
  <h1>Recorder</h1>
  <section class="action-row">
    <Button
      @click="startRecording()"
      :disabled="isRecording"
      label="Start"
      icon="pi pi-play"
      size="small"
    />
    <Button
      @click="stopRecording()"
      :disabled="!isRecording"
      label="Stop"
      icon="pi pi-pause"
      size="small"
    />
    <Button
      @click="upload()"
      :disabled="!dataAvailable || isRecording"
      label="Upload"
      icon="pi pi-upload"
      size="small"
    />
    <Button
      @click="deleteData()"
      :disabled="!dataAvailable || isRecording"
      label="Delete recorded data"
      icon="pi pi-trash"
      size="small"
    />
  </section>
</template>

<script setup lang="ts">
import { ref } from 'vue';

const isRecording = ref(false);
const dataAvailable = ref(false);

async function startRecording() {
  isRecording.value = true;
  dataAvailable.value = true;
}

async function stopRecording() {
  isRecording.value = false;
}

async function upload() {
  isRecording.value = false;
  dataAvailable.value = false;
}

async function deleteData() {
  dataAvailable.value = false;
}
</script>

<style scoped>
.action-row {
  display: flex;
  flex-direction: row;
  gap: 1rem;
}
</style>
