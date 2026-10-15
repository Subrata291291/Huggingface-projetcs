
import os
import tempfile

import gradio as gr

from generator import generate_text
from prompts import SAMPLE_PROMPTS


def write_markdown_file(content: str) -> str:
    fd, path = tempfile.mkstemp(
        prefix="ai_studio_",
        suffix=".md",
        text=True,
    )

    with os.fdopen(fd, "w", encoding="utf-8") as file:
        file.write(content or "")

    return path


def clear_all():
    return "", (
        "### Your next great idea starts here ✨\n\n"
        "Enter a prompt on the left and click **Generate Text**.\n\n"
        "Your AI-generated content will appear in this panel."
    )


def build_app() -> gr.Blocks:
    with gr.Blocks(
        title="AI Studio | Smart Writing Assistant"
    ) as demo:

        with gr.Column(elem_id="app-shell"):

            gr.HTML("""
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
            """)

            gr.HTML("""
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
                    <span class="feature-chip">
                        ✧ Multiple Languages
                    </span>
                    <span class="feature-chip">
                        ⚡ Powered by Groq
                    </span>
                </div>
            </section>
            """)

            with gr.Row(elem_id="workspace"):

                # LEFT: Prompt editor
                with gr.Column(
                    scale=5,
                    min_width=300,
                    elem_id="prompt-panel",
                ):

                    gr.HTML("""
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
                    """)

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

                    gr.HTML("""
                    <div id="sample-title">
                        NEED INSPIRATION? TRY A PROMPT
                    </div>
                    """)

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

                    gr.HTML("""
                    <div class="helper-text">
                        ✧ Better prompts create better results.
                        Review AI-generated content before publishing.
                    </div>
                    """)

                # RIGHT: Generated content
                with gr.Column(
                    scale=7,
                    min_width=320,
                    elem_id="result-panel",
                ):

                    gr.HTML("""
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
                    """)

                    with gr.Column(elem_id="response-scroll"):
                        output = gr.Markdown(
                            value=(
                                "### Your next great idea starts here ✨\n\n"
                                "Enter a prompt on the left and click "
                                "**Generate Text**.\n\n"
                                "Your AI-generated story, blog post, "
                                "caption, or detailed explanation "
                                "will appear in this panel."
                            ),
                            elem_id="response-content",
                        )

                    with gr.Row():
                        copy_btn = gr.Button(
                            "⧉ Copy Response",
                            elem_id="copy-btn",
                        )

                        download_btn = gr.DownloadButton(
                            "↓ Download Markdown",
                            elem_id="download-btn",
                        )

            gr.HTML("""
            <div id="footer-note">
                ✦ AI-generated content · Powered by Groq<br>
                Crafted with care by AI Studio
            </div>
            """)

        # Generate text
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

        # Sample prompts
        story_btn.click(
            fn=lambda: SAMPLE_PROMPTS["story"],
            outputs=prompt_input,
        )

        blog_btn.click(
            fn=lambda: SAMPLE_PROMPTS["blog"],
            outputs=prompt_input,
        )

        social_btn.click(
            fn=lambda: SAMPLE_PROMPTS["social"],
            outputs=prompt_input,
        )

        creative_btn.click(
            fn=lambda: SAMPLE_PROMPTS["creative"],
            outputs=prompt_input,
        )

        # Clear prompt and result
        clear_btn.click(
            fn=clear_all,
            outputs=[prompt_input, output],
        )

        # Copy generated content
        copy_btn.click(
            fn=None,
            inputs=output,
            outputs=None,
            js="""
            async (text) => {
                const content = String(text || "");

                try {
                    await navigator.clipboard.writeText(content);
                } catch (error) {
                    console.error("Copy failed:", error);
                }

                return [];
            }
            """,
        )

        # Download generated content as Markdown
        download_btn.click(
            fn=write_markdown_file,
            inputs=output,
            outputs=download_btn,
        )

    return demo
