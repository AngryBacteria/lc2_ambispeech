<template>
  <h1>Recorder</h1>
  <section class="recorder-wrapper">
    <ProgressBar v-if="!transcriptionError" :value="uploadProgress"></ProgressBar>
    <ProgressBar v-else style="background-color: var(--danger)"></ProgressBar>
    <section class="action-row">
      <Button
        @click="startRecording()"
        :disabled="isRecording"
        label="Start"
        icon="pi pi-play"
        size="small"
      />
      <Button
        @click="pauseRecording()"
        :disabled="!isRecording"
        label="Pause"
        icon="pi pi-pause"
        size="small"
      />
      <Button
        @click="upload()"
        :disabled="!dataAvailable || isRecording"
        label="Upload"
        icon="pi pi-upload"
        size="small"
      />
      <Button
        @click="deleteData()"
        :disabled="!dataAvailable || isRecording"
        label="Delete recorded data"
        icon="pi pi-trash"
        size="small"
      />
    </section>
  </section>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { RecordRTCPromisesHandler, StereoAudioRecorder, invokeSaveAsDialog } from 'recordrtc';
import { useUserStore } from '@/stores/user';
import { type FileTranscriptionProps } from '@/model/interfaces';

const emit = defineEmits(['startUpload']);
defineProps<FileTranscriptionProps>();

const isRecording = ref(false);
const dataAvailable = ref(false);
const store = useUserStore();

let stream: MediaStream;
let recorder: RecordRTCPromisesHandler;

/**
 * Starts the recording. If necessary it also builds the stream and recorder.
 * If the recorder was previously stopped or the recorder inactive, it starts.
 * If the recorder was previously paused, it resumes
 */
async function startRecording() {
  isRecording.value = true;
  dataAvailable.value = true;

  if (!stream) {
    stream = await navigator.mediaDevices.getUserMedia({ audio: true });
  }

  if (!recorder) {
    recorder = new RecordRTCPromisesHandler(stream, {
      recorderType: StereoAudioRecorder,
      mimeType: 'audio/wav',
      disableLogs: false,
      //no benefit for speech to text, but more = better normally
      numberOfAudioChannels: 1,
      //leave this
      desiredSampRate: 16000,
      //Higher = better quality but higher file size
      bufferSize: store.bufferSize,
      //How many milliseconds until new data gets sent
      timeSlice: 1500,
      ondataavailable: function (blob) {
        console.log('SOME NEW DATA', blob);
      }
    });
    await recorder.startRecording();
    return;
  }
  if ((await recorder?.getState()) === 'inactive' || (await recorder?.getState()) === 'stopped') {
    await recorder.startRecording();
    return;
  }
  if ((await recorder.getState()) === 'paused') {
    await recorder.resumeRecording();
  }
}

/**
 * Pauses the recording
 */
async function pauseRecording() {
  isRecording.value = false;
  await recorder.pauseRecording();
}

/**
 * Stops the recording, downloads the files and clears the data from the recorder with recorder.reset()
 */
async function upload() {
  isRecording.value = false;
  dataAvailable.value = false;
  await recorder.stopRecording();
  let blob = await recorder.getBlob();
  emit('startUpload', [new File([blob], 'recording.wav')]);
  invokeSaveAsDialog(blob);
  await recorder.reset();
}

/**
 * Stops the recording and clears the data from the recorder with recorder.reset()
 */
async function deleteData() {
  isRecording.value = false;
  dataAvailable.value = false;
  await recorder.stopRecording();
  await recorder.reset();
}
</script>

<style scoped>
.recorder-wrapper {
  border-radius: 6px;
  background-color: var(--surface-card);
}
.action-row {
  padding: 1rem;
  display: flex;
  flex-direction: row;
  gap: 1rem;
}

.p-progressbar-determinate .p-progressbar-value-animate {
  transition: width 0.1s ease-in-out;
}

.p-progressbar {
  border-bottom-left-radius: 0;
  border-bottom-right-radius: 0;
  height: 8px;
}

:deep(.p-progressbar-label) {
  display: none;
}
</style>
