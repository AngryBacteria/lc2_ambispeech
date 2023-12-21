<template>
  <div class="layout" v-if="extractedInfoObject">
    <section v-for="symptom in extractedInfoObject.symptoms" :key="symptom.symptom" class="symptom">
      <section class="title">
        <h1>{{ symptom.symptom }}</h1>
        <Tag
          @click="showSymptomContext(symptom.symptom, symptom.context)"
          v-if="symptom?.isInTranscript"
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
import type { NLPStatus } from '@/model/interfaces';
import { useUserStore } from '@/stores/user';
import { useDialog } from 'primevue/usedialog';
import ContextConfirmDialog from './ContextConfirmDialog.vue';
import { ref, watch } from 'vue';
import { storeToRefs } from 'pinia';

// Get store data
const store = useUserStore();
const { transcriptionText, extractedInfoObject } = storeToRefs(store);

// Get NLP-Data and initialize it
watch(
  extractedInfoObject,
  () => {
    console.log('GO DATA');
    if (!extractedInfoObject.value?.symptoms) {
      return;
    }

    extractedInfoObject.value.symptoms = extractedInfoObject.value.symptoms.map((symptom) => {
      if (!symptom.status) {
        return {
          ...symptom,
          status: 'preliminary'
        };
      } else {
        return symptom;
      }
    });
  },
  { immediate: true }
);
const statusOptions = ref<NLPStatus[]>(['amended', 'preliminary', 'entered-in-error']);

//Start watching the NLPData and update if it is in the transcript
function isInTranscript(toFind: string) {
  let found = store.transcriptionText.toLowerCase().includes(toFind.toLowerCase());
  return found;
}
watch(
  transcriptionText,
  () => {
    console.log('GO isInTranscript');
    if (!extractedInfoObject.value?.symptoms) {
      return;
    }
    extractedInfoObject.value.symptoms = extractedInfoObject.value.symptoms.map((symptom) => ({
      ...symptom,
      isInTranscript: isInTranscript(symptom.context)
    }));
  },
  { immediate: true }
);

//TODO: into fhir?
async function sendToKIS() {
  console.log(extractedInfoObject.value);
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
