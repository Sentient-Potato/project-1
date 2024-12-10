from PyQt6.QtWidgets import *
from PyQt6.QtGui import QPalette
from PyQt6 import uic
from vote_logic import processing

# This was made after the D&D initiative tracker was halfway done.

class GUI(QMainWindow):
    times_pressed = 0 # The fun variable that has no other purpose other than for a joke function
    def __init__(self):
        super().__init__()

        # Sets the size of the window and prevents resizing
        self.setFixedSize(611, 650)

        # Loads the QtDesigner ui to use
        uic.loadUi('voting_app_project.ui', self)

        # Defines the ui as screen_main in order to call upon the objects within the ui
        self.screen_main = uic.loadUi("voting_app_project.ui", self)

        # Sets default colors of the widget because the code breaks if I don't define it beforehand
        self.set_colors()

        # Adds functionality to the 4 color buttons
        self.join_color_buttons()

        # Adds functionality to my joke button. This serves no important purpose other than amusement
        self.screen_main.vote_for_me_fun_button.clicked.connect(self.fun_button_function)

        self.screen_main.submit_button.clicked.connect(self.retrieve_and_process_data)

    def set_colors(self): # Sets the default colors of the widget
        self.background_color = self.screen_main.title_label.palette().color(QPalette.ColorRole.Window).name()

    def update_styles(self): # Updates any color changes made to the title banner
        stylesheet = f"background-color: {self.background_color};"
        self.screen_main.title_label.setStyleSheet(stylesheet)

    def banner_color_change(self, color): # Defines the colors available and enables color change
        colors = {
            "red": "rgb(188, 56, 58)",
            "blue": "rgb(46, 63, 175)",
            "green": "rgb(44, 180, 65)",
            "gray": "rgb(116, 116, 116)",
        }
        self.background_color = colors.get(color, self.background_color)
        self.update_styles()

    def join_color_buttons(self): # Is the basic function for the 4 color buttons
        color_buttons = {
            "red": self.screen_main.red_banner_button,
            "blue": self.screen_main.blue_banner_button,
            "green": self.screen_main.green_banner_button,
            "gray": self.screen_main.gray_banner_button,
        }
        for color, button in color_buttons.items():
            button.clicked.connect(lambda _, c=color: self.banner_color_change(c))

    def color_message (self, message, is_error=False): # As per the name, it allows the text to change colors depending on the error message
        if is_error:
            self.screen_main.output_message.setStyleSheet("color: red; font-size: 18px; font-family: 'MS Shell Dlg 2';")
        else:
            self.screen_main.output_message.setStyleSheet("color: green; font-size: 18px; font-family: 'MS Shell Dlg 2';")
        self.screen_main.output_message.setText(message)
        # Font family name is included to ensure that the font is consistent. Totally not because I was too lazy to remove it after learning the default font

    def fun_button_function(self): # The function for my little joke button. Hint, it takes around 13 clicks to "break" the program
        self.screen_main.output_message.setStyleSheet("font-size: 18px; font-family: 'MS Shell Dlg 2';")

        messages = [
            "We can't vote for you!",
            "Again, we can't vote for you!",
            "How many times do we have to tell you? We can't vote for you!",
            "Stop it!",
            "I'm warning you!",
            "Don't make me do this!",
            "Stop!",
            "You have until the count of 3 to stop!",
            "1",
            "2",
            "3",
            "That's it, I'm taking away your button privileges!"
        ]

        if self.times_pressed < len(messages):
            self.screen_main.output_message.setText(messages[self.times_pressed])

            if messages[self.times_pressed] == "That's it, I'm taking away your button privileges!": # no button 4 u
                self.hide_buttons()

        self.times_pressed += 1

    def hide_buttons(self): # NO BUTTON 4 U
        for widget in self.findChildren(QPushButton):
            widget.hide()

    def retrieve_data(self):
        name_input = self.screen_main.name_input.text()  # Collects the input from Name
        id_input = self.screen_main.id_input.text()  # Collects the input from ID
        vote_input = self.selected_vote()

        if not name_input or not id_input:  # Detects if there is no input made in either boxes
            return "No input data"  # Error type 1

        try:
            int(id_input)  # Detects if the ID input contains non-integers
            if len(id_input) != 7:  # Detects if the ID is longer or shorter than 7 digits
                return "Invalid ID"  # Error type 2
        except ValueError:
            return "Invalid ID"  # Error type 2

        if not vote_input:
            return "No vote input"  # Error type 3

        processed_data = processing(name_input, id_input, vote_input)
        if processed_data == "Existing ID":
            return "Existing ID"
        else:
            return "Processed"  # Proceed to next function upon success

    def retrieve_and_process_data(self):
        result = self.retrieve_data()

        if result == "Processed":
            self.clear_and_reset()
            self.screen_main.output_message.setText("Voted successfully")  # Indicate successful processing
            self.color_message("Voted successfully")
        else:
            self.errors(result)  # Display specific error message depending on the error type defined above, reason why they're labeled Error type 1-3, 4 is on logic.py

    def selected_vote(self): # If not obvious, it detects which candidate was voted for
        if self.screen_main.john_vote.isChecked():
            return "John Doe"
        elif self.screen_main.jane_vote.isChecked():
            return "Jane Doe"
        elif self.screen_main.person_vote.isChecked():
            return "Person Doe"
        else:
            return None # Determines if there was no vote cast, and we can't have that now, can we?

    def clear_and_reset(self): # Removes all input after successful processing to continue to accept other voters
        self.screen_main.name_input.clear()
        self.screen_main.id_input.clear()

        self.screen_main.john_vote.setAutoExclusive(False)
        self.screen_main.john_vote.setChecked(False)
        self.screen_main.john_vote.setAutoExclusive(True)

        self.screen_main.jane_vote.setAutoExclusive(False)
        self.screen_main.jane_vote.setChecked(False)
        self.screen_main.jane_vote.setAutoExclusive(True)

        self.screen_main.person_vote.setAutoExclusive(False)
        self.screen_main.person_vote.setChecked(False)
        self.screen_main.person_vote.setAutoExclusive(True)

    def errors(self, result): # The specific error messages upon each error that is raised/returned
        if result == "No input data":
            self.color_message("No name or ID number was provided. Please provide a name and valid ID", True)
        elif result == "Invalid ID":
            self.color_message("Your ID is invalid. Make sure it contains only integers and consists of 7 digits",
                                True)
        elif result == "Existing ID":
            self.color_message("This ID has already voted", True)
        elif result == "No vote input":
            self.color_message("Please select a candidate to vote for", True)