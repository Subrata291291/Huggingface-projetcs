
import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

MODEL_ID = "openai/gpt-oss-20b"


def generate_text(prompt: str) -> str:
    if not prompt or not prompt.strip():
        return "⚠️ Please enter a prompt before generating text."

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        return (
            "### Configuration Error\n\n"
            "`GROQ_API_KEY` is missing. Add it to your `.env` file "
            "or your Render Environment Variables."
        )

    try:
        client = Groq(api_key=api_key)

        response = client.chat.completions.create(
            model=MODEL_ID,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert AI writing assistant. "
                        "Answer in the same language as the user's prompt. "
                        "Write useful, accurate, well-structured content. "
                        "Use headings, paragraphs, bullet points, and "
                        "Markdown tables when appropriate. Follow the "
                        "user's requested length and format."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt.strip(),
                },
            ],
            max_completion_tokens=1800,
            reasoning_effort="low",
            reasoning_format="hidden",
        )

        answer = response.choices[0].message.content

        if answer and answer.strip():
            return answer.strip()

        return (
            "The model returned an empty response. "
            "Please try a shorter or more specific prompt."
        )

    except Exception as error:
        print(f"Groq API error: {type(error).__name__}: {error}")

        return (
            "### Unable to generate a response\n\n"
            "Check your API key, model availability, rate limits, "
            "and Render logs. Please try again."
        )
