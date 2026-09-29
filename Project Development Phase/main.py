import os
import json
import re

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

from fastapi import FastAPI, Request 
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv

import google.generativeai as genai


# =========================================================
# LOAD GEMINI API KEY
# =========================================================

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    print("WARNING: GEMINI_API_KEY is missing in .env")

genai.configure(api_key=GEMINI_API_KEY)

local_model_name = "MBZUAI/LaMini-Flan-T5-783M"

tokenizer = AutoTokenizer.from_pretrained(local_model_name)
local_model = AutoModelForSeq2SeqLM.from_pretrained(local_model_name)

# Gemini model
model = genai.GenerativeModel("gemini-3.5-flash-lite")


# =========================================================
# FASTAPI APPLICATION
# =========================================================

app = FastAPI(
    title="EduGenie - Google Gemini Powered Learning Assistant",
    description="AI-powered educational assistant",
    version="1.0"
)

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static/CSS"), name="static")

# =========================================================
# HOME PAGE
# =========================================================

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):

   return templates.TemplateResponse(
    request=request,
    name="index.html",
    context={}
)


# =========================================================
# Q&A MODULE
# =========================================================


@app.post("/qa")
async def question_answer(request: Request):

    data = await request.json()

    question = data.get("question", "").strip()

    if not question:
        return JSONResponse(
            content={
                "error": "Please enter a question."
            },
            status_code=400
        )

    prompt = f"""
Answer the following question in simple and clear language.

Question:
{question}

Give a concise educational answer suitable for a student.
"""

    try:

        response = model.generate_content(prompt)

        return {
            "answer": response.text
        }

    except Exception as e:

        return {
            "error": str(e)
        }

# =========================================================
# EXPLANATION MODULE
# =========================================================

@app.post("/explain")
async def explain_topic(request: Request):

    data = await request.json()

    topic = data.get("topic", "").strip()

    if not topic:

        return JSONResponse(
            content={
                "error": "Please enter a topic."
            },
            status_code=400
        )

    prompt = f"""
Explain the following topic in very simple language.

Topic:
{topic}

Requirements:

1. Give a simple definition.
2. Explain the main idea.
3. Give an example.
4. Keep it suitable for students.
5. Avoid unnecessarily difficult words.
"""

    try:

        inputs = tokenizer(
            prompt,
            return_tensors="pt",
            truncation=True
        )

        outputs = local_model.generate(
            **inputs,
            max_length=300,
            num_beams=4,
            early_stopping=True
        )

        explanation = tokenizer.decode(
            outputs[0],
            skip_special_tokens=True
        )

        return {
            "explanation": explanation
        }

    except Exception as e:

        return {
            "error": str(e)
        }

# =========================================================
# SUMMARY MODULE
# =========================================================

@app.post("/summarize")
async def summarize_text(request: Request):

    data = await request.json()

    text = data.get("text", "").strip()

    if not text:

        return JSONResponse(
            content={
                "error": "Please enter text to summarize."
            },
            status_code=400
        )

    prompt = f"""
Summarize the following educational text.

Make the summary:

- Short
- Clear
- Easy to understand
- Focused on important points

Text:

{text}
"""

    try:

        inputs = tokenizer(
            prompt,
            return_tensors="pt",
            truncation=True,
            max_length=512
        )

        outputs = local_model.generate(
            **inputs,
            max_length=150,
            num_beams=4,
            early_stopping=True
        )

        summary = tokenizer.decode(
            outputs[0],
            skip_special_tokens=True
        )

        return {
            "summary": summary
        }

    except Exception as e:

        return {
            "error": f"Summarization error: {str(e)}"
        }


# =========================================================
# QUIZ MODULE
# =========================================================

def clean_json_response(text):

    text = text.strip()

    text = re.sub(
        r"```json",
        "",
        text,
        flags=re.IGNORECASE
    )

    text = text.replace("```", "")

    # Fix invalid backslash escapes returned by the AI
    text = re.sub(
        r'\\(?!["\\/bfnrtu])',
        r'\\\\',
        text
    )

    return text.strip()

@app.post("/quiz")
async def generate_quiz(request: Request):

    data = await request.json()

    topic = data.get("topic", "").strip()

    if not topic:

        return JSONResponse(
            content={
                "error": "Please enter a topic."
            },
            status_code=400
        )

    prompt = f"""
You are an educational quiz generator.

Create exactly 3 multiple-choice questions about:

{topic}

Each question must contain:

- question
- options
- answer

Each question must have exactly 4 options.

The answer must match one of the four options.

Return ONLY valid JSON.

Use this format:

[
    {{
        "question": "Question 1",
        "options": [
            "Option A",
            "Option B",
            "Option C",
            "Option D"
        ],
        "answer": "Option A"
    }}
]
"""

    try:

        response = model.generate_content(prompt)

        cleaned = clean_json_response(response.text)

        quiz = json.loads(cleaned)

        return {"quiz": quiz}

    except Exception as e:

        return {"error": f"Quiz generation error: {str(e)}"}

# =========================================================
# LEARNING PATH MODULE
# =========================================================

@app.post("/learn/recommendations")
async def learning_recommendations(request: Request):

    data = await request.json()

    topic = data.get("topic", "").strip()

    if not topic:

        return JSONResponse(
            content={
                "error": "Please enter a topic."
            },
            status_code=400
        )

    prompt = f"""
You are an AI learning assistant.

Create a personalized learning path for:

{topic}

Organize it into:

1. Beginner Level
2. Intermediate Level
3. Advanced Level

For each level include:

- Important concepts
- What to learn first
- Practical suggestions
- Useful learning resources

Give the learning path in a clear step-by-step format.
"""

    try:

        response = model.generate_content(prompt)

        return {
            "recommendation": response.text
        }

    except Exception as e:

        return {
            "error": str(e)
        } 