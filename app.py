import os
import gradio as gr
import google.generativeai as genai

# 1. API Setup
# Try to load API key from .env file if it exists
if os.path.exists(".env"):
    with open(".env") as f:
        for line in f:
            if line.strip() and not line.strip().startswith("#"):
                try:
                    key, val = line.strip().split("=", 1)
                    os.environ[key.strip()] = val.strip()
                except ValueError:
                    pass

api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise ValueError("API Key not found! Please set the GEMINI_API_KEY environment variable in your environment or in a .env file.")

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.5-flash')

# 2. Tool Logic
def text_summarizer(text):
    if not text.strip():
        return "Please provide some text to summarize."
    prompt = f"Provide a brief, concise summary of the following text:\n\n{text}"
    return model.generate_content(prompt).text

def idea_generator(topic):
    if not topic.strip():
        return "Please enter a topic to generate ideas."
    prompt = f"Generate 5 creative, practical, and distinct ideas regarding: {topic}"
    return model.generate_content(prompt).text

def simple_chatbot(message, history):
    if not message.strip():
        return "Please enter a message."
    return model.generate_content(message).text

# 3. THE FIX: Hardcoding the colors so Gradio CANNOT make it white.
# We are manually painting the background dark (#111827) and the buttons blue (#3b82f6).
brute_force_dark_theme = gr.themes.Base().set(
    body_background_fill="#111827",      
    body_text_color="#ffffff",           
    background_fill_primary="#1f2937",   
    background_fill_secondary="#111827",
    border_color_primary="#374151",
    button_primary_background_fill="#3b82f6", 
    button_primary_text_color="#ffffff"
)

# 4. Custom CSS to force the inner titles to be blue and input text to be black
custom_css = """
.blue-title { color: #3b82f6 !important; text-align: center; font-size: 1.5em; font-weight: bold; margin-bottom: 15px; }
.tab-nav button.selected { color: #3b82f6 !important; font-weight: bold !important; border-bottom-color: #3b82f6 !important; background: transparent !important;}
.tab-nav button { color: #9ca3af !important; }

/* Force text inside inputs and textareas to be black for visibility */
textarea, input, select, .gr-input, .gr-select {
    color: #000000 !important;
}

/* Force text color in user chat bubbles to be black for legibility */
.user-message, .message.user, .message.user *, [data-testid="user-message"], [data-testid="user-message"] * {
    color: #000000 !important;
}
"""

# 5. Interface Setup
with gr.Blocks(theme=brute_force_dark_theme, css=custom_css) as app:
    gr.Markdown("<h1 style='text-align: center;'>🛠️ Multi-Tool AI Application</h1>")
    
    with gr.Tab("Text Summarizer"):
        gr.Markdown("<div class='blue-title'>📝 Text Summarizer</div>")
        with gr.Row():
            with gr.Column():
                summary_in = gr.Textbox(lines=6, placeholder="Paste your long text here...", label="Input Text")
                sum_btn = gr.Button("Summarize", variant="primary")
            with gr.Column():
                summary_out = gr.Textbox(lines=6, label="Summarized Output", interactive=False)
        sum_btn.click(fn=text_summarizer, inputs=summary_in, outputs=summary_out)

    with gr.Tab("Idea Generator"):
        gr.Markdown("<div class='blue-title'>💡 Idea Generator</div>")
        with gr.Row():
            with gr.Column():
                idea_in = gr.Textbox(lines=2, placeholder="Enter a topic...", label="Topic")
                idea_btn = gr.Button("Generate Ideas", variant="primary")
            with gr.Column():
                idea_out = gr.Textbox(lines=6, label="Generated Ideas", interactive=False)
        idea_btn.click(fn=idea_generator, inputs=idea_in, outputs=idea_out)

    with gr.Tab("Simple Chatbot"):
        gr.Markdown("<div class='blue-title'>🤖 AI Chatbot</div>")
        gr.ChatInterface(fn=simple_chatbot)

if __name__ == "__main__":
    app.launch()
