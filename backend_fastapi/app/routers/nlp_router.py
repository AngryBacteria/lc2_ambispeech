import json
from enum import Enum

from fastapi import APIRouter
from pydantic import BaseModel
from starlette.responses import StreamingResponse
from fastapi import Response, status

from app.utils.general_util import parse_json_from_string
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
    text: str
    service: AnalyzeService


llmRouter = APIRouter(
    prefix="/api/nlp",
    tags=["nlp"],
)

openaiUtil = OpenAIUtil()
# TODO think about if those paths will be the same no matter where you start the app. For other paths relevant too
# TODO maybe move into general util?
with open("app/data/lc2_data.json", 'r', encoding='utf-8') as file:
    data = json.load(file)


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


@llmRouter.post("/analyze")
async def analyze(body: AnalyzeBody, response: Response):
    """Endpoint for analyzing a conversation between a doctor and his patient. All configurations done"""
    prompt = data["prompting"]["prompts"][0]
    for message in prompt["messages"]:
        if "<PLACEHOLDER>" in message["content"]:
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

