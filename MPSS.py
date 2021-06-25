import sys


from PyQt5.QtWidgets import (

    QApplication, QDialog, QMainWindow, QMessageBox

)

from PyQt5.uic import loadUi


from main_window_ui import Ui_MainWindow

from AddToDB_ui import Ui_Dialog

from options_ui import Ui_option_Dialog


class AddToDBDialog(QDialog, Ui_Dialog):
    
    def __init__(self, parent=None):

        super().__init__(parent)
        
        self.setupUi(self)
        
        self.connectSignalsSlots()
        
    
    def connectSignalsSlots(self):
        
        self.pushButton.clicked.connect(self.capture)
        

    def capture(self):
        
        import Capture_Image
        
        Capture_Image.takeImages(self)
               

class AddOptionDialog(QDialog, Ui_option_Dialog):
    
    def __init__(self, parent=None):

        super().__init__(parent)
        
        self.setupUi(self)
        
        #self.connectSignalsSlots()
    

class Window(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.setupUi(self)

        self.connectSignalsSlots()


    def connectSignalsSlots(self):

        self.actionAdd.triggered.connect(self.AddToDB)
        
        self.action_File.triggered.connect(self.option)
        
        self.pushButton.clicked.connect(self.camera)
        
        self.pushButton_2.clicked.connect(self.train)
        
        self.pushButton_3.clicked.connect(self.recognize)
        
        self.pushButton_4.clicked.connect(self.Quit)


    def option(self):
        
        self.dialog = AddOptionDialog(self)

        self.dialog.show()
    
    
    def AddToDB(self):

        self.dialog = AddToDBDialog(self)

        self.dialog.show()
        
    
    def camera(self):
        
        import check_camera
        
        check_camera.camer()
        
        
    def train(self):
        
        import Train_Image
        
        Train_Image.TrainImages()
        
        
    def recognize(self):
        
        import Recognize
        
        Recognize.recognize_face()
        
     
    def Quit(self):
        
        self.close()


if __name__ == "__main__":

    app = QApplication(sys.argv)

    win = Window()

    win.show()

    sys.exit(app.exec())
