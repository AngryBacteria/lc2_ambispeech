<template>
  <div class="layout">
    <section v-for="symptom in data.symptoms" :key="symptom.symptom" class="symptom">
      <section class="title">
        <h1>{{ symptom.symptom }}</h1>
        <Tag
          @click="showSymptomContext(symptom.symptom, symptom.context)"
          v-if="isInTranscript(symptom.context)"
          severity="info"
          value="Im Transkript"
          style="cursor: pointer"
        ></Tag>
        <Tag v-else severity="warning" value="Nicht im Transkript"></Tag>
      </section>
      <p><b>Dauer:</b> {{ symptom.onset }}</p>
      <p><b>Position:</b> {{ symptom.location }}</p>
    </section>
  </div>
</template>

<script setup lang="ts">
import _NLPData from '@/data/mockExtraction.json';
import type { NLPData } from '@/model/interfaces';
import { useUserStore } from '@/stores/user';
import { useDialog } from 'primevue/usedialog';
import { defineAsyncComponent } from 'vue';
const ContextConfirmDialog = defineAsyncComponent(() => import('./ContextConfirmDialog.vue'));

const store = useUserStore();

const data = _NLPData as NLPData;

/**
 * Determines if the context is present in the transcript or not
 */
function isInTranscript(toFind: string) {
  return store.transcriptionText.includes(toFind);
}

const dialog = useDialog();

const showSymptomContext = (symptomText: string, symptomContext: string) => {
  dialog.open(ContextConfirmDialog, {
    data: {
      symptomContext: symptomContext,
      transcript: store.transcriptionText
    },
    props: {
      header: `Kontext von Symptom: ${symptomText}`,
      style: {
        width: '50vw'
      },
      breakpoints: {
        '960px': '75vw',
        '640px': '90vw'
      },
      modal: true,
      maximizable: true
    }
  });
};
</script>

<style scoped>
h1 {
  margin: 0;
}

.layout {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

@media screen and (max-width: 750px) {
  .layout {
    grid-template-columns: 1fr;
  }
}

.title {
  font-size: 1.5rem;
  display: flex;
  flex-direction: row;
  gap: 1rem;
}

.symptom {
  background-color: var(--surface-ground);
  padding: 10px;
  border-radius: var(--border-radius);
}
</style>
