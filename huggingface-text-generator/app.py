
import os

import gradio as gr
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_ID = "openai/gpt-oss-20b"


# -------------------- AI GENERATION --------------------

def generate_text(prompt):
    if not prompt or not prompt.strip():
        return "✍️ Please enter a prompt to get started."

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        return (
            "⚠️ **Configuration Error**\n\n"
            "The API key is missing. Please configure "
            "`GROQ_API_KEY` in your hosting environment."
        )

    try:
        client = Groq(api_key=api_key)

        response = client.chat.completions.create(
            model=MODEL_ID,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a premium AI writing assistant. "
                        "Answer in the same language as the user. "
                        "Support Bengali, English, and other languages. "
                        "Use clean Markdown formatting with headings, "
                        "bold text, lists, and tables when useful. "
                        "Never output HTML tags. Follow the user's "
                        "requested topic, length, tone, and format."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt.strip(),
                },
            ],
            max_completion_tokens=1500,
            reasoning_effort="low",
            reasoning_format="hidden",
        )

        answer = response.choices[0].message.content

        if answer and answer.strip():
            return answer.strip()

        return "The model returned an empty response. Please try again."

    except Exception as error:
        print(f"Groq API error: {type(error).__name__}: {error}")

        return (
            "### ⚠️ Generation failed\n\n"
            "Please try again. If the issue continues, check your "
            "Groq API key, model availability, usage limits, and "
            "the application logs."
        )


# -------------------- PREMIUM CSS --------------------

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
    --bg: #090b14;
    --panel: #111522;
    --border: rgba(255,255,255,0.09);
    --muted: #929bb2;
    --accent: #9b87ff;
}

.gradio-container {
    max-width: 1440px !important;
    margin: auto !important;
    background:
        radial-gradient(ellipse at 15% 0%, rgba(101,72,220,0.15), transparent 38%),
        radial-gradient(ellipse at 90% 12%, rgba(44,125,255,0.10), transparent 32%),
        var(--bg) !important;
    color: #f5f6ff !important;
    font-family: 'Inter', sans-serif !important;
}

body {
    background: var(--bg) !important;
}

#app-shell {
    max-width: 1220px;
    margin: 0 auto;
    padding: 18px 22px 30px;
}

.topbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 14px;
    padding: 15px 20px;
    margin-bottom: 48px;
    background: rgba(17,21,34,0.78);
    border: 1px solid var(--border);
    border-radius: 18px;
    backdrop-filter: blur(18px);
}

.brand {
    display: flex;
    align-items: center;
    gap: 12px;
    font-weight: 800;
    letter-spacing: -0.5px;
    font-size: 18px;
}

.brand-icon {
    display: grid;
    place-items: center;
    width: 42px;
    height: 42px;
    border-radius: 13px;
    background: linear-gradient(135deg, #9d7bff, #536dfe);
    box-shadow: 0 5px 25px rgba(111,87,255,0.3);
    font-size: 22px;
}

.brand-sub {
    display: block;
    margin-top: 3px;
    font-size: 11px;
    font-weight: 500;
    color: var(--muted);
    letter-spacing: 0;
}

.status-pill {
    padding: 8px 12px;
    border: 1px solid rgba(77,222,155,0.22);
    border-radius: 999px;
    color: #83e6b5;
    background: rgba(77,222,155,0.07);
    font-size: 12px;
    white-space: nowrap;
}

.hero {
    max-width: 850px;
    margin: 0 auto 38px;
    text-align: center;
}

.eyebrow {
    display: inline-block;
    padding: 8px 13px;
    margin-bottom: 18px;
    border: 1px solid rgba(157,123,255,0.3);
    border-radius: 999px;
    color: #c5b6ff;
    background: rgba(157,123,255,0.08);
    font-size: 12px;
    font-weight: 600;
}

.hero h1 {
    margin: 0 0 16px;
    font-size: clamp(34px, 5vw, 58px);
    line-height: 1.12;
    letter-spacing: -2.5px;
    font-weight: 800;
    color: #ffffff;
}

.gradient-text {
    background: linear-gradient(100deg, #b8a5ff, #79aaff, #e1a9ff);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
}

.hero p {
    max-width: 650px;
    margin: 0 auto;
    color: #a4acc0;
    font-size: 15px;
    line-height: 1.8;
}

.feature-row {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 10px;
    margin-top: 22px;
}

.feature {
    padding: 8px 12px;
    border-radius: 10px;
    border: 1px solid var(--border);
    background: rgba(255,255,255,0.025);
    color: #c6cce0;
    font-size: 12px;
}

.panel {
    background: linear-gradient(
        145deg,
        rgba(21,26,43,0.97),
        rgba(14,17,29,0.97)
    ) !important;
    border: 1px solid var(--border) !important;
    border-radius: 20px !important;
    padding: 24px !important;
    box-shadow: 0 18px 55px rgba(0,0,0,0.16);
}

.panel-heading {
    margin-bottom: 18px;
}

.panel-heading h3 {
    margin: 0 0 7px;
    color: #f5f5ff;
    font-size: 18px;
    font-weight: 700;
}

.panel-heading p {
    margin: 0;
    color: var(--muted);
    font-size: 12px;
    line-height: 1.7;
}

.field-label {
    color: #dce0f2;
    font-size: 13px;
    font-weight: 600;
    margin-bottom: 8px;
}

#prompt-box textarea {
    min-height: 185px !important;
    padding: 17px !important;
    border: 1px solid rgba(165,145,255,0.2) !important;
    border-radius: 14px !important;
    background: #0b0e19 !important;
    color: #f4f3ff !important;
    font-size: 14px !important;
    line-height: 1.8 !important;
    transition: border-color .2s, box-shadow .2s;
}

#prompt-box textarea:focus {
    border-color: #9680ff !important;
    box-shadow: 0 0 0 3px rgba(150,128,255,0.12) !important;
}

