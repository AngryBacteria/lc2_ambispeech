<template>
  <h2>File Transcriber</h2>
  <FileUpload
    mode="basic"
    name="file"
    url="http://localhost:8000/uploadfile"
    accept="audio/*"
    :auto="true"
    chooseLabel="Hochladen"
    customUpload
    @uploader="customUploader($event)"
  />
</template>

<script setup lang="ts">
import type { FileUploadUploaderEvent } from 'primevue/fileupload'

//Todo see if possible without custom uploader
async function customUploader(event: FileUploadUploaderEvent) {
  const data = new FormData()
  const file = (event.files as File[])[0]
  console.log(file.name)
  data.append('file', file)
  console.log(data)

  const req = await fetch('http://localhost:8000/uploadfile', { method: 'POST', body: data })
  const reader = req?.body?.getReader()
  const decoder = new TextDecoder()

  while (req.ok && reader && true) {
    const { value, done } = await reader.read()

    if (done) {
      console.log('server event stream is done')
      break
    }

    // Convert chunk from Uint8Array to string and print it out.
    const text = decoder.decode(value)
    console.log(text)
  }

  console.log('UPLOAD done', event)
}
</script>
