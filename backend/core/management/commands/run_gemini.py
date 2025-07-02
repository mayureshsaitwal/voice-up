import google.generativeai as genai
import re
import os
from .gemini_prompt import emotion_gemini_prompt, compliance_gemini_prompt
import json
from dotenv import load_dotenv
import ast


load_dotenv()
genai.configure(api_key=os.environ.get("LLM_API"))
# print(os.environ.get("LLM_API"))
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

    # result = response.text.strip()
    # print(response.text.strip())
    response_text = response.text.strip()
    if response_text.startswith("```python"):
        response_text = (
            response_text.replace("```python", "").replace("```", "").strip()
        )
    result = ast.literal_eval(response_text)
    # print(result)

    # Always gives result with json backticks don't know why, so to clean it
    # clean_result = re.sub(r"^```json\n|```$", "", result.strip())

    return result
    # return clean_result


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
    # clean_result = re.sub(r"^```json\n|```$", "", result.strip())
    # return clean_result

    # response = model.generate_content(prompt)
    # result = response.text.strip().lower()
    # return result

    # import json as pyjson  # avoid shadowing
    #
    # formatted = pyjson.dumps(customer_texts, indent=2)
    #
    # prompt = system_prompt.format(customer_texts=formatted)
    #
    # print("📨 Sending to Gemini...\n")
    # # print(prompt)  # Optional: print the prompt you're sending
    #
    # response = model.generate_content(prompt)
    # result = response.text.strip().lower()
    # return result


# if __name__ == "__main__":
#     # Replace with your file path
#     file_path = r"./test.json"
#     messages = load_conversation_json(file_path)
#     emotion = detect_emotion_from_llm(messages)
#     print(f"\n✅ Final detected emotion: {emotion}")
