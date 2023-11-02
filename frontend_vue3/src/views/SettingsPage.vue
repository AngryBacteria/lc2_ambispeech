<template>
  <section class="settings-wrapper">
    <h1>Einstellungen</h1>
    <Button @click="store.resetSettings" severity="warning">Einstellungen Zurücksetzen</Button>
    <section class="settings">
      <section class="setting">
        <h2>Cloud Dienste verwenden für Speech to Text?</h2>
        <ToggleButton
          v-model="store.useCloudS2T"
          onLabel="Ja"
          offLabel="Nein"
          onIcon="pi pi-check"
          offIcon="pi pi-times"
        />
      </section>
      <section class="setting">
        <h2>Cloud Dienste verwenden für Natural Language Processing?</h2>
        <ToggleButton
          v-model="store.useCloudLLM"
          onLabel="Ja"
          offLabel="Nein"
          onIcon="pi pi-check"
          offIcon="pi pi-times"
        />
      </section>
      <section class="setting">
        <h2>Sprecher-Erkennung (Diarization) aktivieren?</h2>
        <ToggleButton
          v-model="store.useDiarization"
          onLabel="Ja"
          offLabel="Nein"
          onIcon="pi pi-check"
          offIcon="pi pi-times"
        />
      </section>
      <section class="setting">
        <h2>Audio Datei nach aufnahme Herunterladen?</h2>
        <ToggleButton
          v-model="store.downloadRecording"
          onLabel="Ja"
          offLabel="Nein"
          onIcon="pi pi-check"
          offIcon="pi pi-times"
        />
      </section>
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
        <h2>Sprache für die Audio Transkribierung</h2>
        <Dropdown
          v-model="store.transcriptionLanguage"
          :options="transcriptionLanguages"
          optionLabel="name"
          option-value="code"
          placeholder="Transkribierungssprache"
        />
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

const transcriptionLanguages = ref([
  { name: 'Deutsch (Schweiz)', code: 'de-CH' },
  { name: 'Deutsch', code: 'de-DE' },
  { name: 'Deutsch (Östereich)', code: 'de-AT' },
  { name: 'Englisch (England)', code: 'en-GB' },
  { name: 'Englisch (USA)', code: 'en-US' }
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
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
  margin-bottom: 3rem;
  margin-top: 1rem;
}

@media (max-width: 600px) {
  /* Adjusts the layout for small devices */
  .settings {
    grid-template-columns: 1fr; /* Makes it a single column on small screens */
  }
}

.setting {
  background-color: var(--surface-card);
  padding: 1rem;
  border-radius: var(--custom-border-radius);
}

.sliders {
  display: flex;
  flex-direction: row;
  gap: 2rem;
  flex-wrap: wrap;
}
</style>
