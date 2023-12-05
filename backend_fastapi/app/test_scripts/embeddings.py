from app.utils.embedding_util import EmbeddingUtil

util = EmbeddingUtil()

res = util.search(util.icd10_symptoms, "Übelkeit", n=20)
print(res["V8"] + " -- " + res["V9"])
