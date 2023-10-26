<template>
  <section class="settings-wrapper">
    <h1>Einstellungen</h1>
    <Button @click="store.resetSettings" severity="warning">Einstellungen Zurücksetzen</Button>
    <section class="settings">
      <section class="setting">
        <h2>Buffer-Grösse</h2>
        <p>
          Eine grösserer Buffer bringt eine höhere Audioqualität, verbraucht aber mehr Speicher. Wir
          empfehlen 4096.
        </p>
        <Dropdown
          v-model="store.bufferSize"
          :options="bufferSizes"
          optionLabel="name"
          option-value="code"
          placeholder="Buffer-Grösse"
        />
      </section>
      <section class="setting">
        <h2>Audio Datei nach aufnahme Herunterladen?</h2>
        <ToggleButton v-model="store.downloadRecording" />
      </section>
      <section class="setting">
        <h2>OpenAI</h2>
        <p>OpenAI ermöglicht es den Output etwas anzupassen mithilfe von Parametern.</p>
        <section class="sliders">
          <div v-for="slider in openAiSettings" :key="slider.label" style="width: 300px">
            <p style="margin: 0">{{ slider.label }}</p>
            <InputNumber
              v-model.number="store.openAiConfig[slider.label]"
              :max="slider.max"
              :min="slider.min"
              :maxFractionDigits="1"
              :step="0.1"
              style="width: 100%"
            />
            <Slider
              v-model="store.openAiConfig[slider.label]"
              :max="slider.max"
              :min="slider.min"
              :step="0.1"
              style="width: 100%"
            />
          </div>
        </section>
      </section>
    </section>
  </section>
</template>

<script setup lang="ts">
import { useUserStore } from '@/stores/user';
import { ref } from 'vue';

const store = useUserStore();

const bufferSizes = ref([
  { name: 256, code: 256 },
  { name: 512, code: 512 },
  { name: 1024, code: 1024 },
  { name: 2048, code: 2048 },
  { name: 4096, code: 4096 },
  { name: 8192, code: 8192 },
  { name: 16384, code: 16384 }
]);

const openAiSettings = [
  {
    label: 'frequency_penalty',
    min: -2,
    max: 2
  },
  {
    label: 'presence_penalty',
    min: -2,
    max: 2
  },
  {
    label: 'temperature',
    min: 0,
    max: 2
  },
  {
    label: 'top_p',
    min: 0,
    max: 2
  }
] as const;
</script>

<style>
.settings-wrapper {
  padding-left: 2rem;
  padding-right: 2rem;
}

.settings {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.sliders {
  display: flex;
  flex-direction: row;
  gap: 2rem;
  flex-wrap: wrap;
}
</style>
