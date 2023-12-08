import json


import requests

from app.utils.embedding_util import EmbeddingUtil


def test_analyze():
    user_input = """SANITÄTER: Hier ist Herr Meier. Er stellt sich wegen wiederkehrenden Kopfschmerzen sowie Schwindel und Inkontinenz vor. Auffällig ist eine vorher diagnostizierte Hydrozephalus, Shunt ist seit 2004 in situ.
ARZT: Danke für die Information. Hallo Herr Meier, mein Name ist Dr. Schmidt. Bitte erzählen Sie uns, wie es Ihnen heute geht.
PATIENT: Die Kopfschmerzen sind heute schlimm aufgetreten, hauptsächlich frontal und im Bereich des Shunts. Ich fühle mich beim Aufstehen schwindelig und habe Inkontinenz festgestellt, die seit Wochen besteht. 
ARZT: Notiert. Ich will einige Fragen zu Ihren Medikamenten stellen. Nehmen Sie Sequase ein?
PATIENT: Ja, jeden Morgen und jeden Abend eine 25mg Tablette.
ARZT: Und Relaxane?
PATIENT: Ja, auch das nehme ich einmal am Morgen und einmal am Abend ein.
ARZT: Gut, danke für die Information. Ich werde jetzt eine körperliche Untersuchung durchführen. Nun, Ihr Blutdruck liegt bei 43/100mmHg und Puls bei 94/min... Guter Hirnnervenstatus, keine Auffälligkeit bei der körperlichen Untersuchung. Ich werde jetzt Ihren Bauchbereich abklopfen...
PATIENT: Okay, verstehe.
ARZT: Der Bauch steht weich, Normale Darmgeräusche in allen Quadranten, keine Druck - oder Rüttelschmerzen.
Ich denke, wir sollten ein Labor bei Ihnen machen, um Ihre Werte zu analysieren.
PATIENT: Dauert das lange?
ARZT: Etwa eine Stunde. Schwester Anna, können Sie bitte Blut abnehmen?
PFLEGE: Ja, welches Profil?
ARZT: Ein Abdomenlabor, bitte.
PFLEGE: In Ordnung, ich werde das gleich erledigen.
ARZT: Ihre Laborwerte zeigen, dass der Glucose-Spiegel bei 4.86 mmol/L und der Blutdruck bei 43/100mmHg liegt. Es gibt keine Hinweise auf eine Infektion und Ihre Werte scheinen relativ normal zu sein. Es gibt Anzeichen einer asymptomatischen Bakteriurie, wahrscheinlich in Zusammenhang mit Ihrer Inkontinenz.
PATIENT: Heißt das, ich muss nicht operiert werden?
ARZT: Nicht sofort. Ihr Shunt ist zwar länger im Einsatz, aber er wird wahrscheinlich bis Januar funktionstüchtig bleiben. Wir haben bereits einen Termin bei einem Neurochirurgen für Sie diese Woche geplant, um das weiter zu besprechen.
PATIENT: Und was ist mit meinen Kopfschmerzen und dem Schwindel?
ARZT: Diese Symptome scheinen mit Ihrem Hydrozephalus zusammenzuhängen. Wir müssen die Situation überwachen und geeignete Schritte einleiten, wenn sich Ihre Symptome verschlimmern. Und wenn Sie Unterbauchschmerzen, Dysurie oder Fieber bekommen, müssen Sie unverzüglich wieder zu uns kommen.
PATIENT: In Ordnung, danke, Dr. Schmidt. 
ARZT: Bitte, Herr Meier. Mein Team und ich sind hier, um Ihnen zu helfen. Wir halten Sie auf dem Laufenden."""

    body = {"text": user_input, "service": "openai"}
    json_data = json.dumps(body)
    response = requests.post(
        "http://127.0.0.1:8000/api/nlp/analyze",
        data=json_data,
        headers={"Content-Type": "application/json"},
    )
    print(response.json())


def test_embeddings():
    embed_util = EmbeddingUtil(
        csv_folder_path="X:/Programming/Web/lc2_ambispeech/backend_fastapi/app/data/catalogs"
    )
    data = embed_util.search(embed_util.icd10_symptoms, "Kopfschmerzen")
    print(data)
