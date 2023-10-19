import wave

from fastapi import APIRouter, UploadFile, HTTPException, WebSocket
from starlette.responses import StreamingResponse

from app.utils.azure_util import AzureUtil

transcribeRouter = APIRouter(
    prefix="/api/transcribe",
    tags=["transcribe"],
)

azure_util = AzureUtil()


@transcribeRouter.post("/file")
def post_file(file: UploadFile):
    # validate if the file is a valid wav
    try:
        file.file.seek(0)
        with wave.open(file.file, "rb") as audio_file:
            audio_params = audio_file.getparams()
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Audio file was not in the correct format. Please provide an uncompressed WAV file.",
        )

    # try to transcribe the wav
    try:
        # TODO: return all recognizing events not only recognized
        file.file.seek(0)
        return StreamingResponse(
            azure_util.speech_recognition_with_push_stream(file, audio_params),
            media_type="text/event-stream",
        )
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="The processing of the audio file failed",
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
