from openai.types.chat import (
    ChatCompletionSystemMessageParam,
    ChatCompletionUserMessageParam,
)
from pydantic import BaseModel
from typing import Union, List


class PromptVersion(BaseModel):
    messages: List[
        Union[ChatCompletionSystemMessageParam, ChatCompletionUserMessageParam]
    ]
    version: int
    placeholder_index: int


prompts: List[PromptVersion] = [
    PromptVersion(
        messages=[
            {
                "role": "system",
                "content": """Gegeben ist das folgende Transkript eines Dialogs zwischen Ärzten und Patienten. Bitte extrahiere spezifische Informationen über Symptome und Medikamente und gib diese im JSON-Format zurück:

<PLACEHOLDER>

Bitte geben Sie das Ergebnis im folgenden Format:

{
„Symptome“: [„Symptom1“, „Symptom2“, …],
„Medikamente“: [„Medikament1“, „Medikament2“, …]
}
""",
            }
        ],
        version=1,
        placeholder_index=0,
    )
]
