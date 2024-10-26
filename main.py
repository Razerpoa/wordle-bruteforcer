import nltk
import tkinter as tk
from tkinter import simpledialog, messagebox, font

# Constants
INDONESIAN_WORD_LIST_FILE = '00-indonesian-wordlist.txt'
ENGLISH_WORD_LIST_FILE = 'en-wordle-list.txt'
FONT_FAMILY = "Helvetica"
FONT_SIZE = 12
FONT_WEIGHT = "bold"
BG_COLOR = "#eee"
FG_COLOR = "#333"
TEXT_BG_COLOR = "#fff"
TEXT_FG_COLOR = "#000"
BUTTON_BG_COLOR = {
    "submit": "#4CAF50",
    "reset": "#f44336"
}
BUTTON_FG_COLOR = "white"
MAX_CANDIDATE_WORDS = 10
ENTRY_WIDTH = 15
RESULT_TEXT_HEIGHT = 10
RESULT_TEXT_WIDTH = 40
INFO_TEXT_HEIGHT = 5
INFO_TEXT_WIDTH = 40

# Download the words dataset if you haven't already
nltk.download('words')

# Load the word list from the file without filtering
with open(ENGLISH_WORD_LIST_FILE, 'r', encoding='UTF-8') as f:
    english_word_list = [word.strip().lower() for word in f]

# Continue filtering the Indonesian word list
with open(INDONESIAN_WORD_LIST_FILE, 'r', encoding='UTF-8') as f:
    indonesian_word_list = [word.strip().lower() for word in f if len(word.strip()) == 5]

def get_matching_words(correct_positions, yellow_letters, wrong_letters, word_list):
    matching_words = []
    for word in word_list:
        if matches(word, correct_positions, yellow_letters, wrong_letters):
            matching_words.append(word)
    return matching_words

def matches(candidate_word, correct_positions, yellow_letters, wrong_letters):
    for i, char in enumerate(correct_positions):
        if char is not None and candidate_word[i] != char:
            return False
    for char, positions in yellow_letters.items():
        if char not in candidate_word:
            return False
        for pos in positions:
            if candidate_word[pos] == char:
                return False
    return all(char not in candidate_word for char in wrong_letters)

class WordleHelper:
    def __init__(self, root):
        self.root = root
        self.correct_positions = [None] * 5
        self.yellow_letters = {}
        self.wrong_letters = set()
        
        self.custom_font = font.Font(family=FONT_FAMILY, size=FONT_SIZE, weight=FONT_WEIGHT)
        
        # Simplify language selection
        self.language = simpledialog.askstring("Language", "Choose language (en for English, id for Indonesian):").lower()
        self.word_list = english_word_list if self.language == 'en' else indonesian_word_list
        messagebox.showinfo("Language", f"{'English' if self.language == 'en' else 'Indonesian'} mode selected.")
        
        self.create_widgets()

    def create_widgets(self):
        frame = tk.Frame(self.root, bg=BG_COLOR)
        frame.grid(row=0, column=0, columnspan=4, padx=2, pady=2, sticky='w')
        
        tk.Label(frame, text="Word:", font=self.custom_font, fg=FG_COLOR, bg=BG_COLOR).pack(side=tk.LEFT)
        self.word_entry = tk.Entry(frame, width=ENTRY_WIDTH, font=self.custom_font)
        self.word_entry.pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Label(frame, text="Match:", font=self.custom_font, fg=FG_COLOR, bg=BG_COLOR).pack(side=tk.LEFT)
        self.match_entry = tk.Entry(frame, width=ENTRY_WIDTH, font=self.custom_font)
        self.match_entry.pack(side=tk.LEFT)
        
        self.submit_button = tk.Button(frame, text="Submit", font=self.custom_font, command=self.submit_guess, 
                                       bg=BUTTON_BG_COLOR["submit"], fg=BUTTON_FG_COLOR)
        self.submit_button.pack(side=tk.LEFT, padx=(10, 5))
        # Bind Enter key to the submit button when focused
        self.submit_button.bind('<Return>', lambda event: self.submit_guess())
        
        self.reset_button = tk.Button(frame, text="Reset", font=self.custom_font, command=self.reset_game, 
                                      bg=BUTTON_BG_COLOR["reset"], fg=BUTTON_FG_COLOR)
        self.reset_button.pack(side=tk.LEFT)
        # Bind Enter key to the reset button when focused
        self.reset_button.bind('<Return>', lambda event: self.reset_game())
        
        self.text_area = tk.Text(self.root, height=RESULT_TEXT_HEIGHT + INFO_TEXT_HEIGHT - 4, 
                                 width=RESULT_TEXT_WIDTH, font=self.custom_font, bg=TEXT_BG_COLOR, fg=TEXT_FG_COLOR)
        self.text_area.grid(row=1, column=0, columnspan=4, padx=2, pady=5)
        self.text_area.config(state=tk.DISABLED)

        self.root.grid_columnconfigure(0, weight=1)

        # Bind the Enter key to the submit_guess method globally
        self.root.bind('<Return>', lambda event: self.submit_guess())

        # Bind Shift+Enter to the reset_game method globally
        self.root.bind('<Shift-Return>', lambda event: self.reset_game())

    def submit_guess(self):
        input_word = self.word_entry.get().lower()
        if input_word == 'exit':
            self.root.destroy()
            return
        if input_word == 'win':
            self.reset_game()
            return
        
        match_info = self.match_entry.get().lower()
        for i, (char, info) in enumerate(zip(input_word, match_info)):
            if info == 'g':
                self.correct_positions[i] = char
            elif info == 'y':
                if char not in self.yellow_letters:
                    self.yellow_letters[char] = set()
                self.yellow_letters[char].add(i)
            elif info == 'b' and char not in self.correct_positions and char not in self.yellow_letters:
                self.wrong_letters.add(char)
        
        matching_words = get_matching_words(self.correct_positions, self.yellow_letters, self.wrong_letters, self.word_list)
        
        self.text_area.config(state=tk.NORMAL)
        self.text_area.delete(1.0, tk.END)
        if matching_words:
            self.text_area.insert(tk.END, "Matching words:\n")
            for word in matching_words:  # Removed the slicing [:MAX_CANDIDATE_WORDS]
                self.text_area.insert(tk.END, word + "\n")
        else:
            self.text_area.insert(tk.END, "No matching words found.\n")
        
        self.text_area.insert(tk.END, f"\nCorrect: {self.correct_positions}\n")
        self.text_area.insert(tk.END, f"Yellow: {self.yellow_letters}\n")
        self.text_area.insert(tk.END, f"Wrong: {', '.join(self.wrong_letters)}\n")
        self.text_area.config(state=tk.DISABLED)
        
    def reset_game(self):
        self.correct_positions = [None] * 5
        self.yellow_letters = {}
        self.wrong_letters = set()
        self.text_area.config(state=tk.NORMAL)
        self.text_area.delete(1.0, tk.END)
        self.text_area.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Wordle Helper")
    root.configure(bg=BG_COLOR)
    app = WordleHelper(root)
    root.mainloop()
