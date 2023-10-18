from fastapi import APIRouter, UploadFile, HTTPException
from starlette.responses import StreamingResponse

from app.utils.azure_util import AzureUtil
import wave

transcribeRouter = APIRouter(
    prefix="/api/transcribe",
    tags=["transcribe"],
)

azure_util = AzureUtil()


@transcribeRouter.post("/file")
def post_file(file: UploadFile):
    try:
        file.file.seek(0)
        with wave.open(file.file, "rb") as audio_file:
            audio_params = audio_file.getparams()
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Audio file was not in the correct format. Please provide an uncompressed WAV file.",
        )

    # TODO return all recognizing events not only recognized
    file.file.seek(0)
    return StreamingResponse(
        azure_util.speech_recognition_with_push_stream(file, audio_params),
        media_type="text/event-stream",
    )
    # return {"size": file.size, "name": file.filename, "content_type": file.content_type, "wav": audio_params}
