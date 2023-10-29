import { defineStore } from 'pinia';
import { useDark, useLocalStorage, useToggle, useWindowSize } from '@vueuse/core';
import type { BufferSize, TranscriptionLanguage } from '@/model/interfaces';

export const useUserStore = defineStore('user', () => {
  // General app state
  const { width, height } = useWindowSize();
  const isDark = useDark();
  const toggleDark = useToggle(isDark);

  // Transcribption state
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
  }

  const openAiPrompt = useLocalStorage(
    'openAiPrompt',
    `
  Gegeben ist das folgende Transkript eines Dialogs zwischen Ärzten und Patienten. Bitte extrahiere spezifische Informationen über Symptome und Medikamente und gib diese im JSON-Format zurück:

  <PLACEHOLDER>

  Bitte geben Sie das Ergebnis im folgenden Format:

  {
  "Symptome": ["Symptom1", "Symptom2", ...],
  "Medikamente": ["Medikament1", "Medikament2", ...]
  }
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
    useDiarization
  };
});
