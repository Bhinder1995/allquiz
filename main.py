from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
import os

app = FastAPI()

# Allow Netlify
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure Gemini
genai.configure(api_key=os.getenv("AIzaSyBJzF6GiDhofEZ5xXUpQzC7urYIf2vLt_U"))
model = genai.GenerativeModel("gemini-pro")

@app.post("/generate-quiz")
async def generate_quiz(data: dict):
    topic = data.get("topic", "general knowledge")

    prompt = f"""
    Create ONE multiple choice quiz question on {topic}.
    Return JSON only in this format:
    {{
      "question": "...",
      "options": ["A", "B", "C", "D"],
      "answer": "correct option"
    }}
    """

    response = model.generate_content(prompt)
    return response.text
