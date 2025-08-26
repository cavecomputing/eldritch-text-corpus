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
    seen_chunks = set()  # Track seen content to prevent duplicates
    
    # Process paragraphs in pairs, stepping by 2 to avoid overlap
    for i in range(0, len(paragraphs)-1, 2):
        para1 = paragraphs[i].strip()
        para2 = paragraphs[i+1].strip() if i+1 < len(paragraphs) else ""
        
        # Only proceed if both paragraphs have reasonable content
        if len(para1) > 50 and len(para2) > 50:
            chunk = para1 + "\n\n" + para2
            
            # Check for duplicates using a hash of the content
            chunk_hash = hash(chunk.lower().strip())
            if chunk_hash not in seen_chunks:
                paragraphChunks.append(chunk)
                seen_chunks.add(chunk_hash)
                total_tokens += count_tokens(chunk)
    
    numberOfExamples = len(paragraphChunks)
    print(f'Got {numberOfExamples} examples from text. Total training tokens: {total_tokens:,}')
    
    trainingData = []
    for chunk in paragraphChunks:
        example = {
            "text": chunk
        }
        trainingData.append(example)
    
    with open(f'training.jsonl', 'a', encoding='UTF-8') as f:
        for example in trainingData:
            f.write(json.dumps(example, ensure_ascii=False) + '\n')

if __name__ == "__main__":
    main()
