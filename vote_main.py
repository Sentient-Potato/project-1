import sys
from PyQt6.QtWidgets import QApplication
from vote_gui import GUI

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = GUI()

    # Shows the ui
    window.show()

    # Runs the program
    sys.exit(app.exec())

