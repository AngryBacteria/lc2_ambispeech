from app.utils.embedding_util import EmbeddingUtil

util = EmbeddingUtil()

res = util.search_functions(
    util.icd10, "Mir geht es nicht gut ich habe Bauchschmerzen im Darm"
)
print(res["V8"] + " -- " + res["V9"])
