import tkinter as tk
import random
from tkinter import messagebox

# Game settings
rows = 4
cols = 4
time_limit = 60

symbols = ['🍎','🍌','🍇','🍒','🥝','🍉','🍍','🍑'] * 2
random.shuffle(symbols)

first_card = None
second_card = None
buttons = []
matched = 0
time_left = time_limit


def flip_card(r, c):
    global first_card, second_card

    button = buttons[r][c]

    if button["text"] != "":
        return

    index = r * cols + c
    button["text"] = symbols[index]

    if first_card is None:
        first_card = (r, c)

    elif second_card is None:
        second_card = (r, c)
        root.after(500, check_match)


def check_match():
    global first_card, second_card, matched

    r1, c1 = first_card
    r2, c2 = second_card

    i1 = r1 * cols + c1
    i2 = r2 * cols + c2

    if symbols[i1] == symbols[i2]:
        matched += 2
    else:
        buttons[r1][c1]["text"] = ""
        buttons[r2][c2]["text"] = ""

    first_card = None
    second_card = None

    if matched == len(symbols):
        messagebox.showinfo("Congratulations", "You won the game!")


def countdown():
    global time_left

    if time_left > 0:
        time_left -= 1
        timer_label.config(text=f"Time Left: {time_left}s")
        root.after(1000, countdown)
    else:
        messagebox.showinfo("Game Over", "Time's up!")
        root.destroy()


# GUI Window
root = tk.Tk()
root.title("Memory Puzzle Game")

timer_label = tk.Label(root, text=f"Time Left: {time_limit}s", font=("Arial", 14))
timer_label.grid(row=0, column=0, columnspan=cols)

# Create grid
for r in range(rows):
    row_buttons = []
    for c in range(cols):
        btn = tk.Button(root, text="", width=8, height=4,
                        command=lambda r=r, c=c: flip_card(r, c))
        btn.grid(row=r+1, column=c)
        row_buttons.append(btn)

    buttons.append(row_buttons)

countdown()

root.mainloop()