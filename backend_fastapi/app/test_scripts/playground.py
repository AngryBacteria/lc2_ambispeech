from app.model.references import medical_texts
from app.utils.general_util import clean_string

for text in medical_texts["files"]:
    print(clean_string(text["transcript"]))
