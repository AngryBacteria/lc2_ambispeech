import { defineStore } from 'pinia';
import { useDark, useLocalStorage, useToggle, useWindowSize } from '@vueuse/core';

export const useUserStore = defineStore('user', () => {
  const { width, height } = useWindowSize();

  const isDark = useDark();

  const toggleDark = useToggle(isDark);

  const bufferSize = useLocalStorage('bufferSize', 4096);

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
    openAiPrompt
  };
});
