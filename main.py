from tkinter import *
from word_brain import WordBrain
from manager import Manager, FONT, HEADER_TEXT

# Main window
window = Tk()
window.title("Typing Speed Test by Gáspár Németh")
window.geometry("720x500")
window.minsize(width=720, height=500)
window.configure(bg="black")
window.columnconfigure(index=0, weight=1)

# Title label
title_label = Label(text="Typing Speed Test by Gáspár Németh", **HEADER_TEXT)
title_label.grid(column=0, row=0, sticky="w")

# Timer label
timer_label = Label(text="", **HEADER_TEXT, width=15)
timer_label.grid(column=1, row=0)

# Words to type
words_to_type = Text(width=40, height=3, font=FONT, wrap="word", spacing3=12)
words_to_type.grid(column=0, row=1, columnspan=3, sticky="ew", padx=10)

# Reset button
reset_button = Button(text="Reset", **HEADER_TEXT, anchor="e", command=lambda: [wb.reset(), timer.reset_interface()])
reset_button.configure(width=5, fg="dark red")
reset_button.grid(column=2, row=0, sticky="ew")

# Entry field
user_word = StringVar()
user_entry = Entry(textvariable=user_word, justify="center", font=FONT, width=20)
user_entry.grid(column=0, row=2, columnspan=3, padx=10, pady=20)
user_entry.focus_set()

# Score label
user_score = Label(text="", **HEADER_TEXT)
user_score.grid(column=0, row=2, sticky="w")

# Create WordBrain and Timer objects
wb = WordBrain(window, words_to_type, user_score, user_entry)
timer = Manager(window, timer_label, wb, user_entry)

# Trace user's input
user_word.trace("w", callback=wb.entry_manager)

# Placeholder button
ph_button = Button(text="FINISH GAME", command=timer.finish_game)
ph_button.grid(column=0, row=3)


window.mainloop()
