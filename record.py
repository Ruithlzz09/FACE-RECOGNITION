#dependecies
import cv2
import numpy as np 
import sqlite3
import os


def connection(db='database.db'):
  conn = sqlite3.connect(db)
  c = conn.cursor()
  uname = input("Enter your name: ")
  c.execute('INSERT INTO users (name) VALUES (?)', (uname,))
  uid = c.lastrowid
  sampleNum = 0
  return conn,uname,uid,sampleNum


def detection_face(img,sampleNum=0,):
  #Classifier
  face_cascade=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
  cv2.namedWindow("detect",cv2.WINDOW_NORMAL)
  faces = face_cascade.detectMultiScale(img, 1.3, 5)
  for (x,y,w,h) in faces:
      sampleNum = sampleNum+1
      cv2.rectangle(img, (x,y), (x+w, y+h), (255,0,0), 1)
  print(img.shape)
  cv2.imshow("detect",img)
  while True:
      pressedkey=chr(cv2.waitKey(1) & 255)
      if pressedkey=='q':
        break
  cv2.destroyWindow("detect")
  return sampleNum


def display(img,loc,title="Face"):
  cv2.imshow(title,img)
  while True:
      pressedkey=chr(cv2.waitKey(1) & 255)
      if pressedkey=='q':
        break
      if pressedkey=='s':
        cv2.imwrite(loc,img)
        #cv2.destroyWindow(title="Face")
        return 1
  #cv2.destroyWindow(title="Face")
  return 0
  


def register():
  #constants
  face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')  #classifier  to detect faces
  pause=1                                                                      #set pause==1 in order to stop detection or vice-vera. By default detection is off

  #finding required data
  conn,uname,uid,sampleNum=connection()

  #cv2.namedWindow("Video feed",cv2.WINDOW_NORMAL)
  #Video Capture Starts
  cap = cv2.VideoCapture(0)
  try:
    while True:
      ret, img = cap.read()
      if ret:  #camera is capturing video
        img=cv2.flip(img,1)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x,y,w,h) in faces:
            if pause==0:
                pathname="dataset/User."+str(uid)+"."+str(sampleNum)+".jpg"
                temp=gray[y:y+h,x:x+w]
                key=chr(cv2.waitKey(30) & 255).lower()
                if key=='q':
                  break
                if key=='l':
                    pause=1
                    continue
                elif key=='s':
                  z=display(temp,pathname,title="Face")
                  if z==1:
                    sampleNum = sampleNum+1
                cv2.rectangle(img, (x,y), (x+w, y+h), (255,0,0), 1)
        cv2.imshow('Video feed',img)

        pressedkey=chr(cv2.waitKey(1) & 255).lower()
        if pressedkey=='q' or sampleNum > 20:
              break
        elif pressedkey=='l':
          pause=1
        elif pressedkey=='u':
          pause=0
      else:
        break
  except Exception as e:
    print(e)
  print("User: {0} has given {1} pics".format(uname,sampleNum))
  conn.commit()
  conn.close()
  cap.release()
  cv2.destroyAllWindows()