<script setup lang="ts">
import { useFetch } from '@vueuse/core';

const { isFetching, error, data } = useFetch('http://127.0.0.1:8000')
</script>

<template>
  <main>
    <h1>Ambient Speech Recognition</h1>
    <h3>Data from Server:</h3>
    <p v-if="isFetching">...Loading :]</p>
    <p v-else-if="error">ERROR: {{ error }}</p>
    <p v-else>{{ data }}</p>
  </main>
</template>

<style>
main {
    display: flex;
    flex-direction: column;
    place-items: center;
}
</style>
