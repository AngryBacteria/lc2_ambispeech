import asyncio
import copy
from typing import List, Union, Optional

from asyncer import asyncify
from fastapi import APIRouter
from pydantic import BaseModel, ValidationError

from app.data.data import (
    prompt_data,
    OpenaiModel,
    lock,
    Extraction,
    PromptIdentifier,
    MedicalDataPrompt,
    Symptom,
    SymptomICD10,
    ExtractionICD10,
)
from app.utils.embedding_util import EmbeddingUtil
from app.utils.general_util import parse_json_from_string
from app.utils.logging_util import logger
from app.utils.openai_util import (
    OpenAIUtil,
    OpenaiCompletionConfig,
    OpenaiCompletionBody,
)


class AnalyzeBody(BaseModel):
    """Body for an /analyze request"""

    text: str


class AnalyzeEndpointOutput(BaseModel):
    symptoms: Optional[List[SymptomICD10]] = None
    anamnesis: Optional[str] = None


class EmbeddingBody(BaseModel):
    """Body for an /embedding request"""

    text: str
    amount: int = 10


class EmbeddingEndpointOutput(BaseModel):
    code: str
    text: str


llmRouter = APIRouter(
    prefix="/api/nlp",
    tags=["nlp"],
)

# init dependencies
openaiUtil = OpenAIUtil()
embedUtil = EmbeddingUtil()


@llmRouter.post("/openai/{model}")
async def openai(model: OpenaiModel, body: OpenaiCompletionBody):
    """Non-Streaming OpenAI chat completion"""
    return await openaiUtil.chat_completion(body.messages, body.config, model)


@llmRouter.post("/embedding")
async def getEmbedding(body: EmbeddingBody) -> List[EmbeddingEndpointOutput]:
    # pandas dataframe is not thread-safe. Therefore, we need to use a lock
    async with lock:
        res = await asyncify(embedUtil.search)(
            embedUtil.icd10_symptoms, body.text, body.amount
        )
        output = res[["schlüsselnummer_mit_punkt", "klassentitel"]].rename(
            columns={"schlüsselnummer_mit_punkt": "code", "klassentitel": "text"}
        )
    return output.to_dict(orient="records")


# TODO: add logic for summary of patient history/symptoms as freetext
@llmRouter.post("/analyze")
async def analyze(body: AnalyzeBody) -> Union[AnalyzeEndpointOutput, str]:
    """Endpoint for analyzing a conversation between a doctor and his patient.
    Returns an HTTP-206 code if no valid JSON was parsed"""
    # init output object
    output = AnalyzeEndpointOutput()
    # run both request in parallel
    results = await asyncio.gather(get_extraction(body.text), get_anamnesis(body.text))
    # get the symptom extraction
    extraction = results[0]
    if extraction is not None:
        output.symptoms = extraction.symptoms

    # get the anamnesis
    anamnesis = results[1]
    if anamnesis is not None:
        output.anamnesis = anamnesis

    return output


async def get_anamnesis(text: str):
    # get the prompt for the anamnesis extraction
    prompt = await get_prompt(text, PromptIdentifier.ANAMNESIS_EXTRACT)
    if prompt is None:
        logger.error("No prompt found for anamnesis extraction")
        return None

    # get the extraction from the llm
    output = await openaiUtil.chat_completion(
        prompt.messages,
        OpenaiCompletionConfig(temperature=0, max_tokens=4096),
        OpenaiModel.GPT_3_TURBO,
    )
    return output


async def get_extraction(text: str, use_embeddings: bool = True):
    """Returns an Extraction object with icd-10 annotated symptoms.
    Either uses embeddings or the direct approach with prompting"""
    # get the prompt for the symptom extraction
    prompt = await get_prompt(text, PromptIdentifier.SYMPTOM_EXTRACT_JSON)
    if prompt is None:
        logger.error("No prompt found for symptom extraction")
        return None
    # get the extraction from the llm
    output = await openaiUtil.chat_completion(
        prompt.messages,
        OpenaiCompletionConfig(
            temperature=0, max_tokens=4096, response_format={"type": "json_object"}
        ),
        OpenaiModel.GPT_3_TURBO,
    )
    if use_embeddings:
        # parse output and validate
        parsed = parse_json_from_string(output)
        try:
            validated = Extraction.model_validate(parsed)
            # add icd10 codes to extraction
            extraction_with_codes = ExtractionICD10(
                symptoms=await add_icd10_codes(validated.symptoms)
            )
            return extraction_with_codes
        except ValidationError:
            logger.error(
                f"GPT Output could not be validated/parsed successfully: {output}"
            )
            return None
    else:
        # TODO: hier einbauen, dass auch direkt icd10 annotierte daten returniert werden ohne embeddings nur mit prompt
        raise NotImplementedError


async def add_icd10_codes(symptoms: List[Symptom]) -> List[SymptomICD10]:
    """Takes a list of symptoms without icd-10 codes and adds them with embeddings"""
    output = []
    async with lock:
        for symptom in symptoms:
            res = await asyncify(embedUtil.search)(
                embedUtil.icd10_symptoms, f"{symptom.symptom}. {symptom.context}", 1
            )
            icd10_string = (
                res["schlüsselnummer_mit_punkt"].iloc[0]
                + " - "
                + res["klassentitel"].iloc[0]
            )
            logger.debug("Embedding Input: " + f"{symptom.symptom}. {symptom.context}")
            logger.debug("Embedding Output: " + f"{icd10_string}")
            output.append(
                SymptomICD10(
                    icd10=icd10_string,
                    context=symptom.context,
                    location=symptom.location,
                    symptom=symptom.symptom,
                    onset=symptom.onset,
                )
            )
    return output


async def get_prompt(
    text: str, identifier: PromptIdentifier
) -> MedicalDataPrompt | None:
    """Returns a prompt for the given identifier. The placeholder for the userinput will be replaced with the text"""
    async with lock:
        prompt_data_copy = copy.deepcopy(prompt_data)

    found_prompts = []
    for pr in prompt_data_copy.prompts:
        if pr.identifier == identifier:
            found_prompts.append(pr)
    if len(found_prompts) == 0:
        return None

    prompt = found_prompts[0]
    # replace the placeholder from the prompt with the message from the user
    for message in prompt.messages:
        if prompt_data_copy.userinput_placeholder in message.content:
            message.content = message.content.replace(
                prompt_data_copy.userinput_placeholder, text
            )
    return prompt
