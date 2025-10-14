import sys,sqlite3
from PyQt5 import QtWidgets
from HomeScreen import Ui_homeScreen


def main():
    conn = sqlite3.connect("../culturama.db")
    app = QtWidgets.QApplication(sys.argv)
    homeScreen = QtWidgets.QMainWindow()
    ui = Ui_homeScreen()
    ui.setupUi(homeScreen,conn)
    homeScreen.showMaximized()
    sys.exit(app.exec_())
    conn.close()

if __name__ == "__main__":
    main()

