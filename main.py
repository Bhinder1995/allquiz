from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
import os
import json
from dotenv import load_dotenv

# ----------------------------
# Load environment variables
# ----------------------------
load_dotenv()

# ----------------------------
# App init
# ----------------------------
app = FastAPI()

# ----------------------------
# CORS (Allow Netlify / frontend)
# ----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # restrict later if needed
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------
# Health check (IMPORTANT for Render)
# ----------------------------
@app.get("/")
def health():
    return {"status": "ok"}

# ----------------------------
# Gemini configuration
# ----------------------------
genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel("gemini-pro")

# ----------------------------
# Generate Quiz API
# ----------------------------
@app.post("/generate-quiz")
async def generate_quiz(data: dict = Body(...)):
    topic = data.get("topic", "general knowledge")

    prompt = f"""
Create ONE multiple choice quiz question on {topic}.

Return JSON ONLY in this exact format:
{{
  "question": "question text",
  "options": ["A", "B", "C", "D"],
  "answer": "correct option"
}}
"""

    try:
        response = model.generate_content(prompt)

        text = response.text.strip()

        # Remove markdown if Gemini adds it
        if text.startswith("```"):
            text = text.split("```")[1].strip()

        return json.loads(text)

    except Exception as e:
        return {
            "error": "Failed to generate quiz",
            "details": str(e)
        }
