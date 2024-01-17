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
      <p><b>ICD10-Code:</b> {{ symptom.icd10 }}</p>
      <p><b>Kontext:</b> {{ symptom.context }}</p>

      <SelectButton
        v-model="symptom.status"
        :options="statusOptions"
        optionLabel="name"
        aria-labelledby="basic"
      />
    </section>
  </div>
  <Button @click="sendToKIS">Daten an KIS senden</Button>
</template>

<script setup lang="ts">
import { useUserStore } from '@/stores/user';
import { useDialog } from 'primevue/usedialog';
import ContextConfirmDialog from './ContextConfirmDialog.vue';
import { ref, watch } from 'vue';
import { storeToRefs } from 'pinia';
import { v4 as uuidv4 } from 'uuid';

// Get store data
const store = useUserStore();
const { transcriptionText, extractedInfoObject } = storeToRefs(store);

// Get NLP-Data and initialize it
watch(
  extractedInfoObject,
  () => {
    if (!extractedInfoObject.value?.symptoms) {
      return;
    }

    extractedInfoObject.value.symptoms = extractedInfoObject.value.symptoms.map((symptom) => {
      if (!symptom.status) {
        return {
          ...symptom,
          status: 'unconfirmed'
        };
      } else {
        return symptom;
      }
    });
  },
  { immediate: true }
);
const statusOptions = ref([
  { name: 'Unbestätigt', value: 'unconfirmed' },
  { name: 'Bestätigt', value: 'confirmed' },
  { name: 'Falsch', value: 'Irrtümlich eingegeben' }
]);

//Start watching the NLPData and update if it is in the transcript
function isInTranscript(toFind: string) {
  let found = store.transcriptionText.toLowerCase().includes(toFind.toLowerCase());
  return found;
}
watch(
  transcriptionText,
  () => {
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

function sendToKIS() {
  // Create conditions
  if (!extractedInfoObject.value?.symptoms) {
    return;
  }
  const fhirConditions = extractedInfoObject.value.symptoms.map((symptom) => {
    return {
      resourceType: 'Condition',
      id: 'condition_' + uuidv4(),
      clinicalStatus: {
        coding: [
          {
            system: 'http://terminology.hl7.org/CodeSystem/condition-clinical',
            code: 'active'
          }
        ]
      },
      verificationStatus: {
        coding: [
          {
            system: 'http://terminology.hl7.org/CodeSystem/condition-ver-status',
            code: symptom.status
          }
        ]
      },
      code: {
        coding: [
          {
            system: 'http://fhir.de/CodeSystem/dimdi/icd-10-gm',
            version: '2019',
            code: symptom.icd10,
            display: symptom.symptom
          }
        ],
        text: symptom.symptom
      },
      subject: {
        reference: `Patient/${store.patient?.id}`
      },
      onsetString: symptom.onset
    };
  });
  console.log('Conditions: ', fhirConditions);

  // Create references
  const fhirConditionsReferences = fhirConditions.map((condition) => {
    return {
      reference: {
        identifier: condition.id
      }
    };
  });
  console.log('Condition References: ', fhirConditionsReferences);

  // Create encounter
  const fhirEncounter = {
    resourceType: 'Encounter',
    id: 'encounter_' + uuidv4(),
    text: {
      status: 'generated',
      div: `<p xmlns="http://www.w3.org/1999/xhtml">${extractedInfoObject.value.anamnesis}</p>>`
    },
    status: 'in-progress',
    class: [
      {
        coding: [
          {
            system: 'http://terminology.hl7.org/CodeSystem/v3-ActCode',
            code: 'EMER',
            display: 'emergency'
          }
        ]
      }
    ],
    reason: [
      {
        value: fhirConditionsReferences
      }
    ],
    subject: {
      reference: `Patient/${store.patient?.id}`
    },
    subjectStatus: {
      coding: [
        {
          system: 'http://terminology.hl7.org/CodeSystem/encounter-subject-status',
          code: 'receiving-care'
        }
      ]
    }
  };
  console.log('Encounter: ', fhirEncounter);

  // Create bundle
  const fhirBundle = {
    resourceType: 'Bundle',
    id: 'bundle_' + uuidv4(),
    type: 'collection',
    entry: [
      {
        resource: fhirEncounter
      },
      ...fhirConditions.map((condition) => {
        return {
          resource: condition
        };
      })
    ]
  };
  console.log('Bundle: ', fhirBundle);

  const jsonString = JSON.stringify(fhirBundle, null, 2);
  const fileToSave = new Blob([jsonString], {
    type: 'application/json'
  });
  const fileDownloadUrl = URL.createObjectURL(fileToSave);
  const downloadLink = document.createElement('a');
  downloadLink.href = fileDownloadUrl;
  downloadLink.download = 'fhirConditions.json';
  document.body.appendChild(downloadLink);
  downloadLink.click();
  document.body.removeChild(downloadLink);
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
