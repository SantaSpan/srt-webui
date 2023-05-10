import asyncio
import subprocess as sp
import time
from dataclasses import replace
from distutils.spawn import spawn
from fnmatch import translate

import gradio as gr
import srt
from deepl import DeepLCLI

default_from_lang = "ja"
default_to_lang = "en"
output_path = "/content/new.srt"

def gradio_translate(target_file, from_language, to_language):
    target_file = target_file.name
    return spawn_new_process(target_file, from_language, to_language)

def spawn_new_process(target_file, from_language, to_language):
    cmd = ["python", "./deepl_tl.py", "--filename", target_file, "--out-filename", output_path, "--from_lang", from_language, "--to_lang", to_language]
    p = sp.Popen(cmd)
    p.wait()
    return output_path

def gradio():
    inputs = [gr.File(label="Upload File"), gr.Text(label="From Language", value=default_from_lang),gr.Text(label="To Language", value=default_to_lang)]
    interface = gr.Interface(fn=gradio_translate,
                             inputs=inputs,
                             outputs = [
                                 gr.File(label="Download")
                             ])
    
    demo = gr.TabbedInterface([interface], tab_names=["deepl"])

    # # Queue up the demo
    demo.queue(concurrency_count=4)
   
    demo.launch(share=True)

if __name__ == "__main__":
    # maybe bad
    # loop = asyncio.new_event_loop()
    # asyncio.set_event_loop(loop)
    gradio()
    #translate_file("./sawagi.srt", "new_test.srt", langs=["en", "ja"])