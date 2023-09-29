from tkinter import *
import pandas as pd
import random

class FlashcardApp:
    def __init__(self, window):
        self.window = window
        self.window.config(padx=50, pady=50, background=BACKGROUND_COLOR)
        self.window.title("Flashy")

        self.flashcards = []
        self.current_card = None
        self.flip_timer = None

        self.card_front = PhotoImage(file="./images/card_front.png")
        self.card_back = PhotoImage(file="./images/card_back.png")

        self.canvas = Canvas(width=800, height=526, highlightthickness=0, background=BACKGROUND_COLOR)
        self.card_image = self.canvas.create_image(400, 263, image=self.card_front)
        self.card_title = self.canvas.create_text(400, 150, text="", font=(FONT_NAME, 40, "italic"))
        self.card_word = self.canvas.create_text(400, 263, text="", font=(FONT_NAME, 60, "bold"))
        self.canvas.grid(column=0, row=0, columnspan=2)

        self.wrong_button = PhotoImage(file="./images/wrong.png")
        self.right_button = PhotoImage(file="./images/right.png")

        self.check_button = Button(image=self.right_button, highlightthickness=0, command=self.next_card)
        self.w_button = Button(image=self.wrong_button, highlightthickness=0, command=self.next_card)

        self.w_button.grid(column=0, row=1)
        self.check_button.grid(column=1, row=1)

        self.load_flashcards()
        self.next_card()

    def load_flashcards(self):
        try:
            data_to_learn = pd.read_csv("./data/words_to_learn.csv")
        except FileNotFoundError:
            original_data = pd.read_csv("./data/french_words.csv")
            df = pd.DataFrame(original_data)
            self.flashcards = df.to_dict(orient="records")
        else:
            df = pd.DataFrame(data_to_learn)
            self.flashcards = df.to_dict(orient="records")

    def next_card(self):
        if self.flashcards:
            self.window.after_cancel(self.flip_timer)
            self.current_card = random.choice(self.flashcards)
            self.canvas.itemconfig(self.card_title, text="English", fill="black")
            self.canvas.itemconfig(self.card_word, text=self.current_card["English"], fill="black")
            self.canvas.itemconfig(self.card_image, image=self.card_front)
            self.flip_timer = self.window.after(DELAY, self.flip_card)
            self.flashcards.remove(self.current_card)
            new_df = pd.DataFrame(self.flashcards)
            new_df.to_csv("./data/words_to_learn.csv", index=False)

    def flip_card(self):
        self.canvas.itemconfig(self.card_image, image=self.card_back)
        self.canvas.itemconfig(self.card_title, text="French", fill="white")
        self.canvas.itemconfig(self.card_word, text=self.current_card["French"], fill="white")

if __name__ == "__main__":
    BACKGROUND_COLOR = "#B1DDC6"
    FONT_NAME = "Arial"
    DELAY = 4000

    window = Tk()
    app = FlashcardApp(window)
    window.mainloop()