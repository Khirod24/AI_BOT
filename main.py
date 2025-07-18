from fastapi import FastAPI, Query ,Request
from pydantic import BaseModel
import os
import groq
from dotenv import load_dotenv
from fastapi.staticfiles import StaticFiles

load_dotenv()

client = groq.Groq(api_key=os.getenv("GROQ_API_KEY"))

app = FastAPI()

chat_history =[]
class ChatInput(BaseModel):
    question: str

# @app.get("/")
# async def read_root():
#     return {"message":"Welcome to the chatbot API!"}

@app.post("/api/chat/")
async def chat(input: ChatInput):
    try:
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": "You are a helpful assistant. Keep your answers under 100 words."},
                {"role": "user", "content": input.question}
            ],
            max_tokens=150
        )
        
        answer = response.choices[0].message.content

            # Save Q&A pair to history
        chat_history.append({
            "question": input.question,
            "answer": answer
        })

        return {"reply": answer}
    except Exception as e:
        return {"error": str(e)}


@app.get("/api/history/")
async def get_chat_history():
    return {"chat_history": chat_history}

app.mount("/", StaticFiles(directory="static", html=True), name="static")
