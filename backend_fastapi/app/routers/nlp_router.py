import json
from enum import Enum

from fastapi import APIRouter
from pydantic import BaseModel
from starlette.responses import StreamingResponse, JSONResponse

from app.data.prompts_verions import prompts
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


def parse_json_from_string(input_string):
    start_index = input_string.find('{')
    if start_index == -1:
        start_index = input_string.find('[')
        if start_index == -1:
            return "No JSON data found"

    end_index = input_string.rfind('}')
    if end_index == -1:
        end_index = input_string.rfind(']')
        if end_index == -1:
            return "No JSON data found"

    json_string = input_string[start_index:end_index + 1]

    try:
        parsed_json = json.loads(json_string)
        return parsed_json
    except json.JSONDecodeError:
        return "Invalid JSON data"


llmRouter = APIRouter(
    prefix="/api/nlp",
    tags=["nlp"],
)

openaiUtil = OpenAIUtil()


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
async def analyze(body: AnalyzeBody):
    """Endpoint for analyzing a conversation between a doctor and his patient. All configurations done"""
    prompt = prompts[0]
    for message in prompt.messages:
        if "<PLACEHOLDER>" in message["content"]:
            message["content"] = message["content"].replace("<PLACEHOLDER>", body.text)

    if body.service is AnalyzeService.OPENAI:
        openaiUtil.openai_model = OpenaiModel.GPT_3_TURBO_16k

        # TODO: tokens anpassen? und error falls kein json
        output = await openaiUtil.chat_completion(
            prompt.messages,
            OpenaiCompletionConfig(
                max_tokens=10,
                response_format={"type": "JSON"}
            )
        )
        return parse_json_from_string(output)
