<template>
    <section class="component-wrapper">
      <h3>Füge den transkribierten Text hier ein</h3>
      <Textarea
        v-model="transcription"
        autoResize
        rows="4"
      />
      <Button @click="analyzeText()">Analyze Text</Button>
  
      <Accordion>
        <AccordionTab header="Extrahierte Informationen">
          <p v-if="analysisIsLoading">Am Analysieren...</p>
          <p> {{ extractedInfo }}</p>
        </AccordionTab>
      </Accordion>
    </section>
</template>
  
<script setup lang="ts">
    import { useUserStore } from '@/stores/user';
    import { ref } from 'vue';

    const transcription = ref('');
    const extractedInfo = ref('');
    const analysisIsLoading = ref(false);
    const userStore = useUserStore();
    let llmApiUrl = 'http://127.0.0.1:8000/api/llm/openai/gpt-3.5-turbo';

    async function analyzeText() {
        if (!transcription.value.trim()) return; // No Input no output.

        analysisIsLoading.value = true;

        //Load prompt and insert transcript
        let prompt = userStore.openAiPrompt.replace('<PLACEHOLDER>', transcription.value)

        //TODO relocate max tokens into backend
        let requestBody = {
            messages: [
                {
                role: 'user',
                content: prompt
                }
            ],
            config: {
                max_tokens: 50,
                temperature: userStore.openAiConfig.temperature,
                presence_penalty: userStore.openAiConfig.presence_penalty,
                top_p: userStore.openAiConfig.top_p,
                frequency_penalty: userStore.openAiConfig.frequency_penalty
            }
        };

        try {
            const response = await fetch(llmApiUrl, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json',},
            body: JSON.stringify(requestBody),
        });

        const answer = await response.json();
        console.log(answer)
        if (answer.length > 1) {
            extractedInfo.value = answer;
        }
        } catch (error) {
            console.error('Error:', error);
        } finally {
            analysisIsLoading.value = false;
        }
    }
</script>
  
<style>
    .component-wrapper {
        width: 80%;
        display: flex;
        gap: 1rem;
        flex-direction: column;
    }

    .p-inputtextarea {
        width: 100%;
    }
</style>
  