#prompt-box textarea::placeholder {
    color: #727c96 !important;
}

.suggestions-label {
    margin: 18px 0 10px;
    color: #a6aec5;
    font-size: 12px;
    font-weight: 600;
}

.suggestion-btn button {
    min-height: 39px !important;
    border: 1px solid var(--border) !important;
    border-radius: 11px !important;
    background: rgba(255,255,255,0.035) !important;
    color: #cbd1e7 !important;
    font-size: 11px !important;
    font-weight: 500 !important;
    transition: all .2s ease;
}

.suggestion-btn button:hover {
    border-color: rgba(157,123,255,0.6) !important;
    background: rgba(157,123,255,0.10) !important;
}

#generate-btn button {
    min-height: 51px !important;
    border: none !important;
    border-radius: 13px !important;
    background: linear-gradient(105deg, #8b6bff, #5b78ff) !important;
    color: white !important;
    font-weight: 700 !important;
    box-shadow: 0 8px 24px rgba(105,92,255,0.23);
    transition: transform .2s, box-shadow .2s;
}

#generate-btn button:hover {
    transform: translateY(-1px);
    box-shadow: 0 10px 30px rgba(105,92,255,0.36);
}

#clear-btn button {
    min-height: 51px !important;
    border: 1px solid var(--border) !important;
    border-radius: 13px !important;
    background: rgba(255,255,255,0.04) !important;
    color: #d3d7e8 !important;
    font-weight: 600 !important;
}

#result-panel {
    min-height: 420px;
}

#result-panel .prose {
    color: #dce2f5 !important;
    font-size: 14px;
    line-height: 1.85;
    overflow-wrap: anywhere;
}

#result-panel .prose h1,
#result-panel .prose h2,
#result-panel .prose h3 {
    color: #ffffff !important;
    letter-spacing: -0.4px;
}

#result-panel .prose h2 {
    padding-bottom: 9px;
    border-bottom: 1px solid var(--border);
}

#result-panel .prose strong {
    color: #c8baff !important;
}

#result-panel .prose a {
    color: #a99aff !important;
}

#result-panel .prose code {
    color: #d8caff;
    background: rgba(157,123,255,0.1);
    border-radius: 5px;
    padding: 2px 5px;
}

#result-panel .prose table {
    display: block;
    max-width: 100%;
    overflow-x: auto;
}

#result-panel .prose th,
#result-panel .prose td {
    border-color: var(--border) !important;
    padding: 9px 12px;
}

.output-note {
    margin-top: 18px;
    padding-top: 13px;
    border-top: 1px solid var(--border);
    color: #737e98;
    font-size: 11px;
    line-height: 1.7;
}

.footer {
    margin-top: 28px;
    padding: 20px 10px;
    border-top: 1px solid var(--border);
    text-align: center;
    color: #727c95;
    font-size: 11px;
    line-height: 1.8;
}

.footer strong {
    color: #b8a8ff;
}

