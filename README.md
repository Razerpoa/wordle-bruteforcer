# Wordle Helper/Bruteforcer

Wordle Helper/Bruteforcer is a Python application designed to assist players in solving Wordle puzzles. It provides suggestions for possible words based on the feedback from previous guesses.

## Features

- Supports both English and Indonesian word lists.
- Interactive GUI built with Tkinter.
- Allows users to input their guesses and receive suggestions for possible words.
- Displays the current state of correct, yellow, and wrong letters.

## Installation

1. **Clone the repository:**

   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Install the required packages:**

   Ensure you have Python installed, then run:

   ```bash
   pip install nltk
   ```

3. **Download the NLTK words dataset:**

   The application requires the NLTK words dataset. You can download it by running the following command in a Python shell:

   ```python
   import nltk
   nltk.download('words')
   ```

4. **Run the application:**

   Execute the main script to start the Wordle Helper:

   ```bash
   python main.py
   ```

## Usage

1. **Select Language:**

   Upon starting the application, you will be prompted to choose a language. Enter `en` for English or `id` for Indonesian.

2. **Input Guesses:**

   - Enter your guessed word in the "Word" field.
   - Enter the feedback in the "Match" field using:
     - `g` for green (correct position),
     - `y` for yellow (correct letter, wrong position),
     - `b` for black (wrong letter).

3. **Submit and Reset:**

   - Click "Submit" to see matching words.
   - Click "Reset" to start a new game.

## Code Overview

- **Word Lists:**
  - English words are loaded from `en-wordle-list.txt`.
  - Indonesian words are loaded from `00-indonesian-wordlist.txt`.

- **Main Components:**
  - `WordleHelper` class: Manages the GUI and game logic.
  - `get_matching_words` function: Filters words based on the current game state.
  - `matches` function: Checks if a word matches the given criteria.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- The word lists are sourced from publicly available datasets.
- The application uses the NLTK library for natural language processing.

