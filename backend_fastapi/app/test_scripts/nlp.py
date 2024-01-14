from datetime import datetime

import requests

from app.data.data import audio_file_data


def main():
    # prepare the audio examples to test
    possible_examples_names = [
        "APPENDIZITIS_1_0.wav",
        "STROKE_1_0_sprecher_4363D135_BgndNoise.wav"
    ]
    examples_to_test = []
    for file in audio_file_data:
        if file.name in possible_examples_names:
            examples_to_test.append(file)

    # test the examples
    for file in examples_to_test:
        output = ""
        print(f"{20 * '-'} Testing file: {file.name} {20 * '-'}")
        output = output + f"{20 * '-'} Testing file: {file.name} {20 * '-'} \n"
        # printing truth
        print(f"{10 * '-'} Truth {10 * '-'}")
        output = output + f"{10 * '-'} Truth {10 * '-'} \n"
        for symptom in file.extraction.symptoms:
            print(symptom.icd10)
            output = output + symptom.icd10 + "\n"

        # printing hypothesis (embeddings)
        print(f"{10 * '-'} Hypothesis (embeddings) {10 * '-'}")
        output = output + f"{10 * '-'} Hypothesis (embeddings) {10 * '-'} \n"
        data = analyze_request(file.transcript, True, False)
        for symptom in data['symptoms']:
            print(f"{symptom['icd10']}   symptom = [{symptom['symptom']}] context = [{symptom['context']}]")
            output = output + f"{symptom['icd10']}   symptom = [{symptom['symptom']}] context = [{symptom['context']}]" + "\n"

        # printing hypothesis (direct-gpt)
        print(f"{10 * '-'} Hypothesis (direct-gpt) {10 * '-'}")
        output = output + f"{10 * '-'} Hypothesis (direct-gpt) {10 * '-'} \n"
        data = analyze_request(file.transcript, False, True)
        for symptom in data['symptoms']:
            print(f"{symptom['icd10']}   symptom = [{symptom['symptom']}] context = [{symptom['context']}]")
            output = output + f"{symptom['icd10']}   symptom = [{symptom['symptom']}] context = [{symptom['context']}]" + "\n"

        # printing hypothesis (anamnesis)
        print(f"{10 * '-'} Hypothesis (anamnesis) {10 * '-'}")
        output = output + f"{10 * '-'} Hypothesis (anamnesis) {10 * '-'} \n"
        print(data['anamnesis'])
        output = output + data['anamnesis'] + "\n"
        print("\n\n")
        output = output + "\n\n"

        now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        safe_file_name = f"output.txt [{file.name}] [{now}]".replace(" ", "_").replace(".", "-")
        with open(safe_file_name, "w") as f:
            f.write(output)


def analyze_request(text: str, use_embeddings: bool = True, do_anamnesis: bool = True):
    url = "http://127.0.0.1:8000/api/nlp/analyze"
    data = {
        "text": text,
        "use_embeddings": use_embeddings,
        "do_anamnesis": do_anamnesis,
    }
    response = requests.post(url, json=data)
    data = response.json()
    return data


main()
