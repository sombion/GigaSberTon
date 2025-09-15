from langchain_core.messages import HumanMessage
from fastapi import FastAPI
from config import router
from consumer import consumer_text

app = FastAPI()

app.include_router(router)