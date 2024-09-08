import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("API_KEY")
genai.configure(api_key=api_key)


def get_message(name, prompt):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        chat = model.start_chat(
            history=[
                {"role": "user", "parts": f"You are my chat bot. my name is {name}"},
                {"role": "model", "parts": "I'll help in any way i can."},
            ]
        )
        response = chat.send_message(prompt)
        return response.text
    except Exception as e:
        print("Something went wrong", e)
