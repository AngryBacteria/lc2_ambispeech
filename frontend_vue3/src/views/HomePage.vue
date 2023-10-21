<script setup lang="ts">
import FileTranscriber from '@/components/FileTranscriber.vue';
</script>

<template>
  <main>
    <FileTranscriber></FileTranscriber>
  </main>
</template>

<style scoped>
main {
  display: flex;
  flex-direction: column;
  gap: 2rem;
  align-items: center;
}
</style>
