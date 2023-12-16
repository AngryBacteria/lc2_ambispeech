<template>
  <section class="component-wrapper">
    <section>
      <SlimProgressBar :is-error="analysisError.length > 0" :value="0" />
      <Accordion>
        <AccordionTab>
          <template #header>
            <section style="display: flex; align-items: center; width: 100%">
              <div>Extrahierte Informationen</div>
              <Button
                @click="
                  $event.stopPropagation();
                  analyzeText(store.transcriptionText);
                "
                :label="store.isMobile ? '' : 'Analyse starten'"
                icon="pi pi-eye"
                size="small"
                :loading="store.analysisIsLoading"
                :class="{
                  hidden: store.transcriptionText.length <= 0 || store.transcriptionIsLoading
                }"
                style="margin-left: auto"
              />
            </section>
          </template>
          <h2 v-if="store.analysisIsLoading">Am Analysieren...</h2>
          <p v-if="analysisError">{{ analysisError }}</p>

          <section
            v-if="
              !analysisError &&
              !store.analysisIsLoading &&
              (store.extractedInfoObject || store.extractedInfoText)
            "
          >
            <section v-if="store.extractedInfoText && !store.extractedInfoObject">
              <h2>Die Analyse konnte nicht vollständig durchgeführt werden</h2>
              <p>{{ store.extractedInfoText }}</p>
            </section>

            <section v-else>
              <NLPSummary />
            </section>
          </section>

          <section
            v-if="
              !analysisError &&
              !store.analysisIsLoading &&
              !store.extractedInfoObject &&
              !store.extractedInfoText
            "
          >
            <h2>Es sind noch keine Daten verfügbar</h2>
          </section>
        </AccordionTab>
      </Accordion>
    </section>
  </section>
</template>

<script setup lang="ts">
import { useUserStore } from '@/stores/user';
import { ref } from 'vue';
import NLPSummary from '@/components/nlp/NLPSummary.vue';
import SlimProgressBar from '@/components/general/SlimProgressBar.vue';

const store = useUserStore();
let llmApiUrl = 'http://localhost:8000/api/nlp/analyze';

const analysisError = ref('');

async function analyzeText(text: string) {
  store.analysisIsLoading = true;
  analysisError.value = '';
  store.extractedInfoObject = null;
  store.extractedInfoText = '';

  const requestBody = {
    text: text,
    service: 'openai'
  };

  try {
    const response = await fetch(llmApiUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(requestBody)
    });

    if (response.status == 200) {
      const answer = await response.json();
      store.extractedInfoObject = answer;
      store.extractedInfoText = '';
    }
    if (response.status == 206) {
      const answer = await response.text();
      store.extractedInfoObject = null;
      store.extractedInfoText = answer;
    }
    if (!response.ok) {
      analysisError.value = 'Während dem Analysieren geschah ein Fehler. Versuche erneut.';
    }
  } catch (error) {
    console.error('Error:', error);
    analysisError.value = 'Während dem Analysieren geschah ein Fehler. Versuche erneut.';
    store.extractedInfoObject = null;
    store.extractedInfoText = '';
  } finally {
    store.analysisIsLoading = false;
  }
}
</script>

<style scoped>
.p-inputtextarea {
  width: 100%;
}
:deep(.p-accordion .p-accordion-header .p-accordion-header-link) {
  border-top-left-radius: 0px;
  border-top-right-radius: 0px;
}
</style>
