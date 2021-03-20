from tkinter import *
import pandas as pd
import random
import time

BACKGROUND_COLOR = "#B1DDC6"

# --------------------------------- DATAFRAME ---------------------------------------- #

words_df = pd.read_csv("./data/french_words.csv")
learn_french = words_df.to_dict(orient="records")
current_card = {}
word_to_learn = {}

# --------------------------------- BUTTON FUNCTIONS ---------------------------------------- #
def know_word():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(learn_french)
    canvas.itemconfig(card_image, image=card_front_img)
    canvas.itemconfig(title_text, text="FRENCH", fill="black")
    canvas.itemconfig(word_text, text=current_card["French"], fill="black")
    flip_timer = window.after(3000, flip_card)


def unknown_word():
    global current_card, flip_timer, word_to_learn
    window.after_cancel(flip_timer)
    current_card = random.choice(learn_french)
    canvas.itemconfig(card_image, image=card_front_img)
    canvas.itemconfig(title_text, text="FRENCH", fill="black")
    canvas.itemconfig(word_text, text=current_card["French"], fill="black")
    flip_timer = window.after(3000, flip_card)
    word_to_learn[current_card["French"]] = current_card["English"]
    # print(type(word_to_learn.items()))
    word_to_learn_df = pd.DataFrame(list(word_to_learn.items()), columns=['FRENCH', 'ENGLISH'])
    word_to_learn_df.to_csv("word_to_learn.csv")

def flip_card():
    canvas.itemconfig(card_image, image=card_back_img)
    canvas.itemconfig(title_text, text="English", fill="white")
    canvas.itemconfig(word_text, text=current_card["English"], fill="white")


# --------------------------------- UI ---------------------------------------- #
window = Tk()
window.title("Flash Cards")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, flip_card)

# canvas
canvas = Canvas(width=800, height=526, highlightthickness=0)
card_back_img = PhotoImage(file="./images/card_back.png")
card_front_img = PhotoImage(file="./images/card_front.png")
card_image = canvas.create_image(400, 263, image=card_front_img)
canvas.config(bg=BACKGROUND_COLOR)
canvas.grid(column=0, row=1, columnspan=2)

# label with canvas
title_text = canvas.create_text(400, 140, text="", font=("Ariel", 40, "italic"))
word_text = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))

# right and wrong
right_img = PhotoImage(file="./images/right.png")
wrong_img = PhotoImage(file="./images/wrong.png")
right_button = Button(image=right_img, highlightthickness=0, command=know_word)
right_button.grid(column=1, row=2)

wrong_button = Button(image=wrong_img, highlightthickness=0, command=unknown_word)
wrong_button.grid(column=0, row=2)

know_word()
# window close
window.mainloop()
