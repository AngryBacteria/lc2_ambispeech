from app.utils.general_util import clean_string

stri = """SPRECHER D:Übergabe von Herrn X. Nach Autounfall mit niedriger Geschwindigkeit. Patient war Beifahrer und nicht angeschnallt. Kopfanprall wahrscheinlich. Ansprechbar und erinnert sich an das Ereignis. Keine sichtbaren Verletzungen. RR 86/52mmHg, HF 99/ min.

SPRECHER B:Danke für die Übergabe. Guten Abend, Herr X. Mein Name ist Dr. Schwarz. Wir untersuchen Sie jetzt und schauen uns Ihre Verletzungen genau an.

SPRECHER A:Guten Abend, Doktor. Ich habe einen ziemlichen Schrecken bekommen.

SPRECHER B:Das kann ich mir vorstellen. Gibt es Medikamente, die Sie regelmäßig einnehmen?

SPRECHER A:Nein, keine.

SPRECHER B:Gut. Ich werde nun Ihre Atemwege, Ihren Hals und Ihre Pulsadern überprüfen...Alles sieht gut aus, keine Atemwegsverlegung, keine gestauten Halsvenen, keine Trachealverlagerung. Nun überprüfe ich Ihren Thorax... Kein Hautemphysem, gleichmäßig belüftet, stabil, keine Anhaltspunkte für Spannungs- oder Hämato-Pneumothorax. Sauerstoffsättigung bei 100%.

SPRECHER C:Ich nehme währenddessen Blut ab für Laboruntersuchungen.

SPRECHER A:Was wird im Labor untersucht?

SPRECHER B:Wir kontrollieren Ihre Blutwerte um sicherzugehen, dass keine inneren Verletzungen vorliegen.

SPRECHER B:(Zum Patienten gewandt) Ihren Bauch, Ihr Becken und Ihre Pulse an den Arterien überprüfe ich nun... alles unauffällig. Ihre Pupillen sind mittelweit und gleich groß, Ihre Lichtreaktion ist vorhanden.

SPRECHER B:Ich untersuche jetzt Ihren Rücken... Druckempfindlichkeit über den Fortsätzen der Hals- und oberen Brustwirbelsäule. Ich erlasse jetzt ein Schädel-CT, um sicherzugehen, dass keine Blutungen oder Brüche bestehen.

SPRECHER A:Das klingt ernst. Ist das nötig?

SPRECHER B:Ja, wir müssen sicherstellen, dass bei Ihrem Unfall keine inneren Verletzungen entstanden sind.

(Nach der CT-Untersuchung...)

SPRECHER B:Herr X, das CT zeigt keine Blutungen oder Frakturen. Ihre Gefäße sind ebenfalls unauffällig. Wir werden Sie weiterhin beobachten und Ihre Schmerzen behandeln. Ihre Frau kann Sie später mit nach Hause nehmen.

SPRECHER A:Was mache ich daheim? Wann kann ich wieder arbeiten?

SPRECHER B:Sie sollten sich auf jeden Fall eine Woche lang schonen und körperliche Anstrengung vermeiden. Sollten die Kopfschmerzen oder Übelkeit auftreten oder die Nackenschmerzen andauern, kommen Sie bitte sofort zurück ins Krankenhaus.

SPRECHER A:Verstanden, danke Doktor. 

SPRECHER B:Gern geschehen, Herr X. Wir sind da, wenn Sie uns brauchen."""

print(clean_string(stri))
