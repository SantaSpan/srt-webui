import argparse
import sys

import srt
from deepl import DeepLCLI

delimiter = "\n---\n"

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
    
    print(f"Text split into {len(batched_segments)} parts")
    print(f"Estimated time: {(len(batched_segments) * 8) + 7} seconds")
        
    
    for count, batch in enumerate(batched_segments):
        print(count)
        print(len(batch))
        print(batch)
        translated = deepl.translate(batch)
        print(translated)
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
    deepl = DeepLCLI(langs[0], langs[1], timeout=150000, use_dom_submit=False)
    
    
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

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="Translate a file from one language to another")

    parser.add_argument("--filename", dest="filename", required=True, help="The path to the input file")
    parser.add_argument("--out-filename", dest="out_filename", required=True, help="The path to the output file")
    parser.add_argument("--from_lang", dest="from_lang", required=True, help="The language to translate from")
    parser.add_argument("--to_lang", dest="to_lang", required=True, help="The language to translate to")

    args = parser.parse_args(sys.argv[1:])
    
    translate_file(args.filename, args.out_filename, langs=[args.from_lang, args.to_lang])
    
    