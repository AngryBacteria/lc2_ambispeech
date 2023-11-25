<template>
  <div v-if="data?.symptomContext && data?.transcript">
    <div v-html="highlightedTranscript" />
  </div>
</template>

<script setup lang="ts">
import { computed, inject, ref } from 'vue';

interface ContextDialogData {
  symptomContext: string;
  transcript: string;
}

/**
 * Ref to track data that was passed to the dialog
 */
const data = ref<ContextDialogData | undefined>();

/**
 * Gets injected by primevue
 */
const dialogRef: any = inject('dialogRef');
/**
 * Fill passed data into ref
 */
const params = dialogRef?.value?.data;
data.value = {
  symptomContext: params?.symptomContext,
  transcript: params?.transcript
};

/**
 * Created a html version of the transcriptText with context highlighting
 */
const highlightedTranscript = computed(() => {
  let output = '<p>';
  if (!data.value?.symptomContext || !data.value?.transcript) {
    return '';
  }

  output =
    output +
    data.value?.transcript.replace(
      new RegExp(data.value?.symptomContext, 'gi'),
      (match: any) => `<mark>${match}</mark>`
    );
  output = output + '</p>';
  return output;
});
</script>

<style scoped></style>
