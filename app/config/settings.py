from dotenv import load_dotenv
import os
load_dotenv()

class Settings:
    OPENAI_API_KEY=os.getenv('OPENAI_API_KEY')
    TAVILY_API_KEY=os.getenv('TAVILY_API_KEY')

    ALLOWED_MODEL_NAMES = [
    "gpt-4.1-2025-04-14",
    "gpt-4.1-mini-2025-04-14",
    ]


settings=Settings()

