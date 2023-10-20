<script setup lang="ts">
import FileTranscriber from '@/components/FileTranscriber.vue'
</script>

<template>
  <main>
    <h1>Ambient Speech Recognition</h1>
    <FileTranscriber></FileTranscriber>
  </main>
</template>

<style>
main {
  display: flex;
  flex-direction: column;
  gap: 2rem;
  align-items: center;
}
</style>
