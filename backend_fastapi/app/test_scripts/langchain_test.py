from app.data.data import LLMService
from app.utils.langchain_util import LangchainUtil

langchain_util = LangchainUtil()

hello = langchain_util.hello_chat_completion(LLMService.OPENAI)

print(hello)

# hello2 = langchain_util.chat_completion(LLMService.OPENAI, "Hello World")
# print(hello2)
