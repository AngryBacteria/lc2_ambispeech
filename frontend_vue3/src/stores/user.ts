import { defineStore } from 'pinia';
import {
  StorageSerializers,
  useDark,
  useLocalStorage,
  useSessionStorage,
  useToggle,
  useWindowSize
} from '@vueuse/core';
import type {
  BufferSize,
  Patient,
  Practitioner,
  SymptomData,
  TranscriptionLanguage
} from '@/model/interfaces';
import { computed, ref } from 'vue';

export const useUserStore = defineStore('user', () => {
  // General app state
  /**
   * Indicates if the app is in debug mode.
   * This enables manually editing state that shouldnt be editable normally
   */
  const isDebug = ref(true);
  const { width, height } = useWindowSize();
  const isDark = useDark();
  const toggleDark = useToggle(isDark);
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

  /**
   * Parameters for the openai completion requests
   */
  const openAiConfig = useLocalStorage('openAiConfig', {
    frequency_penalty: 0,
    presence_penalty: 0,
    temperature: 1,
    top_p: 1
  });

  function resetSettings() {
    openAiConfig.value = {
      frequency_penalty: 0,
      presence_penalty: 0,
      temperature: 1,
      top_p: 1
    };
    bufferSize.value = 4096;
    downloadRecording.value = false;
    transcriptionLanguage.value = 'de-CH';
    useDiarization.value = false;
    useCloudLLM.value = true;
    useCloudS2T.value = true;
  }

  //Maybe interesting
  //https://vueuse.org/core/useWebNotification/
  //https://vueuse.org/core/useDevicesList/
  //https://vueuse.org/core/useOnline/
  //https://vueuse.org/core/useWebSocket/
  //https://vueuse.org/core/useConfirmDialog/

  return {
    width,
    height,
    isDark,
    toggleDark,
    bufferSize,
    openAiConfig,
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
