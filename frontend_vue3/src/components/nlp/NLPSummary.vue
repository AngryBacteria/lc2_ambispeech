<template>
  <div class="layout">
    <section v-for="symptom in data.symptoms" :key="symptom.symptom" class="symptom">
      <section class="title">
        <h1>{{ symptom.symptom }}</h1>
        <Tag
          @click="showSymptomContext(symptom.symptom, symptom.context)"
          v-if="symptom.isInTranscript"
          severity="success"
          value="Im Transkript"
          style="cursor: pointer"
        ></Tag>
        <Tag v-else severity="warning" value="Nicht im Transkript"></Tag>
      </section>
      <p><b>Dauer:</b> {{ symptom.onset }}</p>
      <p><b>Position:</b> {{ symptom.location }}</p>

      <SelectButton v-model="symptom.status" :options="statusOptions" aria-labelledby="basic" />
    </section>
  </div>
  <Button @click="sendToKIS">Daten an KIS senden</Button>
</template>

<script setup lang="ts">
import _NLPData from '@/data/mockExtraction.json';
import type { NLPData, NLPStatus } from '@/model/interfaces';
import { useUserStore } from '@/stores/user';
import { useDialog } from 'primevue/usedialog';
import ContextConfirmDialog from './ContextConfirmDialog.vue';
import { ref, watch } from 'vue';
import { storeToRefs } from 'pinia';
import { useLocalStorage } from '@vueuse/core';

// Get store data
const store = useUserStore();
const { transcriptionText } = storeToRefs(store);

// Get NLP-Data and initialize it
const data = useLocalStorage('nlpSummaryDataTest', _NLPData as NLPData);
data.value.symptoms = data.value.symptoms.map((symptom) => {
  if (!symptom.status) {
    return {
      ...symptom,
      status: 'preliminary'
    };
  } else {
    return symptom;
  }
});
const statusOptions = ref<NLPStatus[]>(['amended', 'preliminary', 'entered-in-error']);

//Start watching the NLPData and update if it is in the transcript
function isInTranscript(toFind: string) {
  console.log('GO');
  return store.transcriptionText.includes(toFind);
}
watch(
  transcriptionText,
  () => {
    data.value.symptoms = data.value.symptoms.map((symptom) => ({
      ...symptom,
      isInTranscript: isInTranscript(symptom.context)
    }));
  },
  { immediate: true }
);

//TODO: into fhir?
async function sendToKIS() {
  console.log(data.value);
}

//Dialog
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
  margin-bottom: 1rem;
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
