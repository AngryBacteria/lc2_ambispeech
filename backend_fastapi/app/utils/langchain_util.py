from __future__ import annotations

from dotenv import load_dotenv
from langchain.chains import LLMChain
from langchain.output_parsers.json import SimpleJsonOutputParser
from langchain.prompts import PromptTemplate

from app.data.data import LLMService, GenericLangChainModel
from app.langchain.gpt4all_helper import GPT4AllHelper
from app.langchain.openai_helper import OpenAIHelper
from app.utils.logging_util import logger


class LangchainUtil:
    """Singleton util class to handle various llm related operations with langchain"""

    _instance = None
    prompt_template = PromptTemplate(
        input_variables=["transcript"],
        template="""Gegeben ist das folgende Transkript eines Dialogs zwischen Ärzten und Patienten. Bitte extrahiere 
        spezifische Informationen über Symptome und Medikamente und gib diese im JSON-Format zurück:

           {transcript}
            
            Bitte geben Sie das Ergebnis im folgenden Format: 
            
            „Symptome“: [„Symptom1“, „Symptom2“, …],
            „Medikamente“: [„Medikament1“, „Medikament2“, …]
            
             """,
    )

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(LangchainUtil, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, "_initialized"):
            return
        load_dotenv()
        logger.info("Created LangchainUtil")
        self._initialized = True

    def test(self, model: LLMService, message):
        json_chain = (
            self.prompt_template
            | get_helper_from_model(model).get_llm()
            | SimpleJsonOutputParser()
        )

        return json_chain.invoke({"transcript": message})

    def hello_chat_completion(self, model: LLMService):
        """Hello World chat completion example for llm with langchain"""
        llm = get_helper_from_model(model).get_llm()
        return llm.invoke("Hello World")

    def chat_completion(self, model: LLMService, transcript):
        helper = get_helper_from_model(model)
        if not helper:
            raise ValueError(f"Unsupported model: {model}")

        chain = LLMChain(llm=helper.get_llm(), prompt=self.prompt_template)

        return chain.run(transcript)


def get_helper_from_model(model: LLMService) -> GenericLangChainModel:
    match model:
        case model.GPT4ALL:
            return GPT4AllHelper()
        case model.OPENAI:
            return OpenAIHelper()
