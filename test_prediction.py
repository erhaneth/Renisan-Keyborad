import json
import readline # Optional: makes typing in terminal nicer

# --- Configuration ---
MODEL_FILE = 'kurmanji_model_optimized.json'

def load_model():
    print(f"⏳ Loading model from {MODEL_FILE}...")
    try:
        with open(MODEL_FILE, 'r', encoding='utf-8') as f:
            model = json.load(f)
        print("✅ Model loaded! You can now type in Kurmanji.")
        return model
    except FileNotFoundError:
        print("❌ Error: Optimized model file not found. Did you run optimize_model.py?")
        exit()

def get_suggestions(model, text_input):
    """
    This function simulates the iOS Keyboard logic.
    It takes the user's text and tries to find the best next word.
    """
    # 1. Clean and split the input into words
    tokens = text_input.strip().lower().split()
    
    if not tokens:
        return []

    # 2. Try finding a match, starting with the longest possible sequence (N=5)
    #    We look at the last 4, 3, 2, or 1 words typed.
    
    max_n = 5
    
    # We loop backwards from 5 down to 2
    for n in range(max_n, 1, -1):
        # We need (n-1) previous words to predict the nth word.
        # Example: To use 3-gram model, we need the last 2 words.
        required_history = n - 1
        
        if len(tokens) >= required_history:
            # Grab the last (n-1) words
            history_tokens = tokens[-required_history:]
            
            # Join them to make the key (e.g., "ser navê")
            history_key = " ".join(history_tokens)
            
            # Check if this key exists in the model for this N level
            # Note: keys in JSON are strings "1", "2", "3"...
            if str(n) in model and history_key in model[str(n)]:
                suggestions = model[str(n)][history_key]
                print(f"   (Matched {n}-gram pattern: '{history_key}')")
                return suggestions

    # 3. Fallback: If no sequence matches, check the Unigram (1-gram) model?
    #    Usually, keyboards don't suggest random words if context is unknown, 
    #    but we could return the most common words overall.
    return {}

def main():
    model = load_model()
    
    print("\n--- Kurmanji Prediction Test ---")
    print("Type a phrase and press Enter. Type 'exit' to quit.\n")

    while True:
        user_input = input("📝 Type here: ")
        
        if user_input.lower() in ['exit', 'quit']:
            break
        
        suggestions = get_suggestions(model, user_input)
        
        if suggestions:
            # Get top 3 suggestions
            top_3 = list(suggestions.items())[:3] 
            
            print("🔮 Predictions:")
            for i, (word, prob) in enumerate(top_3, 1):
                # Format probability as a percentage
                print(f"   {i}. {word} \t({prob:.1%} chance)")
        else:
            print("🤷‍♂️ No prediction found (Sequence is rare or unknown).")
        print("-" * 30)

if __name__ == "__main__":
    main()