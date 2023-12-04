from app.utils.embedding_util import EmbeddingUtil

util = EmbeddingUtil()

res = util.search(util.icd10_symptoms, "Ja, der linke Arm tut weh", n=20)
print(res["V8"] + " -- " + res["V9"])
