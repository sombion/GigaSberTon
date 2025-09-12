from langchain_gigachat import GigaChat
from config import settings


llm = GigaChat(
    model=settings.MODEL,
    credentials=settings.GIGACHAT_CREDENTIALS,
    scope=settings.SCOPE,
    verify_ssl_certs=False
)