import csv
import sqlite3
import cv2
import os
import imutils
import AddToDB_ui

createtable="""CREATE TABLE IF NOT EXISTS Identity (ID INTEGER PRIMARY KEY,Name TEXT NOT NULL,age INTEGER,gender TEXT,remark TEXT,Authorized INTEGER);"""
connection=sqlite3.connect("survilance.db")
cursor=connection.cursor()
cursor.execute(createtable)


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False


# Take image function

def takeImages(self):


    Id =  self.lineEdit.text()
    name = self.lineEdit_2.text()
    age = self.lineEdit_4.text()
    if (self.radioButton.isChecked() == True):
        gender = self.radioButton.text()
    elif (self.radioButton_2.isChecked() == True):
        gender = self.radioButton_2.text()
    elif (self.radioButton_3.isChecked() == True):
        gender = self.radioButton_3.text()
    else:
        gender = "NULL"
    
    remark=self.lineEdit_5.text()

    if(is_number(Id) and remark.isalpha()):
        cam = cv2.VideoCapture(0)
        harcascadePath = "haarcascade_frontalface_default.xml"
        detector = cv2.CascadeClassifier(harcascadePath)
        sampleNum = 0

        while(True):
            ret, img = cam.read()
            img=imutils.resize(img, width=400)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5, minSize=(30,30),flags = cv2.CASCADE_SCALE_IMAGE)
            for(x,y,w,h) in faces:
                cv2.rectangle(gray, (x, y), (x+w, y+h), (10, 159, 255), 1)
                #incrementing sample number
                sampleNum = sampleNum+1
                #saving the captured face in the dataset folder TrainingImage
                cv2.imwrite("TrainingImage" + os.sep +name + "."+Id + '.' +
                            str(sampleNum) + ".jpg", gray[y:y+h, x:x+w])
                #display the frame
                
                cv2.namedWindow('frame', cv2.WINDOW_KEEPRATIO)
                cv2.imshow('frame', gray)
                cv2.resizeWindow('frame',300,300)
            #wait for 100 miliseconds
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
            # break if the sample number is more than 100
            elif sampleNum > 100:
                break
        cam.release()
        cv2.destroyAllWindows()
        res = "Images Saved for ID : " + Id + " Name : " + name
        row = (Id,name,age,gender,remark)
        saverow="INSERT INTO Identity (ID,Name,age,gender,remark) VALUES (?, ?, ?, ?, ?)"
        cursor.execute(saverow,row)
        connection.commit()
    else:
        print("Check Entered Data")
    #connection.close()


