from __future__ import annotations

import azure.cognitiveservices.speech as speechsdk


def conversation_transcription_from_microphone():
    """transcribes a conversation"""
    # Creates speech configuration with subscription information
    speech_config = speechsdk.SpeechConfig(
        subscription="d1f5b3506b3446ef9dd033b2046daae2",
        region="switzerlandnorth",
        speech_recognition_language="de-CH",
    )
    transcriber = speechsdk.transcription.ConversationTranscriber(speech_config)

    done = False

    def stop_cb(evt: speechsdk.SessionEventArgs):
        """callback that signals to stop continuous transcription upon receiving an event `evt`"""
        print("CLOSING {}".format(evt))
        nonlocal done
        done = True

    # Subscribe to the events fired by the conversation transcriber
    transcriber.transcribed.connect(lambda evt: print("TRANSCRIBED: {}".format(evt)))
    transcriber.session_started.connect(
        lambda evt: print("SESSION STARTED: {}".format(evt))
    )
    transcriber.session_stopped.connect(
        lambda evt: print("SESSION STOPPED {}".format(evt))
    )
    transcriber.canceled.connect(lambda evt: print("CANCELED {}".format(evt)))
    # stop continuous transcription on either session stopped or canceled events
    transcriber.session_stopped.connect(stop_cb)
    transcriber.canceled.connect(stop_cb)

    transcriber.start_transcribing_async()

    while not done:
        # No real sample parallel work to do on this thread, so just wait for user to type stop.
        # Can't exit function or transcriber will go out of scope and be destroyed while running.
        print('type "stop" then enter when done')
        stop = input()
        if stop.lower() == "stop":
            print("Stopping async recognition.")
            transcriber.stop_transcribing_async()
            break


conversation_transcription_from_microphone()
