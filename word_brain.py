import random


class WordBrain:
    def __init__(self, window, box, score_label, entry):
        # Feed GUI elements to interact with
        self.window = window
        self.box = box
        self.score_label = score_label
        self.entry = entry

        with open("words.txt", "r") as file:
            self.word_list = [line.strip().lower() for line in file]

        # Set attributes and starting values
        self.ranges = None
        self.current_start = None
        self.current_end = None
        self.current_word = None

        self.score = 0
        self.current_word_index = 0
        self.user_words = []

        # Populate words_to_type
        self.populate_word_list()
        self.update_score()
        self.set_current_word()

    def populate_word_list(self):
        """Fill words_to_type and give tag to each word based on their index"""
        line_count = 1
        tag_index = 0
        random.shuffle(self.word_list)
        for word in self.word_list:
            if len(self.box.get(f"{line_count}.0", "end")) + len(word) > 59:
                self.box.insert("end", "\n")
                line_count += 1
            self.box.tag_config(f"{tag_index}")
            self.box.insert("end", word, f"{tag_index}")
            self.box.insert("end", "  ")
            tag_index += 1

        self.box.tag_config("center", justify="center")
        self.box.tag_add("center", 1.0, "end")
        self.box.configure(bg="white", state="disabled")

        # Establish tags for later use
        self.box.tag_config("green", foreground="green")
        self.box.tag_config("red", foreground="red")
        self.box.tag_config("black", foreground="black")

    def set_current_word(self):
        """Changes current word's background to yellow. Sets start and end of current word, based on tag."""
        self.box.tag_config(f"{self.current_word_index}", background="yellow")
        self.linekill()

        self.ranges = self.box.tag_ranges(f"{self.current_word_index}")
        self.current_start = self.ranges[0]
        self.current_end = self.ranges[1]
        self.current_word = self.box.get(self.current_start, self.current_end)

    def entry_manager(self, *args):
        """Colours letters of the current word green or red, based on user's entry."""
        word = self.entry.get().replace(" ", "")

        if len(self.current_word) >= len(word):
            self.box.tag_remove("green", self.current_start, self.current_end)
            self.box.tag_remove("red", self.current_start, self.current_end)
            letter_index = 0
            for letter in word:
                if letter == self.current_word[letter_index]:
                    self.box.tag_add("green",
                                     f"{self.current_start}+{letter_index}c",
                                     f"{self.current_start}+{letter_index + 1}c")
                else:
                    self.box.tag_add("red",
                                     f"{self.current_start}+{letter_index}c",
                                     f"{self.current_start}+{letter_index + 1}c")
                letter_index += 1
        else:
            self.box.tag_add("red", self.current_start, self.current_end)

        self.bind_previous_word()

    def linekill(self):
        """Deletes top row when user reaches the bottom row."""
        try:
            prev_start = int(str(self.box.tag_ranges(f"{self.current_word_index - 1}")[0]).split(".")[0])

        except IndexError:
            pass

        else:
            new_start = int(str(self.box.tag_ranges(f"{self.current_word_index}")[0]).split(".")[0])
            if prev_start != 1 and prev_start < new_start:
                self.box.configure(state="normal")
                self.box.delete("1.0", "2.0")
                self.box.configure(state="disabled")

    def bind_previous_word(self):
        """Binds the previous method function if entry field is empty."""
        if self.current_word_index != 0 and not self.entry.get():
            self.window.bind("<BackSpace>", lambda event: self.previous_word())
        else:
            self.window.unbind("<BackSpace>")

    def update_score(self):
        """Updates Score label to current score."""
        self.score = 0
        for word in self.user_words:
            word_index = self.user_words.index(word)
            if word == self.word_list[word_index]:
                self.score += 1
        self.score_label.config(text=f"Score: {self.score}")

    def next_word(self):
        """Adds word to user's word list. Updates score. Gets next word and clears entry field."""
        word = self.entry.get().replace(" ", "")

        # Add word to user's word list
        try:
            self.user_words[self.current_word_index] = word
        except IndexError:
            self.user_words.append(word)

        # Update score
        self.update_score()

        # Get next word and clear user entry
        self.box.tag_config(f"{self.current_word_index}", background="white")
        self.current_word_index += 1
        self.set_current_word()
        self.entry.delete(0, "end")

    def previous_word(self):
        """Changes current word to previous one and re-populates entry field with user's previous entry."""
        if not self.entry.get():
            self.box.tag_config(f"{self.current_word_index}", background="white")

            self.current_word_index -= 1
            self.set_current_word()
            self.entry.delete(0, "end")
            self.entry.insert(0, f"{self.user_words[self.current_word_index]}")
        else:
            pass

    def reset(self):
        """Resets object to starting values and clears text fields"""

        # Reset values
        self.score = 0
        self.current_word_index = 0

        # Empty words_to_type and user entry
        self.box.configure(state="normal")
        self.box.delete("1.0", "end")
        self.entry.configure(state="normal")
        self.entry.delete(0, "end")

        # Delete all tags
        for tag in self.box.tag_names():
            self.box.tag_delete(tag)

        # Unbind previous_word() from BackSpace
        self.window.unbind("<BackSpace>")

        self.populate_word_list()
        self.update_score()
        self.set_current_word()
