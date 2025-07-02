import google.generativeai as genai
import re
import os
from .gemini_prompt import emotion_gemini_prompt, compliance_gemini_prompt
import json
from dotenv import load_dotenv
import ast


load_dotenv()
genai.configure(api_key=os.environ.get("LLM_API"))
model = genai.GenerativeModel("gemini-2.5-pro")


def load_conversation_json(file_path):
    """Load a JSON file and return messages list."""
    with open(file_path, "r") as f:
        data = json.load(f)
    return data["messages"]


def detect_emotion_from_llm(messages):
    customer_texts = [
        msg["text"] for msg in messages if msg["sender"].lower() == "customer"
    ]

    formatted_customer_texts = json.dumps(customer_texts, indent=2)

    emotion_prompt = emotion_gemini_prompt.format(
        customer_texts=formatted_customer_texts
    )
    response = model.generate_content(emotion_prompt)

    response_text = response.text.strip()
    if response_text.startswith("```python"):
        response_text = (
            response_text.replace("```python", "").replace("```", "").strip()
        )
    result = ast.literal_eval(response_text)

    return result



def detect_compliance_from_llm(messages):
    customer_texts = [msg["text"] for msg in messages]

    formatted_customer_texts = json.dumps(customer_texts, indent=2)

    compliance_prompt = compliance_gemini_prompt.format(
        customer_texts=formatted_customer_texts
    )
    response = model.generate_content(compliance_prompt)
    response_text = response.text.strip()
    if response_text.startswith("```python"):
        response_text = (
            response_text.replace("```python", "").replace("```", "").strip()
        )

    cleaned_output = response_text.replace("true", "True").replace("false", "False")
    result = ast.literal_eval(cleaned_output)
    return result

