import sys
from PyQt5.QtWidgets import QApplication
from Team_Manager import TeamManager

def cricket_main():
    app = QApplication(sys.argv)
    window = TeamManager()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    cricket_main()