import wave
from enum import Enum

from fastapi import APIRouter, UploadFile, HTTPException
from starlette.responses import StreamingResponse

from app.data.data import AzureLanguageCode
from app.utils.azure_util import AzureUtil
from app.utils.whisper_util import WhisperUtil

transcribeRouter = APIRouter(
    prefix="/api/transcribe",
    tags=["transcribe"],
)

azure_util = AzureUtil()
whisper_util = WhisperUtil()


class TranscribeService(str, Enum):
    WHISPER = "whisper"
    AZURE = "azure"


# todo: whisper not async, problem? If azure is non-async it does not stop on client abort.
@transcribeRouter.post("/file/{service}")
async def post_file(
    file: UploadFile,
    service: TranscribeService,
    diarization: bool = False,
    language: AzureLanguageCode = AzureLanguageCode.DE_CH,
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
        if service == TranscribeService.WHISPER:
            data = await file.read()
            await file.close()
            return StreamingResponse(
                whisper_util.transcribe(data),
                media_type="application/text",
            )
        else:
            data = await file.read()
            await file.close()
            return StreamingResponse(
                azure_util.transcribe_with_push_stream(
                    data, audio_params, use_diarization=diarization, language=language
                ),
                media_type="application/text",
            )

    except Exception as error:
        await file.close()
        raise HTTPException(
            status_code=500,
            detail=f"The processing of the audio file failed: {error}",
        )
