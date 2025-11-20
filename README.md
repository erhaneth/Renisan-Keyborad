# Renîsan: Kurmanji Predictive Keyboard 

**Renîsan** is a custom iOS Keyboard Extension built from scratch to support the **Kurmanji** dialect of Kurdish. It features a custom UI layout with specific Kurdish characters (`ê`, `û`, `ş`, `î`, `ç`) and an on-device N-gram language model for real-time next-word prediction and autocomplete.

##  Features

  * **Custom Layout:** Replicates the native iOS QWERTY layout but integrates essential Kurmanji characters.
  * **Native Look & Feel:** Matches Apple's system colors, fonts, and key shadows (Light Mode).
  * **Predictive Engine:** A probabilistic N-gram model trained on 4+ million words of Kurmanji text.
  * **Stupid Backoff Logic:** Intelligently falls back from 5-gram to unigram contexts to find the best suggestion.
  * **Privacy Focused:** The prediction engine runs entirely offline (on-device). No data is sent to the cloud.

-----

##  Architecture

The project is split into two distinct phases: the **Python NLP Backend** (Model Training) and the **Swift iOS Frontend** (App & Keyboard).

### Phase 1: Python Backend (NLP & Data Science)

We used Python to process raw text data into a statistical model that the iPhone can understand.

  * **Data Source:** [Pewan Corpus](https://github.com/klpp/pewan) (4.1 Million words of Kurmanji news articles).
  * **Libraries:** `KLPT` (Kurdish Language Processing Toolkit) for cleaning/normalization and `NLTK` for tokenization.
  * **Algorithm:** We generated counts for **1-grams through 5-grams**.
  * **Optimization:** To fit within the strict **30MB RAM limit** of an iOS keyboard extension, we wrote an optimization script that:
    1.  **Thresholding:** Removed sequences appearing fewer than 10 times.
    2.  **Probability:** Converted raw counts into pre-calculated probabilities.
    3.  **Pruning:** Removed punctuation and non-Kurdish artifacts.

### Phase 2: iOS Frontend (Swift)

The iOS Keyboard Extension reads the optimized model and renders the UI.

  * **Engine (`PredictionEngine.swift`):** Loads the JSON model into memory and queries it using "Stupid Backoff" logic. It handles both **Next Word Prediction** (when space is typed) and **Autocomplete** (filtering suggestions by the current partial word).
  * **UI (`KeyboardViewController.swift`):** A programmatic UIKit implementation using nested `UIStackViews` to handle the keyboard rows, suggestion bar, and button actions.

-----

## 📂 Project Structure

```text
Renîsan/
├── Python_Backend/
│   ├── kurmanji_corpus.txt         # Raw text data (4M+ words)
│   ├── train_model.py              # Generates raw N-gram counts
│   ├── optimize_model.py           # Filters noise & calculates probabilities
│   └── kurmanji_model_optimized.json # THE BRAIN (Final output)
│
├── Renisan/                        # iOS Container App
│   └── ...
│
└── RenisanBoard/                   # Keyboard Extension Source
    ├── KeyboardViewController.swift # The UI and Key Logic
    ├── PredictionEngine.swift       # The Logic (Model Reader)
    ├── kurmanji_model_optimized.json # Imported Brain
    └── Info.plist
```

-----

##  How the Prediction Works

The engine uses a **Stupid Backoff** approach. When the user types `ser navê`:

1.  **5-gram Check:** Does the model have a prediction for the last 4 words? *(No match)*
2.  **Backoff:** Drop the first word.
3.  **3-gram Check:** Does the model know what comes after `ser navê`?
      * *Match Found\!* -\> `xwe` (Probability: 13%).
4.  **Filter:** If the user starts typing `x`, the engine filters the list to show only words starting with `x`.

-----

##  Setup & Installation

### Prerequisites

  * **Python 3.9+**
  * **Xcode 15+**
  * **iOS Simulator** (iPhone 15/16 Pro recommended)

### 1\. Generate the Model (Python)

If you want to retrain the brain from scratch:

```bash
# Install dependencies
pip install nltk klpt

# Run training (Generates huge JSON)
python train_model.py

# Run optimization (Generates iOS-ready JSON)
python optimize_model.py
```

### 2\. Build the iOS App

1.  Open `Renisan.xcodeproj` in Xcode.
2.  Ensure `kurmanji_model_optimized.json` is inside the **RenisanBoard** group and checked for **Target Membership**.
3.  Select the **Renisan** scheme and a Simulator.
4.  Press **Cmd + R** to run.

### 3\. Enable the Keyboard

1.  In the Simulator, go to **Settings \> General \> Keyboard \> Keyboards**.
2.  Tap **Add New Keyboard...** and select **Renisan**.
3.  Open Messages, long-press the 🌐 icon, and select **RenisanBoard**.

-----

##  Future Roadmap

  * [ ] **Shift/Caps Logic:** Better handling of capitalization states.
  * [ ] **Autocorrect:** Implementing Levenshtein distance to fix typos.
  * [ ] **Pan-Kurdish Corpus:** Adding data from Bakur (North) and Rojava (West) to reduce dialect bias.
  * [ ] **Number Row:** Adding a swipe-down gesture for numbers.

-----

##  License & Credits

  * **Corpus:** Pewan Corpus (Project for Kurdish Language Processing).
  * **Tools:** Built using NLTK and KLPT.

-----

*Built with ❤️ for the Kurdish language.*
