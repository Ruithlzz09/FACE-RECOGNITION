import os
import cv2
import numpy as np 
from PIL import Image
import sqlite3





def getImagesWithID(path):
  imagePaths = [os.path.join(path,f) for f in os.listdir(path)]
  faces = []
  IDs = []
  for imagePath in imagePaths:
    faceImg = Image.open(imagePath).convert('L')
    faceNp = np.array(faceImg,'uint8')
    ID = int(os.path.split(imagePath)[-1].split('.')[1])
    faces.append(faceNp)
    IDs.append(ID)
    cv2.imshow("training",faceNp)
  cv2.destroyAllWindows()

  print("training complete")
  return np.array(IDs), faces



def detect_face():
  #constants
  path = 'dataset'
  face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
  pause=1
  
  #training phase
  recognizer = cv2.face.LBPHFaceRecognizer_create()
  Ids, faces = getImagesWithID(path)
  recognizer.train(faces,Ids)
  recognizer.save('recognizer/trainingData.yml')



  #Detection phase
  conn = sqlite3.connect('database.db')
  c = conn.cursor()

  cv2.namedWindow("Face Recognizer",cv2.WINDOW_NORMAL)
  cap = cv2.VideoCapture(0)
  ids,conf=0,0
  try:
    while True:
      ret, img = cap.read()
      img=cv2.flip(img,1)
      if ret:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x,y,w,h) in faces:
          if pause==0:
            cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),3)
            ids,conf = recognizer.predict(gray[y:y+h,x:x+w])
            c.execute("select name from users where id = (?);", (ids,))
            result = c.fetchall()
            try:
              name = result[0][0]
            except:
              continue
            print(result,conf)
            if conf > 30:
              cv2.putText(img, name, (x+2,y+h-5), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (150,255,0),1)
            else:
              cv2.putText(img, 'No Match', (x+2,y+h-5), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255,0,0),1)
        cv2.imshow('Face Recognizer',img)
        key= chr(cv2.waitKey(1) & 255)
        if key == 'q':
          break
        elif key=='n':
          pause=0
        elif key=='p':
          pause=1
      else:
        break

  except Exception as e:
    print(e)

  conn.commit()
  conn.close()
  cap.release()
  cv2.destroyAllWindows()
