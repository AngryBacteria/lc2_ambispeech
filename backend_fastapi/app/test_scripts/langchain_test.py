import asyncio
import json

from app.utils.langchain_util import LangchainUtil

with open("../data/lc2_data.json", 'r', encoding='utf-8') as file:
    medical_texts = json.load(file)

util = LangchainUtil()
transcript = medical_texts["files"][0]["transcript"]

res = asyncio.run(util.test("chat-open-ai", transcript))
print(res)
