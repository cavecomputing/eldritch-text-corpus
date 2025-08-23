import argparse
import json
import os
import tiktoken

# Get source file path through argument
parser = argparse.ArgumentParser()
parser.add_argument('sourceFile')
args = parser.parse_args()

def extractText(file):
    with open(file, 'r', encoding='UTF-8') as file:
        text = file.read()
        return text.split('\n\n')

def count_tokens(text):
    """Accurate token counting using tiktoken"""
    enc = tiktoken.get_encoding("cl100k_base")  # GPT-4 tokenizer
    return len(enc.encode(text))
    
def main():
    # Get just the filename with extension
    source_filename = os.path.basename(args.sourceFile)
    
    paragraphs = extractText(args.sourceFile)
    paragraphChunks = []
    total_tokens = 0
    
    for i in range(len(paragraphs)-1):
        chunk = paragraphs[i].strip() + '\n\n' + paragraphs[i+1].strip()
        if len(chunk) > 100:
            paragraphChunks.append(chunk)
            total_tokens += count_tokens(chunk)
    
    numberOfExamples = len(paragraphChunks)
    print(f'Got {numberOfExamples} examples from text. Total training tokens: {total_tokens:,}')
    
    trainingData = []
    for chunk in paragraphChunks:
        example = {
            "messages": [
                {"role": "assistant", "content": chunk}
            ],
            "source_file": source_filename  # Add the filename here
        }
        trainingData.append(example)
    
    with open(f'training.jsonl', 'a', encoding='UTF-8') as f:
        for example in trainingData:
            f.write(json.dumps(example, ensure_ascii=False) + '\n')

if __name__ == "__main__":
    main()
