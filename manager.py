from tkinter import Toplevel, Label, Button

FONT = ("Courier", 15, "bold")

HEADER_TEXT = {"fg": "white",
               "bg": "black",
               "font": FONT}


class Manager:
    def __init__(self, window, label, wb, entry):
        # Feed GUI elements to interact with
        self.window = window
        self.label = label
        self.wb = wb
        self.entry = entry

        # Set attributes and starting values
        self.count = 60
        self.after_id = None
        self.label['text'] = f"{self.count}s"
        self.window.bind("<Key>", lambda event: [self.start_timer(), self.change_bindings()])

    def start_timer(self, *args):
        """Start the app timer"""
        self.label['text'] = f"{self.count}s"

        if self.count > 0:
            self.count -= 1
            self.after_id = self.window.after(1000, self.start_timer)
        else:
            self.finish_game()

    def change_bindings(self):
        """Changes key bindings"""
        self.window.unbind("<Key>")
        self.window.bind("<space>", lambda event: self.wb.next_word())

    def reset_interface(self):
        """Resets app interface"""
        self.window.unbind("<space>")

        try:
            self.window.after_cancel(self.after_id)
        except AttributeError:
            pass

        self.count = 60
        self.label['text'] = f"{self.count}s"
        self.window.bind("<Key>", lambda event: [self.start_timer(), self.change_bindings()])

    def finish_game(self):
        """Creates popup window with final score and choice of Exit and Restart"""
        top = Toplevel(self.window)
        top.geometry("250x180")
        top.minsize(width=250, height=180)
        top.configure(bg="black", padx=20)
        top.title("Final Score")

        top_header = Label(top, text="YOUR FINAL SCORE:", **HEADER_TEXT, justify="center")
        top_header.grid(column=0, row=0, columnspan=2, sticky="ew")

        top_cpm_score = Label(top, text=f"{len("".join(self.wb.user_words))}", **HEADER_TEXT, justify="center")
        top_cpm_score.configure(fg="dark red", font=("Courier", 20, "bold"))
        top_cpm_score.grid(column=0, row=1, sticky="ew")

        top_cpm_label = Label(top, text="characters", **HEADER_TEXT, justify="left")
        top_cpm_label.grid(column=1, row=1, sticky="w")

        top_wpm_score = Label(top, text=f"{self.wb.score}", **HEADER_TEXT, justify="center")
        top_wpm_score.configure(fg="dark red", font=("Courier", 20, "bold"))
        top_wpm_score.grid(column=0, row=3, sticky="ew")

        top_wpm_label = Label(top, text="words", **HEADER_TEXT, justify="left")
        top_wpm_label.grid(column=1, row=3, sticky="w")

        exit_button = Button(top, text="Exit", **HEADER_TEXT, command=exit)
        exit_button.configure(width=5, fg="dark red")
        exit_button.grid(column=0, row=5, pady=30, sticky="ew")

        play_again = Button(top, text="Restart", **HEADER_TEXT,
                            command=lambda: [self.wb.reset(), self.reset_interface(), top.destroy()])
        play_again.configure(width=5, fg="dark green")
        play_again.grid(column=1, row=5, pady=30, sticky="ew")

        self.entry.configure(state="disabled")

        top.grab_set()
