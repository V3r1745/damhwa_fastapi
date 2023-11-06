from fastapi import FastAPI
from dotenv import load_dotenv
import os
import uvicorn
import openai
from pydantic import BaseModel
from typing import List, Dict, Union
from fastapi.middleware.cors import CORSMiddleware

class Chat(BaseModel):
  chat: List

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

load_dotenv()
openai.api_key = os.getenv("TOKEN")

@app.get("/")
def index():
  return {"Hello": "FastAPI"}

@app.post("/chat")
async def chat_gpt(body: Chat):
  print(dict(body).get("chat"))
  messages = [{
      "role": "system",
      "content": "너는 인공지능 도우미 '초록여우'야"
  }, {
      "role": "system",
      "content": "너는 환경을 중시하는 봇이야"
  }, {
      "role": "system",
      "content": "너는 모든 대답을 한글로 해주는 것이 좋아"
  }, {
      "role": "system",
      "content": "대답은 최대한 짧게 해줘"
  }, {
      "role": "system",
      "content": "답변을 할 때 '인공지능으로서'와 같은 딱딱하고 '감정'이라는 것이 없는 것 처럼 대답하지마"
  }]
  messages.extend(map(lambda v: {"role": "user" if v.get("user") else "assistant", "content": v.get("chat")}, dict(body).get("chat")))
  completion = openai.ChatCompletion.create(model = "gpt-4", messages = messages)
  print(completion.choices[0].get("message").get("content").strip())
  return {"result": completion.choices[0].get("message").get("content").strip()}

if __name__ == "__main__":
  uvicorn.run("main:app", host = "0.0.0.0", port = int(os.getenv("PORT")), reload = "True")
