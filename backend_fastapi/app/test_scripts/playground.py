from app.utils.general_util import clean_string

stri = """Guest-1: Alle parat für die Übergabe. Das ist Franz Feldmann 66 Jahre hat vernichtende Brustschmerzen, seit etwa 30 Minuten strahlen aus, in den linken Arm hat etwas dyspmö ist nicht synkopiert keine KHK bekannt, hat noch Hypertonus, kennt aber seine Medes nicht, vitalparameter waren Blutdruck, 145 zu 90, Puls, 95, Sauerstoffsättigung, 93% an Raumluft haben mal 4 Liter Sauerstoff und 2 Milligramm Morphin gegeben.
Guest-1: Das EKG hatten wir euch schon per Mail geschickt, da hat es Senkungen in V 2 bis v vierten. Wir haben mit Heparin noch gewartet, weil er nicht sicher war, ob er auch was zur Blutverdünnung nimmt.
Guest-1: Vielen dank Peter, kannst du bitte das EKD organisieren?
Guest-2: Klar, mache ich.
Guest-2: Guten Tag, Herr Feldmann. Ich bin Dr. Fischer, Sie haben Schmerzen in der Brust.
Guest-3: Ja, und Sie sind wirklich stark. Ich hatte in den letzten Monaten schon öfter so ein Leichtes ziehen, aber jetzt ist es viel intensiver.
Guest-2: Strahlt der Schmerz in den Arm, den Hals oder den Rücken aus?
Guest-3: Ja, der linke Arm tut weh und der Kiefer schmerzt.
Guest-2: Haben Sie Schwierigkeiten beim Atmen oder ein Gefühl von Benommenheit?
Guest-3: Vielleicht ist es auch nur die Aufregung, aber ich bin etwas knapp mit.
Guest-2: Der Luft nehmen Sie Medikamente.
Guest-3: Ich nehme Tabletten für meinen Bluthochdruck, aber den Namen weiß ich nicht.
Guest-2: Rauchen oder Alkohol?
Guest-3: Nein, beides nicht.
Guest-2: Gut, ich werde Sie jetzt untersuchen. Zunächst möchte ich Ihren Brustkorb abhören.
Guest-2: Atmen Sie tief durch. Herz und Lungengeräusche sind normal. Jetzt werde ich Ihren Bauch abtasten.
Guest-3: Okay.
Guest-2: Der Bauch ist weich, nicht druckschmerzhaft Leber und Melz nicht vergrößert. Peter, hast du das EKG?
Guest-3: Ja, hier.
Guest-2: Ja, es hat es dir Senkungen, ist aber verwackelt. Machst du bitte ein neues?
Guest-3: Mache ich, Herr Feldmann, ich lege Ihnen jetzt die Elektroden an, dafür muss ich etwas rasieren.
Guest-2: Herr Feldmann, hat jemand in ihrer Familie Herzerkrankungen?
Guest-3: Ja, mein Vater hatte einen Herzinfarkt in meinem Alter.
Guest-2: Waren sie in letzter Zeit beim Hausarzt oder Kardiologen?
Guest-3: Es ist schon eine Weile her. Mein Hausarzt hat mir die Blutdrucktabletten verschrieben, aber ich war lange nicht zur Kontrolle, ich hole die einfach von der Apotheke.
Guest-2: Wie ist das mit der Blutverdünnung?
Guest-3: Ich habe so etwas, was ich mir manchmal auf die Beine reibe, Heparin, Creme oder so, wegen den Krampfadern.
Guest-2: Ok, dann müssen wir da nichts beachten. Peter, machst du bitte herzschema Methode?
Guest-2: CK und pro BNP.
Guest-4: In Ordnung, ich nehme jetzt Blut ab, Herr Feldmann, okay.
Guest-2: Also auch im neuen EKG zeigen sich diese Veränderungen, die für einen Herzinfarkt sprechen. Ich melde Sie dem Kardiologen und voraussichtlich wird es eine Korona Angiografie geben.
Guest-3: Was bedeutet das?
Guest-2: Entschuldigung, das ist eine Herzkatheteruntersuchung, da wird ein Schlauch in die Arterie am Handgelenk eingeführt und die Kardiologen können sich dann die Herzkranzgefässer anschauen, wenn es dort engstellen hat, können sie die Aufweiten und mit einem Körbchen einem Stent sichern.
Guest-3: Ist das gefährlich?
Guest-2: Das gefährliche ist der Herzinfarkt. Selbst wenn wir nichts machen, wird eine große Narbe im Herzmuskel zurückbleiben. Moment, bitte, der Kardiologe ruft zurück, ja, ja, das ist richtig, 66 Jahre alt, Nein, keine Antikoagulation hat bisher nur morphyn okay, dann geben wir noch Heparin Koro 1 wann?
Guest-2: Willst du, dass Troponin noch abwarten? OK, dann bringen wir ihn gleich rüber.
Guest-2: Peter, Wir können los. Nimmst du bitte Sauerstoff und Notfallkoffer mit? Wir gehen ins Koro 1.
Guest-4: Mache ich Anita? Wir gehen ins Coro, übernimmst du bitte koje 2 für mich?
Guest-2: Okay Herr Feldmann, ich erkläre Ihnen auf dem Weg, wie es weitergeht.
Guest-3: Danke. Können Sie bitte noch meine Frau anrufen?
Guest-2: Mache ich, nachdem sie in der Koronarangiographie sind."""

print(clean_string(stri))