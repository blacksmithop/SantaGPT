import gradio as gr
import os
import time
from utils.core import chat
import speech_recognition as sr


r = sr.Recognizer()


def print_like_dislike(x: gr.LikeData):
    print(x.index, x.value, x.liked)


def add_text(history, text):
    history = history + [(text, None)]
    return history, gr.Textbox(value="", interactive=False)


def get_chatbot_response(filePath):
    print("filePath", filePath)
    file = sr.AudioFile(filePath)
    response = r.recognize_whisper(file)
    return [((filePath + ".wav",), response)]


def bot(history):
    question = history[-1][0]
    response = chat(question=question)
    history[-1][1] = ""
    for character in response:
        history[-1][1] += character
        time.sleep(0.05)
        yield history


with gr.Blocks() as demo:
    chatbot = gr.Chatbot(
        [],
        elem_id="chatbot",
        bubble_full_width=False,
        avatar_images=(
            None,
            (os.path.join(os.path.dirname(__file__), "./data/images/avatar.png")),
        ),
    )

    with gr.Row():
        txt = gr.Textbox(
            scale=4,
            show_label=False,
            placeholder="Enter text and press enter, or upload an image",
            container=False,
        )

    txt_msg = txt.submit(add_text, [chatbot, txt], [chatbot, txt], queue=False).then(
        bot, chatbot, chatbot, api_name="bot_response"
    )
    txt_msg.then(lambda: gr.Textbox(interactive=True), None, [txt], queue=False)
    mic = gr.Audio(sources=["microphone"], type="filepath")
    mic.change(get_chatbot_response, mic, chatbot)

    chatbot.like(print_like_dislike, None, None)


if __name__ == "__main__":
    demo.launch(
        share=False,
        debug=True,
        # server_name="0.0.0.0",
        server_port=8000,
    )