@media (max-width: 700px) {
    #app-shell {
        padding: 10px 10px 20px;
    }

    .topbar {
        margin-bottom: 30px;
        padding: 12px;
    }

    .hero {
        margin-bottom: 26px;
    }

    .hero h1 {
        letter-spacing: -1.4px;
    }

    .panel {
        padding: 16px !important;
    }

    #prompt-box textarea {
        min-height: 150px !important;
    }

    #result-panel {
        min-height: 280px;
    }

    .status-pill {
        font-size: 10px;
        padding: 7px 8px;
    }
}
"""


# -------------------- UI --------------------

with gr.Blocks(
    theme=gr.themes.Base(
        primary_hue="violet",
        secondary_hue="blue",
        neutral_hue="slate",
    ),
    css=CSS,
    title="AI Text Generator | Premium AI Writer",
) as demo:

    with gr.Column(elem_id="app-shell", elem_classes=["app-shell"]):

        gr.HTML("""
        <div class="topbar">
            <div class="brand">
                <div class="brand-icon">✦</div>
                <div>
                    AI Studio
                    <span class="brand-sub">YOUR CREATIVE WORKSPACE</span>
                </div>
            </div>
            <div class="status-pill">● AI POWERED</div>
        </div>

        <div class="hero">
            <div class="eyebrow">✦ YOUR IDEAS, AMPLIFIED BY AI</div>
            <h1>Turn ideas into<br>
            <span class="gradient-text">extraordinary words.</span></h1>
            <p>
                Your intelligent writing companion for stories, content,
                creative ideas, and everyday writing — in Bengali, English,
                and more.
            </p>
            <div class="feature-row">
                <span class="feature">✦ Smart Writing</span>
                <span class="feature">◈ Multiple Languages</span>
                <span class="feature">⚡ Powered by Groq</span>
            </div>
        </div>
        """)

        with gr.Row(equal_height=False):

            # LEFT: Prompt editor
            with gr.Column(scale=5, elem_classes=["panel"]):

                gr.HTML("""
                <div class="panel-heading">
                    <h3>✍️ Create something amazing</h3>
                    <p>Describe what you want the AI to write.</p>
                </div>
                <div class="field-label">YOUR PROMPT</div>
                """)

                prompt = gr.Textbox(
                    label=None,
                    placeholder=(
                        "Example: বাংলায় দুর্গাপুজোর ইতিহাস ও "
                        "সংস্কৃতি সম্পর্কে একটি সুন্দর লেখা তৈরি করো..."
                    ),
                    lines=6,
                    max_lines=12,
                    elem_id="prompt-box",
                    show_label=False,
                    container=False,
                )

                gr.HTML(
                    '<div class="suggestions-label">'
                    'NEED INSPIRATION? TRY A PROMPT</div>'
                )

                with gr.Row():
                    story_btn = gr.Button(
                        "📖 Short Story",
                        size="sm",
                        elem_classes=["suggestion-btn"],
                    )
                    blog_btn = gr.Button(
                        "✍️ Blog Post",
                        size="sm",
                        elem_classes=["suggestion-btn"],
                    )

                with gr.Row():
                    social_btn = gr.Button(
                        "📱 Social Caption",
                        size="sm",
                        elem_classes=["suggestion-btn"],
                    )
                    bengali_btn = gr.Button(
                        "বাংলা লেখা",
                        size="sm",
                        elem_classes=["suggestion-btn"],
                    )

                gr.HTML("<div style='height:20px'></div>")

                with gr.Row():
                    clear_btn = gr.Button(
                        "↺  Clear",
                        elem_id="clear-btn",
                        scale=1,
                    )
                    generate_btn = gr.Button(
                        "✦  Generate Text",
                        variant="primary",
                        elem_id="generate-btn",
                        scale=2,
                    )

                gr.HTML("""
                <div class="output-note">
                    ✦ Better prompts create better results.
                    Review AI-generated content before publishing.
                </div>
                """)

            # RIGHT: AI output
            with gr.Column(
                scale=6,
                elem_classes=["panel"],
                elem_id="result-panel",
            ):

                gr.HTML("""
                <div class="panel-heading">
                    <h3>✦ Your AI creation</h3>
                    <p>Your generated content will appear here.</p>
                </div>
                """)

                output = gr.Markdown(
                    value=(
                        "<div style='text-align:center;"
                        "padding:65px 10px;color:#8791aa;'>"
                        "<div style='font-size:42px;margin-bottom:15px;'>✧</div>"
                        "<strong style='color:#c5b8ff;'>"
                        "Your next great idea starts here</strong>"
                        "<p style='margin-top:10px;font-size:13px;'>"
                        "Enter a prompt and click Generate Text to begin."
                        "</p></div>"
                    ),
                    label=None,
                )

                gr.HTML("""
                <div class="output-note">
                    ✧ AI-generated content · Powered by Groq
                </div>
                """)

        gr.HTML("""
        <div class="footer">
            Crafted with <strong>✦ AI Studio</strong><br>
            Create freely. Think bigger. Write better.
        </div>
        """)

    # Generate actions
    generate_btn.click(
        fn=generate_text,
        inputs=prompt,
        outputs=output,
    )

    prompt.submit(
        fn=generate_text,
        inputs=prompt,
        outputs=output,
    )

    # Clear both prompt and output
    clear_btn.click(
        fn=lambda: ("", ""),
        inputs=None,
        outputs=[prompt, output],
    )

    # Prompt suggestion actions
    story_btn.click(
        fn=lambda: (
            "বাংলায় সুন্দরবনের একটি বাঘকে নিয়ে "
            "একটি আকর্ষণীয় ছোট গল্প লেখো।"
        ),
        inputs=None,
        outputs=prompt,
    )

    blog_btn.click(
        fn=lambda: (
            "Write a well-structured blog post about "
            "how AI can help small businesses grow."
        ),
        inputs=None,
        outputs=prompt,
    )

    social_btn.click(
        fn=lambda: (
            "Write 5 engaging Bengali Facebook captions "
            "for a local business."
        ),
        inputs=None,
        outputs=prompt,
    )

    bengali_btn.click(
        fn=lambda: (
            "বাংলার সংস্কৃতি, ঐতিহ্য ও উৎসব নিয়ে "
            "সহজ ভাষায় একটি সুন্দর লেখা তৈরি করো।"
        ),
        inputs=None,
        outputs=prompt,
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))

    demo.queue().launch(
        server_name="0.0.0.0",
        server_port=port,
    )
