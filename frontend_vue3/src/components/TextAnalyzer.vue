<template>
  <section class="component-wrapper">
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
        <p v-if="store.analysisIsLoading">Am Analysieren...</p>
        <p v-if="analysisError">{{ analysisError }}</p>
        <p>{{ store.extractedInfo }}</p>
      </AccordionTab>
    </Accordion>
  </section>
</template>

<script setup lang="ts">
import { useUserStore } from '@/stores/user';
import { ref } from 'vue';

const store = useUserStore();
let llmApiUrl = 'http://localhost:8000/api/llm/openai/gpt-3.5-turbo';

const analysisError = ref('');

async function analyzeText(text: string) {
  store.analysisIsLoading = true;
  analysisError.value = '';

  let prev_messages = [
    {
      role: 'system',
      content:
        'Du bist ein System, das aus einem Transkript eines gesprochenen Dialogs in einem medizinischen Kontext die Symptome und Medikamente des Patienten extrahiert und in einem JSON-Format zurückgibt.'
    },
    {
      role: 'user',
      content:
        'Das ist Franz Feldmann, 66 Jahre. Hat vernichtende Brustschmerzen seit etwa 30 Minuten. Strahlen aus in den linken Arm. Hat etwas Dyspnö, ist nicht synkopiert. Keine KHK bekannt. Hat noch Hypertonus, kennt aber seine Medis nicht. Vitalparameter waren Blutdruck 145 zu 90, Puls 95, Sauerstoffsättigung 93% an Raumluft. Haben mal 4 Liter Sauerstoff und 2mg Morphin gegeben. Das EKG hatten wir Euch schon per Mail geschickt. Da hat es Senkungen in V2 bis V4. Wir haben mit Heparin noch gewartet, weil er nicht sicher war, ob er auch was zur Blutverdünnung nimmt. Ich nehme Tabletten für meinen Bluthochdruck, aber den Namen weiß ich nicht.'
    },
    {
      role: 'system',
      content: JSON.stringify({
        Symptome: ['halbstündige Brustschmerzen', 'leichte Dyspnö', 'Hypertonus'],
        Medikamente: ['Bluthochdruckmedikamente']
      })
    }
  ];

  //Load prompt and insert transcript
  let prompt = store.openAiPrompt.replace('<PLACEHOLDER>', text);

  //TODO handling too large file
  //TODO relocate max tokens into backend

  let { temperature, presence_penalty, top_p, frequency_penalty } = store.openAiConfig;

  let requestBody = {
    messages: [
      ...prev_messages,
      {
        role: 'user',
        content: prompt
      }
    ],
    config: {
      max_tokens: 50,
      temperature,
      presence_penalty,
      top_p,
      frequency_penalty
    }
  };

  try {
    const response = await fetch(llmApiUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(requestBody)
    });

    const answer = await response.json();
    console.log(answer);
    if (answer.length > 1) {
      store.extractedInfo = answer;
    } else {
      analysisError.value = 'Keine Informationen konnten herausgezogen werden.';
    }
  } catch (error) {
    console.error('Error:', error);
    analysisError.value = 'Während dem Analysieren geschah ein Fehler. Versuche erneut.';
  } finally {
    store.analysisIsLoading = false;
  }
}
</script>

<style>
.p-inputtextarea {
  width: 100%;
}
</style>
