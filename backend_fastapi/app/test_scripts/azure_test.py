from app.utils.general_util import print_attributes
from app.utils.speech_util import SpeechUtil


def main():
    sutil = SpeechUtil()
    result = sutil.file_s2t("X:\\Programming\\Web\\lc2_ambispeech\\backend_fastapi\\test.wav")
    print_attributes(result)


if __name__ == '__main__':
    main()
