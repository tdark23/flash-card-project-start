from tkinter import *
import pandas as pd
import random

BACKGROUND_COLOR = "#B1DDC6"
FONT_NAME = "Arial"
DELAY = 4000

flashcards = []

# ------------------- GETTING DATAS MECHANISM ----------------------- #

# Check if words_to_learn.csv file exists
try:
    data_to_learn = pd.read_csv("./data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pd.read_csv("./data/french_words.csv")
    df = pd.DataFrame(original_data)
    flashcards = df.to_dict(orient="records")
else:
    # Creating the dataframe
    df = pd.DataFrame(data_to_learn)
    # Generating a list of records using to_dict
    flashcards = df.to_dict(orient="records")


# ----------------- NEXT CARD MECHANISM -------------------- #

current_card = None

def next_card():
    global current_card, flip_timer, words_to_learn

    # invalidate the previous delay
    window.after_cancel(flip_timer)

    # getting the current card dict
    current_card = random.choice(flashcards)
    # update the card title 
    canvas.itemconfig(card_title, text="English", fill="black")
    # get the english word
    canvas.itemconfig(card_word, text=current_card["English"], fill="black")
    # show the front of the card
    canvas.itemconfig(card_image, image=card_front)

    # schedule the flip_card function to run after a delay
    flip_timer = window.after(DELAY, flip_card)

    # remove the current word from the words to learn list
    flashcards.remove(current_card)
    # creating a new dataframe
    new_df = pd.DataFrame(flashcards)
    # save the words into a new csv file
    new_df.to_csv("./data/words_to_learn.csv", index=False)



# ----------- FLIP CARD MECHANISM ------------- #

def flip_card():
    # show the back of the card
    canvas.itemconfig(card_image, image=card_back)
    # get the French word
    canvas.itemconfig(card_title, text="French", fill="white")
    canvas.itemconfig(card_word, text=current_card["French"], fill="white")

# ----------------- UI CONF ------------------ #


window = Tk()
window.config(padx=50, pady=50, background=BACKGROUND_COLOR)
window.title("Flashy")

flip_timer = window.after(DELAY, func=flip_card)

card_front = PhotoImage(file="./images/card_front.png")
card_back = PhotoImage(file="./images/card_back.png")

canvas = Canvas(width=800, height=526, highlightthickness=0, background=BACKGROUND_COLOR)

card_image = canvas.create_image(400, 263, image=card_front)
card_title = canvas.create_text(400, 150, text="", font=(FONT_NAME, 40, "italic"))
card_word = canvas.create_text(400, 263, text="", font=(FONT_NAME, 60, "bold"))

canvas.grid(column=0, row=0, columnspan=2)

wrong_button = PhotoImage(file="./images/wrong.png")
right_button = PhotoImage(file="./images/right.png")

check_button = Button(image=right_button, highlightthickness=0, command=next_card)
w_button = Button(image=wrong_button, highlightthickness=0, command=next_card)

w_button.grid(column=0, row=1)
check_button.grid(column=1, row=1)

next_card()


window.mainloop()