
import os

import gradio as gr
from dotenv import load_dotenv
from groq import Groq

# Load environment variables from the .env file
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

MODEL_ID = "openai/gpt-oss-120b"


def generate_text(prompt):
    """Generate text using the Groq Hosted API."""

    if not prompt or not prompt.strip():
        return "Please enter a prompt."

    if not GROQ_API_KEY:
        return (
            "Configuration error: GROQ_API_KEY is missing. "
            "Please check your .env file."
        )

    try:
        client = Groq(api_key=GROQ_API_KEY)

        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {
                    "role": "user",
                    "content": (
                        "Answer in the same language as the prompt. "
                        "Write a short story in Bengali about a tiger "
                        "in the Sundarbans, within 100 words."
                        if prompt.strip().lower().startswith("write a short story")
                        else prompt
                    ),
                },
            ],
            max_completion_tokens=500,
            reasoning_effort="low",
            reasoning_format="hidden",
        )

        answer = response.choices[0].message.content

        print("Finish reason:", response.choices[0].finish_reason)
        print("Response content:", repr(answer))

        if answer and answer.strip():
            return answer

        return (
            "The model returned an empty final answer. "
            "Check the terminal output for debugging details."
        )

    except Exception as error:
        # Avoid printing or exposing the API key.
        print(
            f"Groq API request failed: "
            f"{type(error).__name__}: {error}"
        )

        return (
            "Unable to generate a response. "
            "Please check the terminal for the error details, "
            "your API key, model availability, and rate limits."
        )


demo = gr.Interface(
    fn=generate_text,
    inputs=gr.Textbox(
        label="Enter Your Prompt",
        placeholder="For example: Write a short story about a tiger.",
        lines=4,
    ),
    outputs=gr.Textbox(
        label="AI Response",
        lines=10,
    ),
    title="My First AI Text Generator",
    description=(
        "Generate text using a hosted AI model powered by Groq."
    ),
    submit_btn="Generate Text",
    clear_btn="Clear",
)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    demo.launch(
        server_name="0.0.0.0",
        server_port=port
    )
