import asyncio

from app.utils.langchain_util import LangchainUtil
from app.data import transcripts

util = LangchainUtil()
transcript = transcripts.transcript_appendizitis

res = asyncio.run(util.test("chat-open-ai", transcript))
print(res)
