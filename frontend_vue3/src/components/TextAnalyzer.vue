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
    import { ref } from 'vue';

    let transcription = ref('');
    let extractedInfo = ref('');
    let analysisIsLoading = ref(false);
    let llmApiUrl = 'http://127.0.0.1:8000/api/llm/openai/gpt-3.5-turbo';

    async function analyzeText() {
        if (!transcription.value.trim()) return; // No Input no output.

        analysisIsLoading.value = true;

        //TODO relocate max tokens into backend and other settings to settings page
        let requestBody = {
            messages: [
                {
                role: 'user',
                content: transcription.value
                }
            ],
            config: {
                max_tokens: 50,
                temperature: 1,
                presence_penalty: 0,
                top_p: 1
            }
        };

        try {
            const response = await fetch(llmApiUrl, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json',},
            body: JSON.stringify(requestBody),
        });

        const data = await response.json();
        console.log(data)
        if (data.length > 1) {
            extractedInfo.value = data;
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
  