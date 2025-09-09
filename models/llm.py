import os
from langchain_google_genai import ChatGoogleGenerativeAI
from config.config import GOOGLE_API_KEY

def get_chatgemini_model():
    try:
        gemini_model = ChatGoogleGenerativeAI(
            api_key=GOOGLE_API_KEY,
            model="gemini-1.5-flash",
        )
        return gemini_model
    except Exception as e:
        raise RuntimeError(f"Failed to initialize Gemini model: {str(e)}")
