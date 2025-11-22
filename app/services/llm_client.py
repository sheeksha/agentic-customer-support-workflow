import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

load_dotenv()  # loads from .env

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


def get_llm():
    """
    Returns a configured ChatOpenAI instance.
    """
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY is not set in the environment.")

    llm = ChatOpenAI(
        model="gpt-4o-mini",  # or "gpt-4o" if you prefer
        temperature=0.2,
        openai_api_key=OPENAI_API_KEY,
    )
    return llm


def get_embeddings():
    """
    Returns an OpenAIEmbeddings instance.
    """
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY is not set in the environment.")

    return OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
