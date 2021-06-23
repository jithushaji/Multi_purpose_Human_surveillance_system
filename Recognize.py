import datetime
import os
import time
import imutils
import cv2
import pandas as pd
import sqlite3

#-------------------------
def recognize_face():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read("TrainingImageLabel"+os.sep+"Trainner.yml")
    harcascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath)
    connection=sqlite3.connect("survilance.db")
    font = cv2.FONT_HERSHEY_SIMPLEX
    str1="employee"
    
    query="CREATE TABLE IF NOT EXISTS Recognized (ID PRIMARY KEY,Name TEXT NOT NULL,Age INTEGER,Gender TEXT,Remark TEXT,Time Text);"
    query1="CREATE TABLE IF NOT EXISTS Loggedin (ID PRIMARY KEY,Name TEXT NOT NULL,Time Text)"
    cursor=connection.cursor()
    cursor.execute(query)
    cursor.execute(query1)
    query2="SELECT * FROM Identity WHERE ID=?"
    query3="INSERT OR IGNORE INTO Recognized (ID,Name,Age,Gender,Remark,Time) VALUES (? ,?, ?, ?, ?, ?)"
    query4="INSERT OR IGNORE INTO Loggedin (ID,Name,Time) VALUES (? ,?, ?)"
    
    connection.commit()
    

    # Initialize and start realtime video capture
    cam = cv2.VideoCapture(0)
    # Define min window size to be recognized as a face
    minW = 0.1 * cam.get(3)
    minH = 0.1 * cam.get(4)

    while True:
        ret, im = cam.read()
        im=imutils.resize(im, width=400)
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(im, 1.2, 5,minSize = (int(minW), int(minH)),flags = cv2.CASCADE_SCALE_IMAGE)
        for(x, y, w, h) in faces:
            cv2.rectangle(im, (x, y), (x+w, y+h), (10, 159, 255), 1)
            Id, conf = recognizer.predict(gray[y:y+h, x:x+w])
            cursor.execute(query2,(Id,))
            records=cursor.fetchall()

            if conf < 100:

                for row in records:
                    aa = row[1]
                confstr = "  {0}%".format(round(100 - conf))
                tt = str(Id)+"-"+aa


            else:
                Id = '  Unknown  '
                tt = str(Id)
                confstr = "  {0}%".format(round(100 - conf))

            if (100-conf) > 10:
                cv2.putText(im, str(tt), (x+5,y-5), font, 0.5, (255, 255, 255), 2) #printing name on display
                ts = time.time()
                date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M')
                hour = int(timeStamp.split(':')[0])
                for dat in records:
                    Name=dat[1]
                    Age=dat[2]
                    Gender=dat[3]
                    Remark=dat[4]
                    Auth=dat[5]
                val=(Id,Name,Age,Gender,Remark,timeStamp)
                val1=(Id,Name,timeStamp)
                if (Remark == str1) and (hour<12): # adding employee login time
                    cursor.execute(query4,val1)    
                cursor.execute(query3,val) # adding detections to detection database
                connection.commit()
                ### code to alert if system detecs an unauthorized person after a set time
    
                
                if (hour >= 18) and (Auth != 1):
                    print("unauthorized")
                else:
                    print("Authorized")
                
            tt = str(tt) #[2:-2]


        cv2.namedWindow('Recognizer', cv2.WINDOW_KEEPRATIO)
        cv2.imshow('Recognizer', im)
        cv2.resizeWindow('Recognizer',300,300)
        if (cv2.waitKey(1) == ord('q')):
            break
    connection.close()
    print("TERMINATING.......")
    cam.release()
    cv2.destroyAllWindows()
