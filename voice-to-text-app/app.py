
import os

import gradio as gr
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key=API_KEY) if API_KEY else None

# API models are used; no model weights are stored in this project.
LLM_MODEL = "openai/gpt-oss-20b"
STT_MODEL = "whisper-large-v3-turbo"



def respond(message, history):
    if not client:
        return "GROQ_API_KEY পাওয়া যায়নি। .env ফাইলটি পরীক্ষা করো।"

    # Gradio 6 multimodal input contains text and uploaded files.
    if isinstance(message, dict):
        text = (message.get("text") or "").strip()
        files = message.get("files") or []
    else:
        text = str(message or "").strip()
        files = []

    # Transcribe uploaded or recorded audio files.
    for item in files:
        if isinstance(item, dict):
            audio_path = item.get("path")
        else:
            audio_path = item

        if not audio_path or not os.path.isfile(audio_path):
            continue

        try:
            with open(audio_path, "rb") as audio_file:
                transcription = client.audio.transcriptions.create(
                    file=(
                        os.path.basename(audio_path),
                        audio_file.read(),
                    ),
                    model=STT_MODEL,
                    response_format="text",
                )

            voice_text = (
                transcription
                if isinstance(transcription, str)
                else transcription.text
            )
            voice_text = voice_text.strip()

            if voice_text:
                text = f"{text}\n\n{voice_text}".strip()

        except Exception as exc:
            return f"Voice transcription error: {exc}"

    if not text:
        return "একটি text message লেখো অথবা voice/audio পাঠাও।"

    try:
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a helpful AI assistant. "
                    "Understand the user's message and respond clearly. "
                    "Reply in the language the user uses."
                ),
            }
        ]

        # Include recent text conversation history.
        for item in (history or [])[-10:]:
            if not isinstance(item, dict):
                continue

            role = item.get("role")
            content = item.get("content")

            if role in ("user", "assistant") and isinstance(content, str):
                messages.append({"role": role, "content": content})

        messages.append({"role": "user", "content": text})

        result = client.chat.completions.create(
            model=LLM_MODEL,
            messages=messages,
            temperature=0.7,
        )

        return result.choices[0].message.content or "কোনো উত্তর পাওয়া যায়নি।"

    except Exception as exc:
        return f"LLM API error: {exc}"



demo = gr.ChatInterface(
    fn=respond,
    title="Text + Voice AI Assistant",
    description=(
        "Type a message, record your voice, or upload an audio file. "
        "Your voice will be transcribed and sent to the AI."
    ),
    multimodal=True,
        textbox=gr.MultimodalTextbox(
        placeholder="Write a message or record/upload audio...",
        sources=["microphone", "upload"],
        file_types=["audio"],
    ),
)

if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=int(os.getenv("PORT", "7860")),
    )
