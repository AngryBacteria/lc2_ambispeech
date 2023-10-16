import time

import azure.cognitiveservices.speech as speechsdk
from app.utils.speech_util import SpeechUtil


def continuous_recognition():
    done = False
    sutil = SpeechUtil()
    audio_config = speechsdk.audio.AudioConfig(
        filename="X:\\Programming\\Web\\lc2_ambispeech\\backend_fastapi\\test.wav")
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=sutil.speech_config, audio_config=audio_config)

    def stop_cb(evt):
        print('CLOSING on {}'.format(evt))
        speech_recognizer.stop_continuous_recognition()
        nonlocal done
        done = True

    # speech_recognizer.recognizing.connect(lambda evt: print('RECOGNIZING: {}'.format(evt)))
    speech_recognizer.recognized.connect(lambda evt: print('RECOGNIZED: {}'.format(evt)))
    speech_recognizer.session_started.connect(lambda evt: print('SESSION STARTED: {}'.format(evt)))
    speech_recognizer.session_stopped.connect(lambda evt: print('SESSION STOPPED {}'.format(evt)))
    speech_recognizer.canceled.connect(lambda evt: print('CANCELED {}'.format(evt)))

    speech_recognizer.session_stopped.connect(stop_cb)
    speech_recognizer.canceled.connect(stop_cb)

    speech_recognizer.start_continuous_recognition()
    while not done:
        time.sleep(.5)


def main():
    continuous_recognition()


if __name__ == '__main__':
    main()
