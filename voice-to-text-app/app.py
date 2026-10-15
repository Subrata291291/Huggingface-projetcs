
import os

import gradio as gr
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")
LLM_MODEL = "openai/gpt-oss-20b"
STT_MODEL = "whisper-large-v3-turbo"

client = Groq(api_key=API_KEY) if API_KEY else None


# ---------- Audio and message helpers ----------

def get_audio_path(item):
    if isinstance(item, str):
        return item

    if isinstance(item, dict):
        return item.get("path") or item.get("file")

    return None


def normalize_content(content):
    if isinstance(content, str):
        return content.strip()

    if isinstance(content, dict):
        text = content.get("text")
        return text.strip() if isinstance(text, str) else ""

    if isinstance(content, list):
        parts = []

        for item in content:
            if isinstance(item, str):
                parts.append(item)
            elif isinstance(item, dict):
                text = item.get("text")
                if isinstance(text, str):
                    parts.append(text)

        return "\n".join(parts).strip()

    return ""


# ---------- Chat and streaming ----------

def chat(message, history):
    history = list(history or [])

    if not client:
        history.append({
            "role": "assistant",
            "content": "GROQ_API_KEY পাওয়া যায়নি। Environment variables পরীক্ষা করো।",
        })
        yield {"text": "", "files": []}, history
        return

    if isinstance(message, dict):
        text = (message.get("text") or "").strip()
        files = message.get("files") or []
    else:
        text = str(message or "").strip()
        files = []

    transcripts = []

    # Transcribe microphone recordings and uploaded audio.
    for item in files:
        path = get_audio_path(item)

        if not path or not os.path.isfile(path):
            continue

        try:
            with open(path, "rb") as audio_file:
                result = client.audio.transcriptions.create(
                    file=(os.path.basename(path), audio_file.read()),
                    model=STT_MODEL,
                    response_format="text",
                )

            transcript = (
                result if isinstance(result, str) else result.text
            ).strip()

            if transcript:
                transcripts.append(transcript)

        except Exception as exc:
            history.append({
                "role": "assistant",
                "content": f"Voice transcription failed: {exc}",
            })
            yield {"text": "", "files": []}, history
            return

    # Display recognized speech as the user's message.
    user_text = "\n".join(
        part for part in [text, *transcripts] if part
    ).strip()

    if not user_text:
        history.append({
            "role": "assistant",
            "content": "একটি message লেখো অথবা voice পাঠাও।",
        })
        yield {"text": "", "files": []}, history
        return

    # Capture earlier conversation before adding the current turn.
    previous_turns = []

    for item in history:
        if not isinstance(item, dict):
            continue

        role = item.get("role")
        content = normalize_content(item.get("content"))

        if role in ("user", "assistant") and content:
            previous_turns.append({
                "role": role,
                "content": content,
            })

    # Add current user and assistant messages.
    history.append({"role": "user", "content": user_text})
    history.append({"role": "assistant", "content": ""})

    # Show the user's message immediately.
    yield {"text": "", "files": []}, history

    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful conversational AI assistant. "
                "Use previous messages to understand follow-up questions "
                "and references such as 'it', 'this', 'that', and "
                "'what about its career?'. Resolve these references using "
                "conversation history whenever reasonably possible. "
                "Do not ask users to repeat information already provided. "
                "If context is genuinely unclear, ask one focused question. "
                "Reply in the user's language."
            ),
        }
    ]

    # Include recent previous turns once.
    messages.extend(previous_turns[-20:])

    # Include the current user message once.
    messages.append({"role": "user", "content": user_text})

    try:
        stream = client.chat.completions.create(
            model=LLM_MODEL,
            messages=messages,
            temperature=0.7,
            stream=True,
        )

        answer = ""

        for chunk in stream:
            if not chunk.choices:
                continue

            delta = chunk.choices[0].delta.content

            if delta:
                answer += delta
                history[-1]["content"] = answer
                yield {"text": "", "files": []}, history

        if not answer:
            history[-1]["content"] = "AI কোনো উত্তর ফেরত দেয়নি।"
            yield {"text": "", "files": []}, history

    except Exception as exc:
        history[-1]["content"] = f"LLM API error: {exc}"
        yield {"text": "", "files": []}, history


# ---------- Dark theme and layout ----------

APP_CSS = """
:root {
    color-scheme: dark;
}

/* Keep the app within the browser viewport. */
html,
body {
    margin: 0 !important;
    min-height: 100% !important;
    scrollbar-color: #454b59 #0b0f19 !important;
    scrollbar-width: thin !important;
}

.gradio-container {
    min-height: 100vh !important;
    min-height: 100dvh !important;
}

/* Dark scrollbars in Chromium-based browsers. */
*::-webkit-scrollbar {
    width: 9px !important;
    height: 9px !important;
}

*::-webkit-scrollbar-track {
    background: #0b0f19 !important;
}

*::-webkit-scrollbar-thumb {
    background-color: #454b59 !important;
    border: 2px solid #0b0f19 !important;
    border-radius: 8px !important;
}

*::-webkit-scrollbar-thumb:hover {
    background-color: #626b7d !important;
}

/* Chat area: flexible height, with its own scrolling. */
#chatbot {
    min-height: 280px !important;
    scrollbar-color: #454b59 #0b0f19 !important;
    scrollbar-width: thin !important;
}

/* Keep the composer compact. */
#chat-input {
    margin-top: 4px !important;
    margin-bottom: 0 !important;
}

/* Hide Gradio's standard footer to remove the large bottom gap. */
footer {
    display: none !important;
}
"""


with gr.Blocks(
    fill_height=True,
    css=APP_CSS,
    theme=gr.themes.Soft(),
) as demo:

    gr.Markdown(
        """
        # 💬 Voice & Text AI Assistant

        Type a message or speak naturally. Your voice will be
        transcribed, displayed in the chat, and sent to the AI.
        """
    )

    chatbot = gr.Chatbot(
        label="Conversation",
        height=520,
        placeholder="Start a conversation using text or voice.",
        layout="bubble",
        elem_id="chatbot",
        scale=1,
        min_width=0,
    )

    textbox = gr.MultimodalTextbox(
        placeholder="Message the AI or record/upload audio...",
        sources=["microphone", "upload"],
        file_types=["audio"],
        file_count="multiple",
        show_label=False,
        submit_btn=True,
        stop_btn=True,
        elem_id="chat-input",
    )

    textbox.submit(
        fn=chat,
        inputs=[textbox, chatbot],
        outputs=[textbox, chatbot],
    )


if __name__ == "__main__":
    demo.queue().launch(
        server_name="0.0.0.0",
        server_port=int(os.getenv("PORT", "7860")),
    )
