import json
from collections import defaultdict

# --- Configuration ---
RAW_MODEL_FILE = 'kurmanji_ngram_model.json'
OPTIMIZED_MODEL_FILE = 'kurmanji_model_optimized.json'
THRESHOLD = 3  # N-grams occurring less than 3 times will be removed.
ALPHA = 0.4    # Stupid BackOff (SBO) coefficient (for conceptual use here).

def optimize_and_calculate_probabilities(raw_model_file, optimized_file, threshold, alpha):
    """
    1. Removes low-frequency N-grams (thresholding).
    2. Converts raw counts into probabilities P(W_n | Prefix).
    """
    print(f"1. Loading raw model from: {raw_model_file}")
    with open(raw_model_file, 'r', encoding='utf-8') as f:
        model = json.load(f)

    optimized_model = {}

    # --- Process N-grams (N=1 to N=5) ---
    for n_str in sorted(model.keys(), key=int):
        n = int(n_str)
        print(f"2. Optimizing and calculating probabilities for {n}-grams (Threshold={threshold})...")
        
        n_map = model[n_str]
        optimized_n_map = {}

        for prefix, next_word_counts in n_map.items():
            
            # --- Thresholding ---
            # Remove all sequences that occurred less than the threshold
            if isinstance(next_word_counts, dict):
                 # For N > 1 (prefix: {word: count})
                filtered_counts = {word: count for word, count in next_word_counts.items() if count >= threshold}
            else:
                 # For N = 1 (word: count)
                if next_word_counts >= threshold:
                    optimized_n_map[prefix] = next_word_counts
                continue
            
            if not filtered_counts:
                continue

            # --- Probability Calculation ---
            # Prefix count is the sum of all its next_word_counts.
            prefix_count = sum(filtered_counts.values())

            if prefix_count > 0:
                probability_map = {}
                for word, count in filtered_counts.items():
                    # Calculate raw probability P(W_n | Prefix)
                    raw_prob = count / prefix_count
                    probability_map[word] = raw_prob
                
                # Sort the suggestions by probability (descending) before saving.
                sorted_probs = dict(sorted(probability_map.items(), key=lambda item: item[1], reverse=True))
                
                optimized_n_map[prefix] = sorted_probs


        optimized_model[n_str] = optimized_n_map


    # --- 3. Save the Optimized Model ---
    print(f"3. Saving optimized model to {optimized_file}...")
    with open(optimized_file, 'w', encoding='utf-8') as f:
        # Use simple JSON dump for speed; don't use indent=4, as the file is large
        json.dump(optimized_model, f, ensure_ascii=False)
    print("4. Optimization complete. The model is now ready for efficient Swift loading!")
    return optimized_model


# --- EXECUTION ---
optimize_and_calculate_probabilities(RAW_MODEL_FILE, OPTIMIZED_MODEL_FILE, THRESHOLD, ALPHA)