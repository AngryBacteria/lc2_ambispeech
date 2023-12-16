import { defineStore } from 'pinia';
import {
  StorageSerializers,
  useLocalStorage,
  useSessionStorage,
  useWindowSize
} from '@vueuse/core';
import type {
  BufferSize,
  Patient,
  Practitioner,
  SymptomData,
  TranscriptionLanguage
} from '@/model/interfaces';
import { computed, ref, watch } from 'vue';

export const useUserStore = defineStore('user', () => {
  // General app state
  /**
   * Indicates if the app is in debug mode.
   * This enables manually editing state that shouldnt be editable normally
   */
  const isDebug = ref(false);
  const { width, height } = useWindowSize();
  const isMobile = computed(() => {
    return width.value < 750;
  });

  // Session State
  const practitioner = useSessionStorage<Practitioner | null>('practitioner', null, {
    serializer: StorageSerializers.object
  });
  const patient = useSessionStorage<Patient | null>('patient', null, {
    serializer: StorageSerializers.object
  });

  /**
   * Resets the state if the practitioner or patient changes
   */
  watch([practitioner, patient], ([newPractitioner, newPatient], [oldPractitioner, oldPatient]) => {
    if (newPractitioner?.id !== oldPractitioner?.id || newPatient?.id !== oldPatient?.id) {
      resetAnalyzeState();
    }
  });

  // NLP State
  /**
   * Information (Data) that was extracted from the transcript with NLP
   */
  const extractedInfoText = useSessionStorage('extractedInfoText', '');
  const extractedInfoObject = useSessionStorage<SymptomData | null>('extractedInfoObject', null, {
    serializer: StorageSerializers.object
  });
  /**
   * If a transcription is currently loading or not
   */
  const analysisIsLoading = ref(false);

  // Transcription state
  /**
   * Text that was transcribed from audio
   */
  const transcriptionText = useSessionStorage('transcriptionText', '');
  /**
   * If a transcription is currently loading or not
   */
  const transcriptionIsLoading = ref(false);

  function resetAnalyzeState() {
    extractedInfoObject.value = null;
    extractedInfoText.value = '';
    analysisIsLoading.value = false;
    transcriptionText.value = '';
    transcriptionIsLoading.value = false;
  }

  // Settings-State
  /**
   * Buffer state to  use for the audio recording.
   * Higher value means better quality
   */
  const bufferSize = useLocalStorage<BufferSize>('bufferSize', 4096);
  /**
   * Boolean to control if an audio file should be downloaded after the recording or not
   */
  const downloadRecording = useLocalStorage<boolean>('downloadRecording', false);
  /**
   * What language to use for the transcription
   */
  const transcriptionLanguage = useLocalStorage<TranscriptionLanguage>(
    'transcriptionLanguage',
    'de-CH'
  );
  /**
   * If diarization should be used (azure only feature)
   */
  const useDiarization = useLocalStorage<boolean>('useDiarization', false);

  /**
   * If cloud services should be used for speech to text
   */
  const useCloudS2T = useLocalStorage<boolean>('useCloudS2T', true);

  /**
   * If cloud services should be used for natural langugae processing
   */
  const useCloudLLM = useLocalStorage<boolean>('useCloudLLM', true);

  function resetSettings() {
    bufferSize.value = 4096;
    downloadRecording.value = false;
    transcriptionLanguage.value = 'de-CH';
    useDiarization.value = false;
    useCloudLLM.value = true;
    useCloudS2T.value = true;
  }

  return {
    width,
    height,
    bufferSize,
    resetSettings,
    downloadRecording,
    transcriptionLanguage,
    useDiarization,
    useCloudLLM,
    useCloudS2T,
    isDebug,
    transcriptionText,
    practitioner,
    patient,
    transcriptionIsLoading,
    isMobile,
    extractedInfoText,
    extractedInfoObject,
    analysisIsLoading
  };
});
