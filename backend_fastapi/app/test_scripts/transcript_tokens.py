import json
import os
import tiktoken

from app.data.data import PromptData
from app.utils.general_util import clean_string


def get_tokens_lengths():
    file_paths = "F:\\OneDrive - Berner Fachhochschule\\Dokumente\\UNI\\Semester 5\\LC2\\speech_to_text\\testfiles\\transcripts"
    prompt_file = "X:\\Programming\\Web\\lc2_ambispeech\\backend_fastapi\\app\\data\\lc2_data.json"

    ## Get token lengths for audio examples
    files = [f for f in os.listdir(file_paths) if f.endswith(".txt")]
    token_lengths = []
    for file in files:
        with open(os.path.join(file_paths, file), 'r') as f:
            file_content = f.read()
            enc = tiktoken.encoding_for_model("gpt-4")
            tokens = enc.encode(clean_string(file_content))
            token_lengths.append(len(tokens))

    average_audio_tokens = sum(token_lengths) / len(token_lengths)
    print(f"Average token length (audio examples): {average_audio_tokens}")

    ## Get token lengths for prompts
    prompt_lengths = []
    _json_file_path = os.path.join(prompt_file)
    with open(_json_file_path, "r", encoding="utf-8") as file:
        _nlp_data = json.load(file)

        # parse prompt data
        prompt_data = PromptData(**_nlp_data["prompting"])

        for prompt in prompt_data.prompts:
            prompt_text = prompt.messages[0].content
            enc = tiktoken.encoding_for_model("gpt-4")
            tokens = enc.encode(prompt_text)
            prompt_lengths.append(len(tokens))

    average_prompt_tokens = sum(prompt_lengths) / len(prompt_lengths)
    print(f"Average token length (prompts): {average_prompt_tokens}")

    print(f"Overall average length: {average_prompt_tokens + average_audio_tokens}")


get_tokens_lengths()
