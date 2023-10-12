<script setup lang="ts">
import { ref } from 'vue';

const data = ref("")
const request = await fetch("http://127.0.0.1:8000")
data.value = await request.text()
</script>

<template>
    <h1>hello world</h1>
    <p>{{ data }}</p>
</template>