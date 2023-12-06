<template>
  <div>
    <h3>Personalien</h3>
    <p>
      <b>Name:</b> {{ localPatient.name[0].given[0] }} {{ localPatient.name[0].family }} ({{
        localPatient.gender
      }})
    </p>
    <p>
      <b>Geboren am:</b> {{ localPatient.birthDate }} ({{ yearsSince(localPatient.birthDate) }}
      jahre alt)
    </p>
    <p>
      <b>Adresse:</b> {{ localPatient.address[0].line[0] }} {{ localPatient.address[0].city }} ({{
        localPatient.address[0].postalCode
      }})
    </p>
    <h3>Kontakt</h3>
    <p><b>Telefon:</b> {{ localPatient.telecom[0].value }}</p>
    <p>
      <b>E-Mail: </b>
      <a :href="'mailto:' + localPatient.telecom[1].value">{{ localPatient.telecom[1].value }}</a>
    </p>
    <h3>Versicherung</h3>
    <p><b>Versicherten-Nummer:</b> {{ localPatient.identifier[0].value }}</p>
  </div>
</template>
<script setup lang="ts">
import type { Patient } from '@/model/interfaces';

defineProps<{
  localPatient: Patient;
}>();

function yearsSince(dateString: string) {
  const givenDate = new Date(dateString);
  const currentDate = new Date();

  const differenceInTime = currentDate.getTime() - givenDate.getTime();
  const differenceInYears = differenceInTime / (1000 * 60 * 60 * 24 * 365);

  return Math.floor(differenceInYears);
}
</script>
<style scoped></style>
