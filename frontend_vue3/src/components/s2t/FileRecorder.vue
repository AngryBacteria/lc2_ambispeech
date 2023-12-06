<template>
  <section class="recorder-wrapper">
    <SlimProgressBar :is-error="transcriptionError.length > 1" :value="uploadProgress" />
    <section class="action-row">
      <Button
        @click="startRecording()"
        :disabled="isRecording || transcriptionIsLoading"
        label="Start"
        icon="pi pi-play"
      />
      <Button @click="pauseRecording()" :disabled="!isRecording" label="Pause" icon="pi pi-pause" />
      <Button
        @click="upload()"
        :disabled="!dataAvailable || isRecording"
        label="Hochladen"
        icon="pi pi-upload"
      />
      <Button
        @click="deleteData()"
        :disabled="!dataAvailable || isRecording"
        label="Aufnahme löschen"
        icon="pi pi-trash"
      />
      <p v-if="transcriptionError" style="color: var(--danger)">{{ transcriptionError }}</p>
      <p v-else-if="estimatedSize > 0" style="margin: 0">
        Aufnahmegrösse: {{ estimatedSizeString }}
      </p>
    </section>
  </section>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue';
import { RecordRTCPromisesHandler, StereoAudioRecorder, invokeSaveAsDialog } from 'recordrtc';
import { useUserStore } from '@/stores/user';
import { type FileTranscriptionProps } from '@/model/interfaces';
import { getHumanFileSize } from '@/composables/util';
import { useToast } from 'primevue/usetoast';
import SlimProgressBar from '../general/SlimProgressBar.vue';

enum RecordingStateFlag {
  START,
  PAUSE,
  RESUME,
  UPLOAD,
  DELETE
}

// Props v-model and emits
const emit = defineEmits(['startUpload']);
defineProps<FileTranscriptionProps>();
const transcriptionError = defineModel<string>('transcriptionError', {
  required: true
});

const isRecording = ref(false);
const dataAvailable = ref(false);
const estimatedSize = ref(0);

const estimatedSizeString = computed(() => {
  return getHumanFileSize(estimatedSize.value);
});

const store = useUserStore();
const toast = useToast();

let stream: MediaStream;
let recorder: RecordRTCPromisesHandler;

/**
 * Starts the recording. If necessary it also builds the stream and recorder.
 * If the recorder was previously stopped or the recorder inactive, it starts.
 * If the recorder was previously paused, it resumes
 */
async function startRecording() {
  if (!stream) {
    try {
      stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    } catch (error) {
      toast.add({
        severity: 'warn',
        summary: 'Kein Zugriff auf ihr Mikrofon',
        detail:
          'Die Applikation braucht Zugriff auf ihr Mikrofon um die Aufnahme zu starten. Überprüfen sie ihre Browsereinstellungen'
      });
      return;
    }
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
        if (blob?.size) {
          estimatedSize.value = estimatedSize.value + blob.size;
        }
      }
    });
    setState(RecordingStateFlag.START);
    await recorder.startRecording();
    return;
  }
  if ((await recorder?.getState()) === 'inactive' || (await recorder?.getState()) === 'stopped') {
    setState(RecordingStateFlag.START);
    await recorder.startRecording();
    return;
  }
  if ((await recorder.getState()) === 'paused') {
    setState(RecordingStateFlag.RESUME);
    await recorder.resumeRecording();
  }
}

/**
 * Pauses the recording
 */
async function pauseRecording() {
  setState(RecordingStateFlag.PAUSE);
  await recorder.pauseRecording();
}

/**
 * Stops the recording, downloads the files and clears the data from the recorder with recorder.reset()
 */
async function upload() {
  setState(RecordingStateFlag.UPLOAD);
  await recorder.stopRecording();
  let blob = await recorder.getBlob();
  emit('startUpload', [new File([blob], 'recording.wav')]);
  if (store.downloadRecording) invokeSaveAsDialog(blob);
  await recorder.reset();
}

/**
 * Stops the recording and clears the data from the recorder with recorder.reset()
 */
async function deleteData() {
  setState(RecordingStateFlag.DELETE);
  await recorder.stopRecording();
  await recorder.reset();
}

function setState(state: RecordingStateFlag) {
  switch (state) {
    case RecordingStateFlag.START:
      isRecording.value = true;
      dataAvailable.value = true;
      estimatedSize.value = 0;
      transcriptionError.value = '';
      break;
    case RecordingStateFlag.PAUSE:
      isRecording.value = false;
      break;
    case RecordingStateFlag.RESUME:
      isRecording.value = true;
      break;
    case RecordingStateFlag.UPLOAD:
      isRecording.value = false;
      dataAvailable.value = false;
      break;
    case RecordingStateFlag.DELETE:
      isRecording.value = false;
      dataAvailable.value = false;
      estimatedSize.value = 0;
      break;
  }
}
</script>

<style scoped>
.recorder-wrapper {
  border-radius: var(--custom-border-radius);
  background-color: var(--surface-card);
  border: 1px solid var(--surface-border);
}
.action-row {
  padding: 1rem;
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  align-items: center;
  gap: 1rem;
}

.centered-p {
  margin-top: auto;
  margin-bottom: auto;
}
</style>
