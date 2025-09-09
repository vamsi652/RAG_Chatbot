import os
from langchain_google_genai import ChatGoogleGenerativeAI
from config.config import GOOGLE_API_KEY

def get_chatgemini_model():
    """Initialize and return the Google Gemini chat model"""
    try:
        gemini_model = ChatGoogleGenerativeAI(
            api_key=GOOGLE_API_KEY,
            model="gemini-1.5-flash",  # Use the correct model name
        )
        return gemini_model
    except Exception as e:
        raise RuntimeError(f"Failed to initialize Gemini model: {str(e)}")
