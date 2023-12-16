<template>
  <Dialog
    v-model:visible="isVisible"
    modal
    :closable="false"
    header="Patient anmelden"
    :style="{ width: '50rem' }"
    :breakpoints="{ '1199px': '75vw', '575px': '90vw' }"
  >
    <section class="account-input" v-if="!store.practitioner?.id">
      <InputText type="text" placeholder="Benutzername" @keydown.enter="loginPractitioner()" />
      <InputText type="text" placeholder="Passwort" @keydown.enter="loginPractitioner()" />
      <Button
        @keyup.enter="loginPractitioner()"
        @click="loginPractitioner()"
        label="Anmelden"
        severity="success"
      />
    </section>
    <section class="patient-input" v-if="!store.patient?.id && store.practitioner?.id">
      <Dropdown
        v-model="localPatient"
        filter
        :options="patients"
        :optionLabel="patientOptions"
        placeholder="Patient*in suchen"
      />
    </section>
    <section v-if="localPatient?.id && store.practitioner?.id">
      <PatientSummary :localPatient="localPatient" />
      <Button
        @click="loginPatient()"
        label="Bestätigen"
        severity="success"
        @keyup.enter="loginPatient()"
      />
    </section>
  </Dialog>
</template>

<script setup lang="ts">
import { useUserStore } from '@/stores/user';
import { computed, ref } from 'vue';
import practitionersData from '@/data/practitioners.json';
import patientData from '@/data/patients.json';
import type { Patient, Practitioner } from '@/model/interfaces';
import PatientSummary from '@/components/general/PatientSummary.vue';
import { useRouter } from 'vue-router';

// Data
const patients: Patient[] = patientData as unknown as Patient[];
const practitioners: Practitioner[] = practitionersData as unknown as Practitioner[];

// Formatted data
const patientOptions = (patient: Patient) =>
  `${patient.name[0].given[0]} ${patient.name[0].family} (${patient.identifier[0].value})`;
const localPatient = ref<Patient | undefined>(undefined);

// Composables
const store = useUserStore();
const router = useRouter();

function loginPractitioner() {
  store.practitioner = practitioners[0];
}

function loginPatient() {
  if (localPatient.value) {
    store.patient = localPatient.value;
    router.push('/');
  }
}

const isVisible = computed(() => {
  if (store.isDebug) {
    return false;
  }
  if (!store.patient || !store.practitioner) {
    return true;
  } else {
    return false;
  }
});
</script>

<style scoped>
.account-input {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
</style>
