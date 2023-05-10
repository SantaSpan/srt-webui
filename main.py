import asyncio
import time
from dataclasses import replace
from fnmatch import translate

import gradio as gr
import srt
from deepl import DeepLCLI

from_lang = "en"
to_lang = "ja"

test_file_path = "./sawagi.srt"

output_path = "/content/test.srt"
    
    
delimiter = "\n---\n"
async def replace_sub(subtitle_chunk):
    orig_lang = subtitle_chunk.content
    translated = await deepl.translate_async(orig_lang)
    subtitle_chunk.content = translated
    return





async def main():
    with open(test_file_path, "r", encoding="utf-8") as file:
        file_data = file.read()
    
    subs = srt.parse(file_data)
    tasks = []
    
    for sub in subs:
        tasks.append(asyncio.create_task(replace_sub(sub)))
        await asyncio.sleep(1)
        

    # run event loop
    asyncio.gather(*tasks)
    
    for sub in subs:
        print(sub.content)

def no_async_main():
    with open(test_file_path, "r", encoding="utf-8") as file:
        file_data = file.read()
    
    subs = list(srt.parse(file_data))
    
    for sub in subs:
        translation = deepl.translate(sub.content)
        sub.content = translation
        
    new_subs = []
    for sub in subs:
        new_subs.append(sub.content)
        
    print(new_subs)
        
    
        
        
def batch_deepl_text(segments: list[str], max_len=3000):

    delimiter_len = len(delimiter)
    bulk_segments = [""]
    for i in segments:
        new_seg = False
        current_batch = bulk_segments[-1]
        
        if len(current_batch) + len(i) + delimiter_len >= max_len:
            new_seg = True
            current_batch = ""
            
        if not new_seg:
            current_batch += delimiter
            current_batch += i
            bulk_segments[-1] = current_batch
        else:
            bulk_segments.append(i)
    
    return bulk_segments

def batch_get_translations(deepl, segment_texts):
    translated_segments = []
    batched_segments = batch_deepl_text(segment_texts)
    
    print(len(batched_segments))
    for count, batch in enumerate(batched_segments):
        print(count)
        translated = deepl.translate(batch)
        batch_segments = translated.split(delimiter)
        batch_segments = [x for x in batch_segments if x.strip()]
        translated_segments.extend(batch_segments)
    
    return translated_segments
def high_level():
    srt_data = ()
    split_translations = ()
    
    for i, translation_text in enumerate(split_translations):
        srt_data[i].content = translation_text
        
    
    new_srt = srt.compose(srt_data)
    pass

def translate_file(input_file, output_file, langs=["ja", "en"]):
    deepl = DeepLCLI(langs[0], langs[1], timeout=150000, use_dom_submit=True)
    
    
    with open(input_file, "r", encoding="utf-8") as file:
        file_data = file.read()
        
    subs = list(srt.parse(file_data))
    segments = [x.content for x in subs]
    translated = batch_get_translations(deepl,segments)
    for count, i in enumerate(translated):
        subs[count].content = i
        
    new_subs = srt.compose(subs)
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(new_subs)

def gradio_translate(target_file, from_language, to_language):
    deepl = DeepLCLI(from_language, to_language, timeout=150000, use_dom_submit=True)
    file_data = target_file.read()
    file_data = file_data.decode("utf-8")
    print(file_data)
    subs = list(srt.parse(file_data))
    segments = [x.content for x in subs]
    translated = batch_get_translations(deepl,segments)
    for count, i in enumerate(translated):
        subs[count].content = i
        
    new_subs = srt.compose(subs)
    with open(output_path, "w", encoding="utf-8") as file:
        file.write(new_subs)
        
    return output_path
    

def gradio():
    inputs = [gr.File(label="Upload File"), gr.Text(label="From Language"),gr.Text(label="To Language")]
    interface = gr.Interface(fn=gradio_translate,
                             inputs=inputs,
                             outputs = [
                                 gr.File(label="Download")
                             ])
    
    demo = gr.TabbedInterface([interface], tab_names=["deepl"])

    # # Queue up the demo
    # if app_config.queue_concurrency_count is not None and app_config.queue_concurrency_count > 0:
    #     demo.queue(concurrency_count=app_config.queue_concurrency_count)
   
    demo.launch(share=True)

if __name__ == "__main__":
    gradio()
    #translate_file("./sawagi.srt", "new_test.srt", langs=["en", "ja"])