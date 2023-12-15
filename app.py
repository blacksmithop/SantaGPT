import gradio as gr

css = """
.user {
    background-color: slategrey;
}
"""

def AskBot(question):
    return question.upper()

with gr.Blocks(css=css) as demo:
    chatbot = gr.Chatbot()
    msg = gr.Textbox()
    clear = gr.ClearButton([msg, chatbot])

    def respond(message, chat_history):
        bot_message = AskBot(question=message)
        chat_history.append((message, bot_message))
        return "", chat_history

    msg.submit(respond, [msg, chatbot], [msg, chatbot])

if __name__ == "__main__":
    demo.launch()

