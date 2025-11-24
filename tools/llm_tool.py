from langchain.tools import tool
#from google import genai
import google.genai as genai

import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
print("Loaded Gemini Key:", api_key)

# Create client
client = genai.Client(api_key=api_key)


@tool
def llm_answer(query: str, web_results: str) -> str:
    """
    Final LLM answer using Gemini 2.5 Flash.
    """

    prompt = f"""
You are an intelligent AI assistant.

USER QUERY:
{query}

WEB SEARCH RESULTS:
{web_results}

Your job:
- Combine both.
- Be factual and precise.
- If results don't answer, politely say so.
- Keep it short.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text.strip()
