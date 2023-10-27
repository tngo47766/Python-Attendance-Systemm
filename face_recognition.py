from sklearn.neighbors import KNeighborsClassifier
import cv2
import pickle
import numpy as np
import os

#---------------------------------------#
# Su dung thuat toan KNN(K-Nearest Neighbors) de ung dung lam nhan dang khuon mat
#---------------------------------------#
video=cv2.VideoCapture(0) #0 la dung webcam

facedetect=cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')# Load Classifier de Nhan dien khuon mat

with open('data/names.pkl', 'rb') as w:
    LABELS=pickle.load(w)
with open('data/faces_data.pkl', 'rb') as f:
    FACES=pickle.load(f)
knn=KNeighborsClassifier(n_neighbors=5)
knn.fit(FACES, LABELS)

while True:
    ret,frame=video.read()# ret la gia tri check webcam, frame la frame nhan dc
    gray=cv2.cvtColor(frame,cv2.COLOR_RGB2GRAY)# convert frame sang mau xam de nhan dien khuon mat
    faces=facedetect.detectMultiScale(gray,1.3,5)# nhan dien khuon mat
    for (x,y,w,h) in faces:
        crop_img=frame[y:y+h,x:x+w,:]#Cat anh de ghi nhan
        resize_img=cv2.resize(crop_img,(50,50)).flatten().reshape(1,-1)# resize anh
        output=knn.predict(resize_img)
        cv2.putText(frame,str(output[0]),(x,y-15),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),1)
        cv2.rectangle(frame,(x,y),(x+w,y+h),(50,50,255),1)# ve khung bao mat
    cv2.imshow("frame",frame)
    k=cv2.waitKey(1)
    if k==ord('q') or k==ord('Q') :
        break
video.release()
cv2.destroyAllWindows()
