<template>
  <ProgressBar v-if="isError" :value="0" style="background-color: var(--danger)" />
  <ProgressBar v-else :value="value" />
</template>

<script setup lang="ts">
defineProps<{
  isError: boolean;
  value: number;
}>();
</script>

<style scoped>
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
