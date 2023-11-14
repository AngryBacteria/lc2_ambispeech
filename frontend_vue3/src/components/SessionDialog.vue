<template>
  <Dialog
    v-model:visible="isVisible"
    modal
    :closable="false"
    header="Patient anmelden"
    :style="{ width: '50rem' }"
    :breakpoints="{ '1199px': '75vw', '575px': '90vw' }"
  >
    <section class="account-input" v-if="!store.practitioner">
      <InputText type="text" placeholder="Benutzername" @keydown.enter="login()" />
      <InputText type="text" placeholder="Passwort" @keydown.enter="login()" />
      <Button @click="login()" label="Anmelden" severity="success" />
    </section>
    <section class="patient-input" v-if="!localPatient && store.practitioner">
      <Dropdown
        v-model="localPatient"
        filter
        :options="patients"
        :optionLabel="patientOptions"
        placeholder="Patient*in suchen"
      />
    </section>
    <section v-if="localPatient">
      <PatientSummary :localPatient="localPatient" />
      <Button @click="store.patient = localPatient" label="Bestätigen" severity="success" />
    </section>
  </Dialog>
</template>

<script setup lang="ts">
import { useUserStore } from '@/stores/user';
import { computed, ref } from 'vue';
import practitionersData from '@/data/practitioners.json';
import patientData from '@/data/patients.json';
import type { Patient, Practitioner } from '@/model/interfaces';
import PatientSummary from './PatientSummary.vue';

const patients: Patient[] = patientData as unknown as Patient[];
const practitioners: Practitioner[] = practitionersData as unknown as Practitioner[];
const patientOptions = (patient: Patient) =>
  `${patient.name[0].given[0]} ${patient.name[0].family} (${patient.identifier[0].value})`;
const localPatient = ref<Patient | undefined>(undefined);

const store = useUserStore();

function login() {
  store.practitioner = practitioners[0];
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

<style>
.account-input {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
</style>
