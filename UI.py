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
        self.pushButton.clicked.connect(self.camera)



    def AddToDB(self):

        dialog = AddToDBDialog(self)

        dialog.exec()
    
    def camera(self):
        
        import check_camera
        check_camera.camer()
        
    def capture(self):
        
        import Capture_Image
        Capture_Image.takeImages()
        
        
    def train(self):
        
        import Train_Image
        Train_Image.TrainImages()
        
    def recognize(self):
        
        import Recognize
        Recognize.recognize_face()


class AddToDBDialog(QDialog):

    def __init__(self, parent=None):

        super().__init__(parent)

        loadUi("UI/Add_to_Database.ui", self)


if __name__ == "__main__":

    app = QApplication(sys.argv)

    win = Window()

    win.show()

    sys.exit(app.exec())
