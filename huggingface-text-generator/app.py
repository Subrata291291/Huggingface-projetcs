
import os
import gradio as gr

from ui import build_app
from styles import load_css


if __name__ == "__main__":
    app = build_app()
    port = int(os.environ.get("PORT", "7860"))

    app.launch(
        server_name="0.0.0.0",
        server_port=port,
        share=True,
        theme=gr.themes.Base(
            primary_hue="violet",
            secondary_hue="slate",
            neutral_hue="slate",
        ),
        css=load_css(),
    )
