import requests

from app.data.data import audio_file_data


def main():
    # prepare the audio examples to test
    possible_examples_names = [
        "APPENDIZITIS_1_0.wav",

    ]
    examples_to_test = []
    for file in audio_file_data:
        if file.name in possible_examples_names:
            examples_to_test.append(file)

    # test the examples
    for file in examples_to_test:
        print(f"{20 * '-'} Testing file: {file.name} {20 * '-'}")
        # printing truth
        print(f"{10 * '-'} Truth {10 * '-'}")
        for symptom in file.extraction.symptoms:
            print(symptom.icd10)
        # printing hypothesis (icd10)
        print(f"{10 * '-'} Hypothesis (icd10) {10 * '-'}")
        data = analyze_request(file.transcript)
        for symptom in data['symptoms']:
            print(symptom['icd10'])
        # printing hypothesis (anamnesis)
        print(f"{10 * '-'} Hypothesis (anamnesis) {10 * '-'}")
        print(data['anamnesis'])
        print("\n\n")


def analyze_request(text: str):
    url = "http://127.0.0.1:8000/api/nlp/analyze"
    data = {
        "text": text
    }
    response = requests.post(url, json=data)
    data = response.json()
    return data


main()
