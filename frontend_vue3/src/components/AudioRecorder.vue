<script setup lang="ts">
import { RecordRTCPromisesHandler, StereoAudioRecorder, invokeSaveAsDialog } from 'recordrtc'

async function startRecording() {
  let stream = await navigator.mediaDevices.getUserMedia({ audio: true })
  let recorder = new RecordRTCPromisesHandler(stream, {
    recorderType: StereoAudioRecorder,
    mimeType: 'audio/wav',
    disableLogs: false,
    numberOfAudioChannels: 1,
    sampleRate: 44100,
    desiredSampRate: 16000,
    ondataavailable: function (blob) {
      console.log('SOME NEW DATA', blob)
    }
  })
  recorder.startRecording()

  const sleep = (m: number | undefined) => new Promise((r) => setTimeout(r, m))
  await sleep(3000)

  await recorder.stopRecording()
  let blob = await recorder.getBlob()
  invokeSaveAsDialog(blob)
}
</script>

<template>
  <h2>This is the audio recorder component</h2>
  <button @click="startRecording()">Start Audio Recording</button>
</template>
