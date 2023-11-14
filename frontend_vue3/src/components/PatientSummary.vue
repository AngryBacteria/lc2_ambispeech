<template>
  <div>
    <p>
      <b>Name:</b> {{ localPatient.name[0].given[0] }} {{ localPatient.name[0].family }} ({{
        localPatient.gender
      }})
    </p>
    <p>
      <b>Geboren am:</b> {{ localPatient.birthDate }} ({{ yearsSince(localPatient.birthDate) }}
      jahre alt)
    </p>
    <p><b>Versicherten-Nummer:</b> {{ localPatient.identifier[0].value }}</p>
    <p>
      <b>Adresse:</b> {{ localPatient.address[0].line[0] }} {{ localPatient.address[0].city }} ({{
        localPatient.address[0].postalCode
      }})
    </p>
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
<style></style>
