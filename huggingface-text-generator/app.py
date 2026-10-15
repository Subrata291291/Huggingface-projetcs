
import os

import gradio as gr
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_ID = "openai/gpt-oss-20b"


# =========================
# AI TEXT GENERATION
# =========================

def generate_text(prompt):
    if not prompt or not prompt.strip():
        return "⚠️ Please enter a prompt before generating text."

    if not GROQ_API_KEY:
        return (
            "⚠️ **Configuration Error**\n\n"
            "GROQ_API_KEY is missing. Add it to your local "
            ".env file or your Render Environment Variables."
        )

    try:
        client = Groq(api_key=GROQ_API_KEY)

        response = client.chat.completions.create(
            model=MODEL_ID,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert AI writing assistant. "
                        "Answer in the same language as the user's prompt. "
                        "Write useful, accurate, well-structured content. "
                        "Use descriptive headings, paragraphs, bullet points, "
                        "and Markdown tables when appropriate. "
                        "Do not put the entire answer inside a code block. "
                        "Follow the user's requested length and format."
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
        print(
            f"Groq API error: {type(error).__name__}: {error}"
        )

        return (
            "### Unable to generate a response\n\n"
            "Please check your API key, model availability, "
            "rate limits, and Render logs. Try again in a moment."
        )


# =========================
# SAMPLE PROMPTS
# =========================

def sample_prompt(kind):
    prompts = {
        "story": (
            "বাংলায় সুন্দরবনের একটি বাঘকে নিয়ে "
            "একটি আকর্ষণীয় ছোট গল্প লেখো।"
        ),
        "blog": (
            "Write a well-structured blog post about "
            "the cultural importance of Bengali Durga Puja."
        ),
        "social": (
            "বাংলায় দুর্গাপুজো উপলক্ষে একটি আকর্ষণীয় "
            "Facebook পোস্ট লেখো।"
        ),
        "creative": (
            "Write a creative and inspiring piece about "
            "turning ordinary ideas into extraordinary achievements."
        ),
    }

    return prompts.get(kind, "")


def clear_all():
    return "", ""


# =========================
# PREMIUM UI STYLES
# =========================

CSS = """
:root {
    --bg: #090b14;
    --panel: #111421;
    --panel-light: #171a2a;
    --border: rgba(164, 157, 207, 0.17);
    --text: #f4f3ff;
    --muted: #a3a8c2;
    --purple: #8b5cf6;
    --purple-light: #b6a0ff;
}

.gradio-container {
    max-width: 1500px !important;
    margin: auto !important;
    background:
        radial-gradient(
            ellipse at 10% 0%,
            rgba(104, 65, 220, 0.13),
            transparent 40%
        ),
        radial-gradient(
            ellipse at 95% 10%,
            rgba(29, 78, 216, 0.10),
            transparent 35%
        ),
        var(--bg) !important;
    color: var(--text) !important;
    font-family: Inter, ui-sans-serif, system-ui, sans-serif;
}

footer {
    display: none !important;
}

#app-shell {
    max-width: 1380px;
    margin: 0 auto;
    padding: 20px 26px 36px;
}

#topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 16px;
    padding: 16px 20px;
    margin-bottom: 30px;
    background: rgba(18, 21, 37, 0.88);
    border: 1px solid var(--border);
    border-radius: 18px;
    backdrop-filter: blur(18px);
}

.brand {
    display: flex;
    align-items: center;
    gap: 12px;
}

.brand-icon {
    width: 42px;
    height: 42px;
    display: grid;
    place-items: center;
    border-radius: 13px;
    background: linear-gradient(135deg, #8b5cf6, #5b4ce2);
    color: white;
    font-size: 23px;
    box-shadow: 0 6px 24px rgba(124, 86, 255, 0.30);
}

.brand-name {
    font-size: 17px;
    font-weight: 750;
    letter-spacing: -0.4px;
}

.brand-caption {
    color: var(--muted);
    font-size: 10px;
    letter-spacing: 1.1px;
    margin-top: 3px;
}

.status-pill {
    color: #a7f3d0;
    background: rgba(16, 185, 129, 0.10);
    border: 1px solid rgba(52, 211, 153, 0.20);
    border-radius: 999px;
    padding: 8px 12px;
    font-size: 11px;
    white-space: nowrap;
}

#hero {
    text-align: center;
    padding: 12px 12px 32px;
}

.hero-badge {
    display: inline-block;
    padding: 7px 13px;
    margin-bottom: 15px;
    border: 1px solid rgba(167, 139, 250, 0.25);
    border-radius: 999px;
    background: rgba(139, 92, 246, 0.09);
    color: #c4b5fd;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1px;
}

.hero-title {
    font-size: clamp(30px, 4.2vw, 53px);
    font-weight: 850;
    line-height: 1.12;
    letter-spacing: -2px;
    margin: 0 0 14px;
    color: #faf9ff;
}

.hero-gradient {
    background: linear-gradient(
        100deg,
        #b9a6ff 0%,
        #8b8bff 45%,
        #df9cff 100%
    );
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
}

.hero-subtitle {
    max-width: 660px;
    margin: 0 auto;
    color: var(--muted);
    font-size: 14px;
    line-height: 1.8;
}

.feature-row {
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
    gap: 9px;
    margin-top: 20px;
}

.feature-chip {
    padding: 8px 12px;
    border-radius: 999px;
    border: 1px solid var(--border);
    background: rgba(255, 255, 255, 0.025);
    color: #c7c9de;
    font-size: 11px;
}

#workspace {
    align-items: flex-start !important;
    gap: 22px !important;
}

/* Sticky left-side editor */
#prompt-panel {
    position: sticky !important;
    top: 14px;
    align-self: flex-start !important;
    max-height: calc(100vh - 28px);
    overflow-y: auto;
    overflow-x: hidden;
    scrollbar-width: thin;
    scrollbar-color: #4f4578 transparent;
    background: rgba(17, 20, 33, 0.94);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 22px !important;
    box-shadow: 0 18px 60px rgba(0, 0, 0, 0.16);
}

#prompt-panel::-webkit-scrollbar {
    width: 5px;
}

#prompt-panel::-webkit-scrollbar-thumb {
    background: #4f4578;
    border-radius: 99px;
}

#result-panel {
    min-width: 0;
    align-self: flex-start !important;
    background: rgba(17, 20, 33, 0.80);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 22px !important;
}

.section-eyebrow {
    color: #b9a4ff;
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-bottom: 9px;
}

.section-title {
    font-size: 21px;
    font-weight: 750;
    letter-spacing: -0.6px;
    margin: 0 0 8px;
    color: #f5f3ff;
}

.section-description {
    color: var(--muted);
    font-size: 12px;
    line-height: 1.7;
    margin-bottom: 22px;
}

#prompt-input textarea {
    min-height: 180px !important;
    background: #0c0f1b !important;
    border: 1px solid #30334b !important;
    border-radius: 12px !important;
    color: #f3f1ff !important;
    font-size: 14px !important;
    line-height: 1.8 !important;
    padding: 15px !important;
}

#prompt-input textarea:focus {
    border-color: #8b5cf6 !important;
    box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.12) !important;
}

#prompt-input label,
#result-panel label {
    color: #d9d7ee !important;
    font-size: 12px !important;
    font-weight: 650 !important;
}

#sample-title {
    color: #969ab6;
    font-size: 10px;
    font-weight: 750;
    letter-spacing: 1px;
    margin: 22px 0 10px;
}

.sample-btn {
    border: 1px solid #30334b !important;
    background: #191d30 !important;
    color: #d9d7f2 !important;
    border-radius: 10px !important;
    font-size: 11px !important;
    transition: all 0.2s ease !important;
}

.sample-btn:hover {
    background: #282044 !important;
    border-color: #8061dc !important;
    transform: translateY(-1px);
}

#generate-btn {
    background: linear-gradient(110deg, #8b5cf6, #673de0) !important;
    border: 1px solid rgba(190, 165, 255, 0.30) !important;
    color: white !important;
    border-radius: 11px !important;
    font-weight: 750 !important;
    box-shadow: 0 7px 24px rgba(111, 66, 220, 0.22);
    transition: all 0.2s ease !important;
}

#generate-btn:hover {
    filter: brightness(1.12);
    transform: translateY(-1px);
}

#clear-btn,
#copy-btn {
    background: #202438 !important;
    color: #e3e1f6 !important;
    border: 1px solid #343850 !important;
    border-radius: 11px !important;
    font-weight: 650 !important;
}

#clear-btn:hover,
#copy-btn:hover {
    background: #2b3048 !important;
}

.helper-text {
    color: #858aa8;
    font-size: 10px;
    line-height: 1.7;
    margin-top: 15px;
}

#response-scroll {
    max-height: calc(100vh - 285px);
    min-height: 280px;
    overflow-y: auto;
    overflow-x: hidden;
    padding: 8px 12px 8px 2px;
    scrollbar-width: thin;
    scrollbar-color: #554982 transparent;
    overscroll-behavior: contain;
    border-top: 1px solid var(--border);
    border-bottom: 1px solid var(--border);
}

#response-scroll::-webkit-scrollbar {
    width: 6px;
}

#response-scroll::-webkit-scrollbar-thumb {
    background: #554982;
    border-radius: 99px;
}

#response-scroll .prose {
    color: #e1e3f2 !important;
    font-size: 13px;
    line-height: 1.9;
    overflow-wrap: anywhere;
}

#response-scroll .prose h1,
#response-scroll .prose h2,
#response-scroll .prose h3 {
    color: #f4efff !important;
    letter-spacing: -0.4px;
    line-height: 1.45;
    margin-top: 1.4em;
}

#response-scroll .prose h1 {
    font-size: 25px;
}

#response-scroll .prose h2 {
    font-size: 20px;
}

#response-scroll .prose h3 {
    font-size: 16px;
}

#response-scroll .prose strong {
    color: #d0bdff !important;
}

#response-scroll .prose a {
    color: #b7a3ff !important;
}

#response-scroll .prose table {
    display: block;
    width: 100%;
    overflow-x: auto;
    border-collapse: collapse;
    font-size: 12px;
}

#response-scroll .prose th {
    background: #201d35;
    color: #d9caff;
}

#response-scroll .prose th,
#response-scroll .prose td {
    border: 1px solid #34334b;
    padding: 10px 12px;
}

#response-scroll .prose blockquote {
    border-left-color: #8b5cf6;
    background: rgba(139, 92, 246, 0.06);
    padding: 10px 15px;
    border-radius: 0 8px 8px 0;
}

.response-toolbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 10px;
    flex-wrap: wrap;
    margin-bottom: 15px;
}

.response-caption {
    color: var(--muted);
    font-size: 11px;
}

#footer-note {
    text-align: center;
    color: #777c98;
    font-size: 10px;
    padding: 26px 10px 0;
    line-height: 1.8;
}

@media (max-width: 760px) {
    #app-shell {
        padding: 12px 12px 26px;
    }

    #topbar {
        padding: 12px;
        margin-bottom: 18px;
    }

    .hero-title {
        letter-spacing: -1.2px;
    }

    #workspace {
        gap: 16px !important;
    }

    #prompt-panel {
        position: static !important;
        max-height: none;
        overflow: visible;
        padding: 17px !important;
    }

    #result-panel {
        padding: 17px !important;
    }

    #response-scroll {
        max-height: 65vh;
        min-height: 220px;
    }

    #prompt-input textarea {
        min-height: 140px !important;
    }
}

@media (prefers-reduced-motion: reduce) {
    *,
    *::before,
    *::after {
        transition: none !important;
        animation: none !important;
    }
}
"""


# =========================
# GRADIO APPLICATION
# =========================

with gr.Blocks(
    title="AI Studio | Smart Writing Assistant",
    theme=gr.themes.Base(
        primary_hue="violet",
        secondary_hue="slate",
        neutral_hue="slate",
    ),
    css=CSS,
) as demo:

    with gr.Column(elem_id="app-shell"):

        # Header
        gr.HTML(
            """
            <header id="topbar">
                <div class="brand">
                    <div class="brand-icon">✦</div>
                    <div>
                        <div class="brand-name">AI Studio</div>
                        <div class="brand-caption">
                            YOUR CREATIVE WORKSPACE
                        </div>
                    </div>
                </div>
                <div class="status-pill">✦ AI POWERED</div>
            </header>
            """
        )

        # Hero section
        gr.HTML(
            """
            <section id="hero">
                <div class="hero-badge">
                    ✦ YOUR IDEAS, AMPLIFIED BY AI
                </div>

                <h1 class="hero-title">
                    Turn ideas into<br>
                    <span class="hero-gradient">
                        extraordinary words.
                    </span>
                </h1>

                <p class="hero-subtitle">
                    Your intelligent writing companion for stories,
                    content, creative ideas, and everyday writing
                    in Bengali, English, and more.
                </p>

                <div class="feature-row">
                    <span class="feature-chip">✧ Smart Writing</span>
                    <span class="feature-chip">✧ Multiple Languages</span>
                    <span class="feature-chip">⚡ Powered by Groq</span>
                </div>
            </section>
            """
        )

        # Main workspace
        with gr.Row(elem_id="workspace"):

            # LEFT: Sticky prompt panel
            with gr.Column(
                scale=5,
                min_width=300,
                elem_id="prompt-panel",
            ):
                gr.HTML(
                    """
                    <div class="section-eyebrow">
                        ✦ CREATE SOMETHING AMAZING
                    </div>
                    <h2 class="section-title">
                        What shall we write?
                    </h2>
                    <div class="section-description">
                        Describe what you want the AI to create.
                        Be specific for better results.
                    </div>
                    """
                )

                prompt_input = gr.Textbox(
                    label="YOUR PROMPT",
                    placeholder=(
                        "উদাহরণ: বাংলায় দুর্গাপুজোর ইতিহাস "
                        "ও সংস্কৃতি সম্পর্কে লেখো..."
                    ),
                    lines=6,
                    max_lines=12,
                    elem_id="prompt-input",
                )

                gr.HTML(
                    '<div id="sample-title">'
                    'NEED INSPIRATION? TRY A PROMPT'
                    '</div>'
                )

                with gr.Row():
                    story_btn = gr.Button(
                        "✦ Short Story",
                        elem_classes=["sample-btn"],
                    )
                    blog_btn = gr.Button(
                        "✦ Blog Post",
                        elem_classes=["sample-btn"],
                    )

                with gr.Row():
                    social_btn = gr.Button(
                        "✦ Social Caption",
                        elem_classes=["sample-btn"],
                    )
                    creative_btn = gr.Button(
                        "✦ Creative Writing",
                        elem_classes=["sample-btn"],
                    )

                with gr.Row():
                    clear_btn = gr.Button(
                        "↺ Clear",
                        elem_id="clear-btn",
                        scale=1,
                    )
                    generate_btn = gr.Button(
                        "✦ Generate Text",
                        elem_id="generate-btn",
                        variant="primary",
                        scale=2,
                    )

                gr.HTML(
                    """
                    <div class="helper-text">
                        ✧ Better prompts create better results.
                        Review AI-generated content before publishing.
                    </div>
                    """
                )

            # RIGHT: Independent response panel
            with gr.Column(
                scale=7,
                min_width=320,
                elem_id="result-panel",
            ):
                gr.HTML(
                    """
                    <div class="section-eyebrow">
                        ✧ YOUR AI CREATION
                    </div>
                    <h2 class="section-title">
                        Your words, beautifully crafted.
                    </h2>
                    <div class="section-description">
                        Your generated content will appear here.
                        Long answers scroll inside this panel.
                    </div>
                    <div class="response-toolbar">
                        <span class="response-caption">
                            MARKDOWN SUPPORTED · BENGALI · ENGLISH
                        </span>
                    </div>
                    """
                )

                with gr.Column(elem_id="response-scroll"):
                    output = gr.Markdown(
                        value=(
                            "### Your next great idea starts here ✨\n\n"
                            "Enter a prompt on the left and click "
                            "**Generate Text**.\n\n"
                            "Your AI-generated story, blog post, "
                            "caption, or detailed explanation will "
                            "appear in this panel."
                        ),
                        elem_id="response-content",
                    )

                with gr.Row():
                    copy_btn = gr.Button(
                        "⧉ Copy Response",
                        elem_id="copy-btn",
                    )

                    download_btn = gr.DownloadButton(
                        "↓ Download TXT",
                        variant="secondary",
                    )

        gr.HTML(
            """
            <div id="footer-note">
                ✦ AI-generated content · Powered by Groq<br>
                Crafted with care by AI Studio
            </div>
            """
        )

    # =========================
    # EVENT HANDLERS
    # =========================

    generate_btn.click(
        fn=generate_text,
        inputs=prompt_input,
        outputs=output,
        show_progress="full",
    )

    prompt_input.submit(
        fn=generate_text,
        inputs=prompt_input,
        outputs=output,
        show_progress="full",
    )

    story_btn.click(
        fn=lambda: sample_prompt("story"),
        outputs=prompt_input,
    )

    blog_btn.click(
        fn=lambda: sample_prompt("blog"),
        outputs=prompt_input,
    )

    social_btn.click(
        fn=lambda: sample_prompt("social"),
        outputs=prompt_input,
    )

    creative_btn.click(
        fn=lambda: sample_prompt("creative"),
        outputs=prompt_input,
    )

    clear_btn.click(
        fn=clear_all,
        outputs=[prompt_input, output],
    )

    copy_btn.click(
        fn=None,
        inputs=output,
        js="""
        async (text) => {
            const content = String(text || "");
            try {
                await navigator.clipboard.writeText(content);
            } catch (error) {
                console.error("Copy failed:", error);
            }
        }
        """,
    )

    download_btn.click(
        fn=lambda text: (
            _write_download_file(text)
        ),
        inputs=output,
        outputs=download_btn,
    )


# =========================
# DOWNLOAD HELPER
# =========================

def _write_download_file(text):
    import tempfile

    fd, path = tempfile.mkstemp(
        prefix="ai_studio_",
        suffix=".txt",
        text=True,
    )

    with os.fdopen(fd, "w", encoding="utf-8") as file:
        file.write(text or "")

    return path


if __name__ == "__main__":
    demo.launch()
