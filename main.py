from tkinter import *
import pandas
import random

try:
    data_frame = pandas.read_csv('data/words_to_learn.csv').to_dict(orient='records')
except FileNotFoundError:
    data_frame = pandas.read_csv('data/french_words.csv').to_dict(orient='records')

current_card = {}


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(data_frame)
    canvas.itemconfig(card_title, text='French', fill='black')
    canvas.itemconfig(card_word, text=current_card['French'], fill='black')
    canvas.itemconfig(card_image, image=flash_card_front_image)
    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    canvas.itemconfig(card_title, text='English', fill='white')
    canvas.itemconfig(card_word, text=current_card['English'], fill='white')
    canvas.itemconfig(card_image, image=flash_card_back_image)


def is_known():
    global data_frame
    data_frame.remove(current_card)
    to_learn = pandas.DataFrame(data_frame)
    to_learn.to_csv('data/words_to_learn.csv', index=False)
    next_card()


BACKGROUND_COLOR = "#B1DDC6"

window = Tk()
window.title('flashy')
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

right_image = PhotoImage(file=r'images\right.png')
right_button = Button(image=right_image, highlightthickness=0, command=is_known)
right_button.grid(column=1, row=1)

wrong_image = PhotoImage(file=r'images\wrong.png')
wrong_button = Button(image=wrong_image, highlightthickness=0, command=next_card)
wrong_button.grid(column=0, row=1)

flash_card_front_image = PhotoImage(file=r'images\card_front.png')
flash_card_back_image = PhotoImage(file=r'images\card_back.png')

canvas = Canvas(width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)
card_image = canvas.create_image(400, 263, image=flash_card_front_image)
card_title = canvas.create_text(400, 150, text='', font=('Arial', 40, 'italic'))
card_word = canvas.create_text(400, 263, text='', font=('Arial', 60, 'bold'))
canvas.grid(row=0, column=0, columnspan=2)

next_card()

window.mainloop()
