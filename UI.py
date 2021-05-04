import sys


from PyQt5.QtWidgets import (

    QApplication, QDialog, QMainWindow, QMessageBox

)

from PyQt5.uic import loadUi


from main_window_ui import Ui_MainWindow


class Window(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.setupUi(self)

        self.connectSignalsSlots()


    def connectSignalsSlots(self):


        self.actionAdd.triggered.connect(self.AddToDB)



    def AddToDB(self):

        dialog = AddToDBDialog(self)

        dialog.exec()




class AddToDBDialog(QDialog):

    def __init__(self, parent=None):

        super().__init__(parent)

        loadUi("UI/Add_to_Database.ui", self)


if __name__ == "__main__":

    app = QApplication(sys.argv)

    win = Window()

    win.show()

    sys.exit(app.exec())
