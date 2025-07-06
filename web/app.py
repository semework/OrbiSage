"""Gradio chat for Orbisage Router"""
import gradio as gr
from orbisage_router.graph import build_router_graph

# Build your LangGraph router workflow
wf = build_router_graph()

# Your chat handler
def chat(msg, history):
    history = history or []
    final = wf.invoke({"user_input": msg, "messages": []})
    history.append({"role": "user", "content": msg})
    history.append({"role": "assistant", "content": final["messages"][-1]})
    return "", history

# Build the Gradio Blocks UI
with gr.Blocks(theme="default") as demo:
    gr.Markdown("### 🌿 Orbisage – AI Router Chat")

    # Chatbot with OpenAI-style messages & smaller height
    chatbox = gr.Chatbot(value=[], type="messages", height=300)

    with gr.Row():
        txt = gr.Textbox(
            show_label=False,
            placeholder="Ask me anything…",
            lines=1,
            max_lines=4,
            autofocus=True
        )
        send_btn = gr.Button("Submit")

    # Bind Enter and Submit button to same handler
    txt.submit(chat, inputs=[txt, chatbox], outputs=[txt, chatbox])
    send_btn.click(chat, inputs=[txt, chatbox], outputs=[txt, chatbox])

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
