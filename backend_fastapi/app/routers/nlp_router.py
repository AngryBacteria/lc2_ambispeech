import copy
from enum import Enum
from typing import List, Dict, TypedDict, Union

from asyncer import asyncify
from fastapi import APIRouter
from fastapi import Response, status
from pydantic import BaseModel, ValidationError

from app.data.data import prompt_data, OpenaiModel, lock, Extraction
from app.utils.embedding_util import EmbeddingUtil
from app.utils.general_util import parse_json_from_string
from app.utils.openai_util import (
    OpenAIUtil,
    OpenaiCompletionConfig,
    OpenaiCompletionBody,
)


class AnalyzeService(str, Enum):
    """Enum for all supported NLP analyze services"""

    OPENAI = "openai"


class AnalyzeBody(BaseModel):
    """Body for an /analyze request"""

    text: str
    service: AnalyzeService


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


# todo: implement possibility to add embeddings to the output
@llmRouter.post("/analyze")
async def analyze(body: AnalyzeBody, response: Response) -> Union[Extraction, str]:
    """Endpoint for analyzing a conversation between a doctor and his patient.
    Returns an HTTP-206 code if no valid JSON was parsed"""
    async with lock:
        prompt_data_copy = copy.deepcopy(prompt_data)
    prompt = prompt_data_copy.prompts[0]
    # replace the placeholder from the prompt with the message from the user
    for message in prompt.messages:
        if prompt_data_copy.userinput_placeholder in message.content:
            message.content = message.content.replace(
                prompt_data_copy.userinput_placeholder, body.text
            )

    output = ""
    if body.service is AnalyzeService.OPENAI:
        output = await openaiUtil.chat_completion(
            prompt.messages,
            OpenaiCompletionConfig(
                max_tokens=4096, response_format={"type": "json_object"}
            ),
            OpenaiModel.GPT_3_TURBO_1106,
        )

    # parse output and validate
    parsed = parse_json_from_string(output)
    try:
        return Extraction.model_validate(parsed)
    except ValidationError:
        response.status_code = status.HTTP_206_PARTIAL_CONTENT
        return output
