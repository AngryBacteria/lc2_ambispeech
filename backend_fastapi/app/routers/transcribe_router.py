import wave
from enum import Enum

import aiofiles
import aiofiles.os
from fastapi import APIRouter, UploadFile, HTTPException, WebSocket, BackgroundTasks
from starlette.responses import StreamingResponse

from app.utils.azure_util import AzureUtil, AzureLanguageCode
from app.utils.logging_util import logger
from app.utils.whisper_util import WhisperUtil

transcribeRouter = APIRouter(
    prefix="/api/transcribe",
    tags=["transcribe"],
)

azure_util = AzureUtil()
whisper_util = WhisperUtil()


class TranscribeService(str, Enum):
    whisper = "whisper"
    azure = "azure"


async def async_delete_if_exists(filename: str):
    """Function to async delete a file if it exists. Useful for a fastapi background task"""
    try:
        if await aiofiles.os.path.exists(filename):
            await aiofiles.os.remove(filename)
            logger.info(f"File: {filename} deleted successfully")
        else:
            logger.info(f"File: {filename} does not exist")

    except Exception as error:
        logger.error(f"Error while deleting File: {filename} Error: {error}")


@transcribeRouter.post("/file/{service}")
async def post_file(
    background_tasks: BackgroundTasks,
    file: UploadFile,
    service: TranscribeService,
    diarization: bool = False,
    language: AzureLanguageCode = "de-CH",
):
    """
    Transcribes a file. Either with whisper locally or azure on the cloud.
    First it checks if the file is a correct wav file. After that it transcribes with the corresponding util classes.
    """
    # validate if the file is a valid wav
    try:
        await file.seek(0)
        with wave.open(file.file, "rb") as audio_file:
            audio_params = audio_file.getparams()
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Audio file was not in the correct format. Please provide an uncompressed WAV file.",
        )
    finally:
        await file.seek(0)

    # try to transcribe the wav
    try:
        if service.name.lower() == "whisper":
            async with aiofiles.open(
                f"upload_files/{file.filename}", "wb"
            ) as out_file:  # this closes the file
                while content := await file.read(1024):  # async read chunk
                    await out_file.write(content)  # async write chunk.

            background_tasks.add_task(async_delete_if_exists, f"upload_files/{file.filename}")

            return StreamingResponse(
                whisper_util.transcribe_file(out_file.name, language),
                media_type="application/text",
            )
        else:
            return StreamingResponse(
                azure_util.transcribe_with_push_stream(
                    file, audio_params, use_diarization=diarization, language=language
                ),
                media_type="application/text",
            )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"The processing of the audio file failed: {error}",
        )


# TODO: WORK IN PROGRESS
@transcribeRouter.websocket("/stream")
async def stream(websocket: WebSocket):
    try:
        await azure_util.test_websocket(websocket)
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="The processing of the audio file failed",
        )
