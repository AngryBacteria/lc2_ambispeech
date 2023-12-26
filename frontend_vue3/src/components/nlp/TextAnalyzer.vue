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
          <section v-if="!analysisError && !store.analysisIsLoading && !store.extractedInfoObject">
            <h2>Es sind noch keine Daten verfügbar</h2>
          </section>

          <section v-if="!analysisError && !store.analysisIsLoading">
            <section v-if="store.extractedInfoObject?.anamnesis">
              <h2>Zusammenfassung</h2>
              <section v-html="markdown.render(store.extractedInfoObject.anamnesis)" />
            </section>

            <section v-if="store.extractedInfoObject?.symptoms">
              <h2>Strukturierte Daten</h2>
              <SymptomSummary />
            </section>
          </section>
        </AccordionTab>
      </Accordion>
    </section>
  </section>
</template>

<script setup lang="ts">
import { useUserStore } from '@/stores/user';
import { ref } from 'vue';
import SymptomSummary from '@/components/nlp/SymptomSummary.vue';
import SlimProgressBar from '@/components/general/SlimProgressBar.vue';
import { NLPDataSchema } from '@/model/interfaces';
import MarkdownIt from 'markdown-it';

const store = useUserStore();
let llmApiUrl = 'http://localhost:8000/api/nlp/analyze';
const markdown = new MarkdownIt();

const analysisError = ref('');

async function analyzeText(text: string) {
  store.analysisIsLoading = true;
  analysisError.value = '';
  store.extractedInfoObject = null;

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
      // check type with zod
      let parsed = NLPDataSchema.safeParse(answer);
      if (parsed.success) {
        store.extractedInfoObject = parsed.data;
      } else {
        analysisError.value =
          'Während dem Analysieren geschah ein Fehler. Versuche erneut: ' + parsed.error.message;
      }
    }

    if (!response.ok) {
      analysisError.value = 'Während dem Analysieren geschah ein Fehler. Versuche erneut.';
    }
  } catch (error) {
    console.error('Error:', error);
    analysisError.value = 'Während dem Analysieren geschah ein Fehler. Versuche erneut.';
    store.extractedInfoObject = null;
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

p {
  white-space: pre-line;
}
</style>
