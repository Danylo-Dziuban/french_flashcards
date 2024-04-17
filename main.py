import tkinter as tk
import pandas as pd
import random
import os

# ------------------------------------------------------Variables----------------------------------------------------- #
window = tk.Tk()

BG_COLOR = '#B1DDC6'
FONT_TOP = ('Ariel', 40, 'italic')
FONT_BOTTOM = ('Ariel', 60, 'bold')
canvas_front_img = tk.PhotoImage(file='images/card_front.png')
canvas_back_img = tk.PhotoImage(file='images/card_back.png')
cross_image = tk.PhotoImage(file='images/wrong.png')
tick_image = tk.PhotoImage(file='images/right.png')

english = ''
french = ''


try:
    kw = open('data/unknown_words.csv')

except:
    data = pd.read_csv('data/french_words.csv')

else:
    kw.close()
    if os.path.getsize('data/unknown_words.csv') > 0:
        data = pd.read_csv('data/unknown_words.csv')

    else:
        data = pd.read_csv('data/french_words.csv')

# ------------------------------------------------------Commands------------------------------------------------------ #


def card_text_action():
    global french, english

    french = random.choice((data['French']).to_list())
    english = data[data.French == french].English.iloc[0]

    card_canvas.itemconfig(card_top_text, text='French', fill='black')
    card_canvas.itemconfig(card_bottom_text, text=french, fill='black')
    card_canvas.itemconfig(card_background_img, image=canvas_front_img)

    window.after(3000, update_card_back)


def update_card_back():
    global english

    card_canvas.itemconfig(card_top_text, text='English', fill='white')
    card_canvas.itemconfig(card_bottom_text, text=english, fill='white')
    card_canvas.itemconfig(card_background_img, image=canvas_back_img)


def handle_unknown():
    global english, french

    data.to_csv('data/unknown_words.csv', mode='w', index=False)

    card_text_action()


def handle_known():
    global french, english, data

    data = data.drop(data[data.French == french].index)

    print(len(data.to_dict()['French']))

    data.to_csv('data/unknown_words.csv', mode='w', index=False)

    card_text_action()


# ---------------------------------------------------------UI--------------------------------------------------------- #

window.title('Flash Card Program')
window.config(padx=50, pady=50, bg=BG_COLOR)

card_canvas = tk.Canvas(width=800, height=526, highlightthickness=0)
card_canvas.config(bg=BG_COLOR)
card_background_img = card_canvas.create_image(400, 263, image=canvas_front_img)
card_top_text = card_canvas.create_text(400, 150, text='French', font=FONT_TOP)
card_bottom_text = card_canvas.create_text(400, 263, text="Word", font=FONT_BOTTOM)

dont_know_button = tk.Button(image=cross_image, highlightthickness=0, command=handle_unknown)
dont_know_button.grid(row=1, column=0)

know_button = tk.Button(image=tick_image, highlightthickness=0, command=handle_known)
know_button.grid(row=1, column=1)

card_canvas.grid(row=0, column=0, columnspan=2)

card_text_action()

window.mainloop()
