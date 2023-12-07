import json
from enum import Enum

from fastapi import APIRouter
from pydantic import BaseModel
from starlette.responses import StreamingResponse
from fastapi import Response, status

from app.data import nlp_data
from app.utils.embedding_util import EmbeddingUtil
from app.utils.general_util import parse_json_from_string
from app.utils.logging_util import logger
from app.utils.openai_util import (
    OpenAIUtil,
    OpenaiModel,
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
    return await openaiUtil.hello_chat_completion(config)


@llmRouter.post("/openai/{model}")
async def openai(model: OpenaiModel, body: OpenaiCompletionBody):
    """Non-Streaming OpenAI chat completion"""
    openaiUtil.openai_model = model
    return await openaiUtil.chat_completion(body.messages, body.config)


@llmRouter.post("/openaistream/{model}")
async def openai(model: OpenaiModel, body: OpenaiCompletionBody):
    """Streaming OpenAI chat completion"""
    openaiUtil.openai_model = model
    return StreamingResponse(
        openaiUtil.stream_chat_completion(body.messages, body.config),
        media_type="text/event-stream",
    )


@llmRouter.post("/embedding")
async def getEmbedding(body: EmbeddingBody):
    res = embedUtil.search(embedUtil.icd10_symptoms, body.text, body.amount)
    output = res[["V8", "V9"]].rename(columns={'V8': 'code', 'V9': 'text'})
    return output.to_dict(orient='records')


@llmRouter.post("/analyze")
async def analyze(body: AnalyzeBody, response: Response):
    """Endpoint for analyzing a conversation between a doctor and his patient.
    Returns an HTTP-206 code if no valid JSON was parsed"""
    prompt = nlp_data["prompting"]["prompts"][0]
    # replace the placeholder from the prompt with the message from the user
    for message in prompt["messages"]:
        if nlp_data["prompting"]["userinput_placeholder"] in message["content"]:
            message["content"] = message["content"].replace("<PLACEHOLDER>", body.text)

    output = ""
    if body.service is AnalyzeService.OPENAI:
        openaiUtil.openai_model = OpenaiModel.GPT_4_TURBO

        # TODO: tokens anpassen? und error falls kein json
        output = await openaiUtil.chat_completion(
            prompt["messages"],
            OpenaiCompletionConfig(
                max_tokens=4096,
                response_format={"type": "json_object"}
            )
        )
    parsed = parse_json_from_string(output)
    if parsed == "parsing_error":
        response.status_code = status.HTTP_206_PARTIAL_CONTENT
        return output
    else:
        return parsed
