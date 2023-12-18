import copy
from enum import Enum
from typing import List, Dict, TypedDict, Union

from asyncer import asyncify
from fastapi import APIRouter
from fastapi import Response, status
from pydantic import BaseModel, ValidationError

from app.data.data import prompt_data, OpenaiModel, lock, Extraction, PromptIdentifier, MedicalDataPrompt
from app.utils.embedding_util import EmbeddingUtil
from app.utils.general_util import parse_json_from_string
from app.utils.openai_util import (
    OpenAIUtil,
    OpenaiCompletionConfig,
    OpenaiCompletionBody,
)


class AnalyzeBody(BaseModel):
    """Body for an /analyze request"""

    text: str


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


@llmRouter.post("/hello/{model}")
async def hello(model: OpenaiModel, config: OpenaiCompletionConfig):
    """Hello World example for large language models"""
    openaiUtil.openai_model = model
    return await openaiUtil.hello_chat_completion(config, model)


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


# TODO: add logic for using embeddings or not using then
# TODO: add logic for summary of patient history/symptoms as freetext
@llmRouter.post("/analyze")
async def analyze(body: AnalyzeBody, response: Response) -> Union[Extraction, str]:
    """Endpoint for analyzing a conversation between a doctor and his patient.
    Returns an HTTP-206 code if no valid JSON was parsed"""
    # get the prompt for the analyze request
    prompt = await get_prompt(body.text, PromptIdentifier.SYMPTOM_EXTRACT_JSON)
    if prompt is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return f"No prompt found for identifier"

    # query the model to get Medical Data
    output = await openaiUtil.chat_completion(
        prompt.messages,
        OpenaiCompletionConfig(
            max_tokens=4096, response_format={"type": "json_object"}
        ),
        OpenaiModel.GPT_4,
    )

    # parse output and validate
    parsed = parse_json_from_string(output)
    try:
        validated = Extraction.model_validate(parsed)
        # add icd10 codes to extraction
        await add_icd10_codes(validated)
        return validated
    except ValidationError:
        response.status_code = status.HTTP_206_PARTIAL_CONTENT
        return output


async def add_icd10_codes(extraction: Extraction):
    """Adds icd10 codes to an extraction object"""
    async with lock:
        for extraction in extraction.symptoms:
            res = await asyncify(embedUtil.search)(
                embedUtil.icd10_symptoms, extraction.context, 1
            )
            extraction.icd10 = (
                res["schlüsselnummer_mit_punkt"].iloc[0]
                + " "
                + res["klassentitel"].iloc[0]
            )


async def get_prompt(text: str, identifier: PromptIdentifier) -> MedicalDataPrompt | None:
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
