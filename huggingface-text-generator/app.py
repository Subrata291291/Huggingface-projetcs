
import os

import gradio as gr
from dotenv import load_dotenv
from groq import Groq

# Load local environment variables if a .env file exists.
# On Render, GROQ_API_KEY is read from Environment Variables.
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_ID = "openai/gpt-oss-20b"


def generate_text(prompt):
    """Generate formatted text using the Groq Hosted API."""

    if not prompt or not prompt.strip():
        return "⚠️ Please enter a prompt."

    if not GROQ_API_KEY:
        return (
            "⚠️ **Configuration error:** `GROQ_API_KEY` is missing. "
            "Please configure it in your hosting provider's environment variables."
        )

    try:
        client = Groq(api_key=GROQ_API_KEY)

        response = client.chat.completions.create(
            model=MODEL_ID,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a helpful AI writing assistant. "
                        "Answer in the same language as the user's prompt. "
                        "Use proper Markdown formatting, including headings, "
                        "bold text, bullet points, numbered lists, and tables "
                        "when appropriate. Do not output HTML tags such as <br>. "
                        "Keep answers clear, useful, and well organized."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt.strip(),
                },
            ],
            max_completion_tokens=1000,
            reasoning_effort="low",
            reasoning_format="hidden",
        )

        answer = response.choices[0].message.content

        if answer and answer.strip():
            return answer.strip()

        return (
            "⚠️ The model returned an empty response. "
            "Please try again."
        )

    except Exception as error:
        # Log the error without exposing the API key.
        print(f"Groq API error: {type(error).__name__}: {error}")

        return (
            "❌ **Unable to generate a response.** "
            "Please try again later. If the problem continues, "
            "check the application logs, API key, model availability, "
            "and API rate limits."
        )


demo = gr.Interface(
    fn=generate_text,
    inputs=gr.Textbox(
        label="Enter Your Prompt",
        placeholder=(
            "For example: বাংলায় দুর্গাপুজোর ইতিহাস ও সংস্কৃতি লেখো।"
        ),
        lines=4,
    ),
    outputs=gr.Markdown(
        label="AI Response",
    ),
    title="AI Text Generator",
    description=(
        "Generate well-formatted text in Bengali, English, "
        "and other languages using Groq-powered AI."
    ),
    submit_btn="Generate Text",
    clear_btn="Clear",
    flagging_mode="never",
)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))

    demo.launch(
        server_name="0.0.0.0",
        server_port=port,
    )
