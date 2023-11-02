import { defineStore } from 'pinia';
import { useDark, useLocalStorage, useToggle, useWindowSize } from '@vueuse/core';
import type { BufferSize, TranscriptionLanguage } from '@/model/interfaces';
import { ref } from 'vue';

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

  // Shared state
  /**
   * Text that was transcribed from audio
   */
  const transcriptionText = ref('');

  // Transcription state
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

  //LLM State
  /**
   * Parameters for the openai completion requests
   */
  const openAiConfig = useLocalStorage('openAiConfig', {
    frequency_penalty: 0,
    presence_penalty: 0,
    temperature: 1,
    top_p: 1
  });

  // Methods
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

  const openAiPrompt = useLocalStorage(
    'openAiPrompt',
    `
    Bitte extrahiere spezifische Informationen über Symptome und Medikamente aus diesem Transkript:

    <PLACEHOLDER>    
  `
  );

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
    openAiPrompt,
    downloadRecording,
    transcriptionLanguage,
    useDiarization,
    useCloudLLM,
    useCloudS2T,
    isDebug,
    transcriptionText
  };
});
