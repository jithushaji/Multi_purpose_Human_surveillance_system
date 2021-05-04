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
    query="CREATE TABLE IF NOT EXISTS Recognized (ID INTEGER PRIMARY KEY ,Name TEXT NOT NULL,Age INTEGER,Gender TEXT,Remark TEXT,Time Text);"
    cursor=connection.cursor()
    cursor.execute(query)
    query2="SELECT * FROM Identity WHERE ID=?"
    query3="INSERT OR IGNORE INTO Recognized (ID,Name,Age,Gender,Remark,Time) VALUES (? ,?, ?, ?, ?, ?)"

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

            if (100-conf) > 20:
                ts = time.time()
                date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                for dat in records:
                    Name=dat[1]
                    Age=dat[2]
                    Gender=dat[3]
                    Remark=dat[4]
                val=(Id,Name,Age,Gender,Remark,timeStamp)
                cursor.execute(query3,val)
                connection.commit()

            tt = str(tt) #[2:-2]


            if(100-conf) > 30:
                cv2.putText(im, str(tt), (x+5,y-5), font, 0.5, (255, 255, 255), 2)
            else:
                cv2.putText(im, str(tt), (x + 5, y - 5), font, 0.5, (255, 255, 255), 2)

            if (100-conf) > 27:
                cv2.putText(im, str(confstr), (x + 5, y + h - 5), font,1, (0, 255, 0),1 )
            elif (100-conf) > 20:
                cv2.putText(im, str(confstr), (x + 5, y + h - 5), font, 1, (0, 255, 255), 1)
            else:
                cv2.putText(im, str(confstr), (x + 5, y + h - 5), font, 1, (0, 0, 255), 1)


        cv2.imshow('Recognizer', im)
        if (cv2.waitKey(1) == ord('q')):
            break
    connection.close()
    print("TERMINATING.......")
    cam.release()
    cv2.destroyAllWindows()
