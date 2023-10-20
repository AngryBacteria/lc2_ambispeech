<template>
  <h2>Playground</h2>
  <h3>This is some Test Data from Server:</h3>
  <p v-if="isFetching">...Loading :]</p>
  <p v-else-if="error">ERROR: {{ error }}</p>
  <p v-else>{{ data }}</p>
  <Button
    @click="fetchAndPrintStream('http://127.0.0.1:8000/stream', {})"
    label="GetStream"
    icon="pi pi-check"
    loadingIcon="pi pi-spin pi-spinner"
    :loading="isFetching"
  />
  <Button
    @click="
      fetchAndPrintStream('http://127.0.0.1:8000/api/llm/openaistream/gpt-3.5-turbo', postExample)
    "
    label="Get Openai Stream"
    icon="pi pi-check"
    loadingIcon="pi pi-spin pi-spinner"
    :loading="isFetching"
  />
</template>

<script setup lang="ts">
import { useFetch } from '@vueuse/core'

const { isFetching, error, data } = useFetch('http://127.0.0.1:8000')

const postExample: RequestInit = {
  method: 'POST',
  headers: { 'content-type': 'application/json' },
  body: JSON.stringify({
    messages: [
      {
        role: 'user',
        content: 'hello world! I am so happy :]'
      }
    ],
    config: {
      max_tokens: 10,
      temperature: 1,
      presence_penalty: 0,
      top_p: 1
    }
  })
}

async function fetchAndPrintStream(url: string, fetchConfig: RequestInit) {
  try {
    const response = await fetch(url, fetchConfig)
    const reader = response?.body?.getReader()
    const decoder = new TextDecoder()

    while (response.ok && reader && true) {
      const { value, done } = await reader.read()

      if (done) {
        console.log('server event stream is done')
        break
      }

      // Convert chunk from Uint8Array to string and print it out.
      const text = decoder.decode(value)
      console.log(text)
    }
  } catch (err) {
    console.error('Error:', err)
  }
}
</script>
