<script setup lang="ts">
import { RecordRTCPromisesHandler, StereoAudioRecorder, invokeSaveAsDialog } from 'recordrtc';

let stream: MediaStream;
let recorder: RecordRTCPromisesHandler;
let socket: WebSocket;

async function initRecorder() {
  socket = new WebSocket('ws://localhost:8000/api/transcribe/stream');

  socket.addEventListener('message', (event) => {
    console.log('Message from server: ', event.data);
  });

  stream = await navigator.mediaDevices.getUserMedia({ audio: true });
  recorder = new RecordRTCPromisesHandler(stream, {
    recorderType: StereoAudioRecorder,
    mimeType: 'audio/wav',
    disableLogs: false,
    //no benefit for speech to text, but more = better normally
    numberOfAudioChannels: 1,
    //leave this
    desiredSampRate: 16000,
    //Higher = better quality but higher file size
    bufferSize: 4096,
    //How many milliseconds until new data gets sent
    timeSlice: 1500,
    ondataavailable: function (blob) {
      console.log('SOME NEW DATA', blob);
      socket.send(blob);
    }
  });
}

async function startRecording() {
  await initRecorder();
  await recorder.startRecording();

  socket.onmessage = (event) => {
    console.log('Recieved from server: ', event.data);
  };
}

async function stopRecording() {
  await recorder.stopRecording();
  let blob = await recorder.getBlob();
  invokeSaveAsDialog(blob);
  await recorder.destroy();
  socket.close();
}
</script>

<template>
  <h2>This is the audio recorder component</h2>
  <button @click="startRecording()">Start Audio Recording</button>
  <button @click="stopRecording()">Stop and Save</button>
</template>
