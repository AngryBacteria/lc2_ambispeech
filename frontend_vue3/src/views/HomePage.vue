<script setup lang="ts">
import FileTranscriber from '@/components/FileTranscriber.vue';
import TextAnalyzer from '@/components/TextAnalyzer.vue';
</script>

<template>
  <main>
    <FileTranscriber></FileTranscriber>

    <TextAnalyzer></TextAnalyzer>
  </main>
</template>

<style scoped>
main {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  align-items: center;
}
</style>
