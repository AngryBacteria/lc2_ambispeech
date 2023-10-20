import { defineStore } from 'pinia';
import { useDark, useToggle, useWindowSize } from '@vueuse/core';

export const useUserStore = defineStore('user', () => {
  const { width, height } = useWindowSize();
  const isDark = useDark();
  const toggleDark = useToggle(isDark);

  //Maybe interesting
  //https://vueuse.org/core/useWebNotification/
  //https://vueuse.org/core/useDevicesList/
  //https://vueuse.org/core/useOnline/
  //https://vueuse.org/core/useWebSocket/
  //https://vueuse.org/core/useConfirmDialog/

  return { width, height, isDark, toggleDark };
});
