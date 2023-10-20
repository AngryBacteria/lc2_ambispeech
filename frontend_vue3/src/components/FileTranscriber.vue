<template>
  <h2>File Transcriber</h2>
  <h3>Custom Upload XHR</h3>
  <FileUpload
    mode="basic"
    name="file"
    url="http://localhost:8000/uploadfile"
    accept="audio/*"
    :auto="true"
    chooseLabel="Hochladen"
    customUpload
    @uploader="customUploaderXHR($event)"
  />


  <h3>Custom Upload Fetch</h3>
  <FileUpload
    mode="basic"
    name="file"
    url="http://localhost:8000/uploadfile"
    accept="audio/*"
    :auto="true"
    chooseLabel="Hochladen"
    customUpload
    @uploader="customUploaderFetch($event)"
  />
</template>

<script setup lang="ts">
import type { FileUploadUploaderEvent } from 'primevue/fileupload'

function customUploaderXHR(event: FileUploadUploaderEvent) {
  const data = new FormData();
  const file = (event.files as File[])[0];
  console.log(file.name);
  data.append('file', file);

  const xhr = new XMLHttpRequest();
  
  // Event listener for progress
  xhr.upload.onprogress = function(e) {
    if (e.lengthComputable) {
      const percentComplete = (e.loaded / e.total) * 100;
      console.log(`Upload progress: ${percentComplete}%`);
    }
  };

  let lastReadPosition = 0;

  xhr.onreadystatechange = function() {
    if (xhr.readyState === XMLHttpRequest.LOADING) {
      const newText = xhr.responseText.substring(lastReadPosition);
      console.log("New chunk received:", newText);
      lastReadPosition = xhr.responseText.length;
    }

    if (xhr.readyState === XMLHttpRequest.DONE) {
      console.log('Streaming done');
    }
  };

  // Event listener for errors during the request
  xhr.onerror = function() {
    console.error('XHR error.');
  };

  xhr.open('POST', 'http://localhost:8000/uploadfile', true);
  xhr.send(data);
}


//Todo: see if possible without custom uploader
async function customUploaderFetch(event: FileUploadUploaderEvent) {
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
