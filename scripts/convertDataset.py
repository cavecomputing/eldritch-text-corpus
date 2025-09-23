import argparse
import json
import os
import glob
import tiktoken

# Enhanced argument parsing
parser = argparse.ArgumentParser(description='Convert text documents to training dataset')
parser.add_argument('--texts-dir', default='texts', help='Path to texts directory (default: texts)')
parser.add_argument('--authors', nargs='*', help='Specific author folders to include (default: all)')
parser.add_argument('--output', default='eldritch-text-corpus.jsonl', help='Output file name')
parser.add_argument('--min-length', type=int, default=50, help='Minimum character length for each paragraph (default: 50)')
args = parser.parse_args()

def extractText(file):
    with open(file, 'r', encoding='UTF-8') as file:
        text = file.read()
        return text.split('\n\n')

def count_tokens(text):
    """Accurate token counting using tiktoken"""
    enc = tiktoken.get_encoding("cl100k_base")  # GPT-4 tokenizer
    return len(enc.encode(text))
    
def get_text_files():
    """Get all .txt files from specified authors or all authors"""
    text_files = []
    
    if args.authors:
        # Process specific authors
        for author in args.authors:
            author_path = os.path.join(args.texts_dir, author)
            if os.path.isdir(author_path):
                pattern = os.path.join(author_path, "*.txt")
                text_files.extend(glob.glob(pattern))
                print(f"Found {len(glob.glob(pattern))} files for {author}")
            else:
                print(f"Warning: Author directory '{author}' not found")
    else:
        # Process all authors
        pattern = os.path.join(args.texts_dir, "*", "*.txt")
        text_files = glob.glob(pattern)
        authors = set(os.path.basename(os.path.dirname(f)) for f in text_files)
        print(f"Processing all authors: {', '.join(sorted(authors))}")
    
    return text_files

def main():
    text_files = get_text_files()
    
    if not text_files:
        print("No text files found!")
        return
    
    print(f"Processing {len(text_files)} text files...")
    
    all_chunks = []
    total_tokens = 0
    seen_chunks = set()  # Track seen content to prevent duplicates
    
    for file_path in text_files:
        print(f"Processing: {os.path.relpath(file_path)}")
        paragraphs = extractText(file_path)
        file_chunks = 0
        
        # Process paragraphs in pairs, stepping by 2 to avoid overlap
        for i in range(0, len(paragraphs)-1, 2):
            para1 = paragraphs[i].strip()
            para2 = paragraphs[i+1].strip() if i+1 < len(paragraphs) else ""
            
            # Only proceed if both paragraphs have reasonable content
            if len(para1) > args.min_length and len(para2) > args.min_length:
                chunk = para1 + "\n\n" + para2
                
                # Check for duplicates using a hash of the content
                chunk_hash = hash(chunk.lower().strip())
                if chunk_hash not in seen_chunks:
                    all_chunks.append(chunk)
                    seen_chunks.add(chunk_hash)
                    tokens = count_tokens(chunk)
                    total_tokens += tokens
                    file_chunks += 1
        
        print(f"  → {file_chunks} chunks extracted")
    
    numberOfExamples = len(all_chunks)
    print(f'\nDataset Summary:')
    print(f'Total examples: {numberOfExamples:,}')
    print(f'Total training tokens: {total_tokens:,}')
    print(f'Output file: {args.output}')
    
    # Clear output file if it exists
    if os.path.exists(args.output):
        os.remove(args.output)
    
    trainingData = []
    for chunk in all_chunks:
        example = {
            "text": chunk
        }
        trainingData.append(example)
    
    with open(args.output, 'w', encoding='UTF-8') as f:
        for example in trainingData:
            f.write(json.dumps(example, ensure_ascii=False) + '\n')

if __name__ == "__main__":
    main()
