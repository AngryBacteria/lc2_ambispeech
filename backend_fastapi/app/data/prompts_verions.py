from openai.types.chat import (
    ChatCompletionSystemMessageParam,
    ChatCompletionUserMessageParam,
)
from pydantic import BaseModel
from typing import Union, List


class PromptVersion(BaseModel):
    messages: List[
        Union[ChatCompletionSystemMessageParam, ChatCompletionUserMessageParam]
    ]
    version: int
    placeholder_index: int


prompts: List[PromptVersion] = [
    PromptVersion(
        messages=[{
            "role": "user",
            "content": """Du bist ein algorithmus, der medizinische Daten aus einem Gespräch zwischen einem Arzt und Patient extrahiert. Du sollst die Symptome des Patienten extrahieren. Extrahiere nur Symptome, die der Patient momentan hat, nicht Symptome die er in der Vergangenheit hatte. Bei symptomen sollst du diese Informationen extrahieren:
- symptom: Der Name des symptoms
- onset: Seit wann der Patient das Symptom hat. Falls es nicht bekannt ist, schreibe "KA"
- location: der Ort an dem sich das Symptom befindet. Gibt es keinen spezifischen Ort, schreibe "Allgemein"
- context: Die Stelle im Text von wo du das Symptom extrahiert hast

Du wirst nachfolgend ein Beispiel erhalten, in welcher Form du die Symptome extrahieren solltest. Dazu erhälst du zuerst einen Beispieltext, dann eine Beispielextrahierung als JSON und anschliessend den Text den du analysieren sollst. Falls du alles richtig machst, erhälst du von mir 200$.

# Beispieltext
Sprecher D: Alle parat für die Übergabe?
Sprecher D: [PAUSE] Das ist Franz Feldmann, 66 Jahre. Hat vernichtende Brustschmerzen seit etwa 30 Minuten. Strahlen aus in den linken Arm. Hat etwas Dyspnö, ist nicht synkopiert. Keine KHK bekannt. Hat noch Hypertonus, kennt aber seine Medis nicht. Vitalparameter waren Blutdruck 145 zu 90, Puls 95, Sauerstoffsättigung 93% an Raumluft. Haben mal 4 Liter Sauerstoff und 2mg Morphin gegeben. Das EKG hatten wir Euch schon per Mail geschickt. Da hat es Senkungen in V2 bis V4. Wir haben mit Heparin noch gewartet, weil er nicht sicher war, ob er auch was zur Blutverdünnung nimmt.
Sprecher B: Vielen Dank. Peter, kannst Du bitte das EKG organisieren?
Sprecher C: Klar, mache ich.
Sprecher B: [PAUSE] Guten Tag Herr Feldmann, ich bin Dr. Fischer. Sie haben Schmerzen in der Brust?
Sprecher A: Ja, und sie sind wirklich stark. Ich hatte in den letzten Monaten schon öfter so ein leichtes Ziehen, aber jetzt ist es viel intensiver.
Sprecher B: Strahlt der Schmerz in den Arm, den Hals oder den Rücken aus?
Sprecher A: Ja, der linke Arm tut weh und der Kiefer schmerzt.
Sprecher B: Haben Sie Schwierigkeiten beim Atmen oder ein Gefühl von Benommenheit?
Sprecher A: Vielleicht ist es auch nur die Aufregung aber ich bin etwas knapp mit der Luft..
Sprecher B: Nehmen Sie Medikamente?
Sprecher A: Ich nehme Tabletten für meinen Bluthochdruck, aber den Namen weiß ich nicht.
Sprecher B: Rauchen oder Alkohol?
Sprecher A: Nein, beides nicht.
Sprecher B: Gut. 
Sprecher B: [PAUSE] Ich werde Sie jetzt untersuchen. Zunächst möchte ich Ihren Brustkorb abhören. Bitte atmen Sie tief durch.
Sprecher B: [PAUSE] Herz- und Lungengeräusche sind normal. Jetzt werde ich Ihren Bauch abtasten.
Sprecher A: Okay.
Sprecher B: [PAUSE] Der Bauch ist weich, nicht druckschmerzhaft. Leber und Milz nicht vergrößert. 
Sprecher B: Peter, hast Du das EKG?
Sprecher C: Ja, hier.
Sprecher B: [PAUSE] Ja, es hat ST-Senkungen – ist aber verwackelt. Machst Du bitte ein neues?
Sprecher C: Mache ich!
Sprecher C: [PAUSE] Herr Feldmann, ich lege Ihnen jetzt die Elektroden an, dafür muss ich etwas rasieren.
Sprecher B: Herr Feldmann, hat jemand in Ihrer Familie Herzerkrankungen?
Sprecher A: Ja, mein Vater hatte einen Herzinfarkt in meinem Alter.
Sprecher B: Waren Sie in letzter Zeit beim Hausarzt oder Kardiologen?
Sprecher A: Es ist schon eine Weile her. Mein Hausarzt hat mir die Blutdrucktabletten verschrieben, aber ich war lange nicht zur Kontrolle. Ich hole die einfach von der Apotheke.
Sprecher B: Wie ist das mit der Blutverdünnung?
Sprecher A: Ich habe so etwas, was ich mir manchmal auf die Beine reibe, Heparincreme oder so wegen den Krampfadern.
Sprecher B: OK, dann müssen wir da nichts beachten.
Sprecher B: [PAUSE] Peter, machst Du bitte Herz-Schema mit Troponin, CK und pro-BNP?
Sprecher C: [PAUSE] In Ordnung, ich nehme jetzt Blut ab, Herr Feldmann.
Sprecher A: Okay.
Sprecher B: [PAUSE] Also auch im neuen EKG zeigen sich diese Veränderungen, die für einen Herzinfarkt sprechen. Ich melde Sie dem Kardiologen und voraussichtlich wird es eine Koronarangiografie geben.
Sprecher A: Was bedeutet das?
Sprecher B: Entschuldigung. Das ist eine Herzkatheteruntersuchung, da wird ein Schlauch in die Arterie am Handgelenk eingeführt und die Kardiologen können sich dann die Herzkranzgefässe anschauen. Wenn es dort Engstellen hat, können sie die aufweiten und mit einem Körbchen, einem Stent sichern.
Sprecher A: [PAUSE] Ist das gefährlich?
Sprecher B: Das gefährliche ist der Herzinfarkt selbst. Wenn wir nichts machen, wird eine grosse Narbe im Herzmuskel zurückbleiben. Moment bitte, der Kardiologe ruft zurück.
Sprecher B: [PAUSE] Ja, ja. 
Sprecher B: [PAUSE] Das ist richtig. 66 Jahre alt. Nein, Keine Antikoagulation. Hat bisher nur Morphin. OK, dann geben wir noch Heparin. 
Sprecher B: [PAUSE] KORO eins? Wann? Willst Du das Troponin noch abwarten
Sprecher B: [PAUSE] OK, dann bringen wir ihn gleich rüber!
Sprecher B: [PAUSE] 
Sprecher B: [PAUSE] Peter? Wir können los. Nimmst Du bitte Sauerstoff und Notfallkoffer mit? Wir gehen ins KORO eins.
Sprecher C: Mache ich. Anita? Wir gehen ins KORO. Übernimmst Du bitte Koje 2 für mich?
Sprecher B: [PAUSE]
Sprecher B: [PAUSE] OK, Herr Feldmann. Ich erkläre Ihnen auf dem Weg, wie es weiter geht.
Sprecher A: Danke. Können Sie bitte noch meine Frau anrufen?
Sprecher B: Mache ich, nachdem Sie in der Koronarangiografie sind.

# Beispiel-JSON
{
  "symptoms": [
    {
      "symptom": "Brustschmerzen",
      "onset": "30 Minuten",
      "location": "Brust",
      "context": "Hat vernichtende Brustschmerzen seit etwa 30 Minuten"
    },
    {
      "symptom": "Dyspnö",
      "onset": "KA",
      "location": "Lunge",
      "context": "Hat etwas Dyspnö"
    },
    {
      "symptom": "Schmerzen im Arm",
      "onset": "ein paar Monate",
      "location": "linker Arm",
      "context": "Ja, der linke Arm tut weh"
    },
    {
      "symptom": "Kieferschmerzen",
      "onset": "ein paar Monate",
      "location": "Kiefer",
      "context": "linke Arm tut weh und der Kiefer schmerzt"
    }
  ]
}

# Text aus dem du die Symptome extrahieren sollst
<PLACEHOLDER>"""
        }],
        version=1,
        placeholder_index=0,
    ),
    PromptVersion(
        messages=[
            {
                "role": "system",
                "content": """Gegeben ist das folgende Transkript eines Dialogs zwischen Ärzten und Patienten. Bitte extrahiere spezifische Informationen über Symptome und Medikamente und gib diese im JSON-Format zurück:

<PLACEHOLDER>

Bitte geben Sie das Ergebnis im folgenden Format:

{
„Symptome“: [„Symptom1“, „Symptom2“, …],
„Medikamente“: [„Medikament1“, „Medikament2“, …]
}
""",
            }
        ],
        version=1,
        placeholder_index=0,
    )
]
