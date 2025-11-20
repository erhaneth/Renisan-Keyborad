import nltk
from nltk.util import ngrams
from collections import defaultdict
import json
import os
from klpt.preprocess import Preprocess 
# Note: We replaced Counter with defaultdict(int) for cleaner nesting

# --- Configuration ---
CORPUS_FILE = 'kurmanji_corpus.txt' 
MODEL_OUTPUT_FILE = 'kurmanji_ngram_model.json' 
MAX_N = 5 # Generate counts up to 5-grams
# ---------------------

def train_ngram_model(file_path, max_n):
    """Loads, cleans, and generates N-gram counts for the Kurmanji corpus."""
    print(f"1. Starting N-gram model training from: {file_path}")
    
    if not os.path.exists(file_path):
        print(f"ERROR: Corpus file not found at {file_path}. Please download the file!")
        return None

    # 1. Initialize Kurdish Preprocessor
    preprocessor = Preprocess(dialect="Kurmanji", script="Latin")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        raw_text = f.read()

    # 2. Preprocessing & Tokenization
    print("2. Cleaning and tokenizing text...")
    
    normalized_text = preprocessor.standardize(raw_text) 
    tokens = nltk.word_tokenize(normalized_text.lower()) 
    
    # 3. Generate N-gram counts: Using a standard dict mapping N to the count structure
    ngram_counts = {}
    
    for n in range(1, max_n + 1):
        print(f"   -> Processing {n}-grams...")
        
        # Unigrams (N=1) are handled as simple counts
        if n == 1:
            unigram_counts = defaultdict(int)
            for gram in ngrams(tokens, 1):
                unigram_counts[gram[0]] += 1
            ngram_counts[str(n)] = dict(unigram_counts)
        
        # Higher-order N-grams (N > 1) are handled as prefix -> {next_word: count}
        else:
            n_gram_map = defaultdict(lambda: defaultdict(int))
            for gram in ngrams(tokens, n):
                prefix = " ".join(gram[:-1]) # Join prefix words into a single string key
                word = gram[-1]
                n_gram_map[prefix][word] += 1
            
            # Convert inner defaultdicts to regular dicts for JSON output
            final_map = {k: dict(v) for k, v in n_gram_map.items()}
            ngram_counts[str(n)] = final_map

    print(f"3. Training complete. Generated counts up to {max_n}-grams.")
    
    return ngram_counts

# --- EXECUTION ---
print("--- Training Started ---")
model_data = train_ngram_model(CORPUS_FILE, MAX_N)

if model_data:
    # 4. Save the N-gram data to a JSON file
    print(f"4. Saving model data to {MODEL_OUTPUT_FILE}...")
    with open(MODEL_OUTPUT_FILE, 'w', encoding='utf-8') as f:
        # Saving with indentation for readability, but use json.dump(model_data, f) for production speed
        json.dump(model_data, f, ensure_ascii=False, indent=4)
    print("5. Model data saved successfully! File is ready for iOS integration.")