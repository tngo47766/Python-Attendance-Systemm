import cv2
import pickle
import numpy as np
import os
import csv
#---------------------------------------#
#Muc tieu chinh cua chuong trinh la luu tru du lieu khuon mat cua nguoi dung qua web cam su dung ham facedect cua cv2 va luu tru chung duoi dang file pickle 
#---------------------------------------#
video=cv2.VideoCapture(0) #0 la dung webcam

facedetect=cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')# Load Classifier de Nhan dien khuon mat


# bien dung de cat anh moi 10 frame
# name=input("Nhap ten cua ban: ")
# email = input("Nhap email cua ban: ")
# password = input("Nhap mat khau cua ban")

def add_face(name, email, password):
    faces_data=[]
    i=0
    while True:
        ret,frame=video.read()# ret la gia tri check webcam, frame la frame nhan dc
        gray=cv2.cvtColor(frame,cv2.COLOR_RGB2GRAY)# convert frame sang mau xam de nhan dien khuon mat
        faces=facedetect.detectMultiScale(gray,1.3,5)# nhan dien khuon mat
        for (x,y,w,h) in faces:
            crop_img=frame[y:y+h,x:x+w,:]#Cat anh de ghi nhan
            resize_img=cv2.resize(crop_img,(50,50))# resize anh
            if len(faces_data)<=100 and i%3==0:
                faces_data.append(resize_img)
            i=i+1
            cv2.putText(frame, "Ghi Nhan: "+str(len(faces_data))+"/100",(50,50),cv2.FONT_HERSHEY_COMPLEX,1,(50,50,255),1)#in so anh da duoc ghi nhan
            cv2.rectangle(frame,(x,y),(x+w,y+h),(50,50,255),1)# ve khung bao mat
        cv2.imshow("frame",frame)
        k=cv2.waitKey(1)
        if k==ord('q') and len(faces_data) < 100:
            faces_data.clear()
            return False
        if k==ord('q') or len(faces_data)==100 or k==ord('Q'):
            break
    video.release()
    cv2.destroyAllWindows()
    # Chuyen list face_data thanh Numpy array:

    faces_data=np.asarray(faces_data)
    faces_data=faces_data.reshape(100, -1)
    #Kiem tra xem file names.pkl da ton tai hay chua 
    if 'names.pkl' not in os.listdir('data/'):
        names=[name]*100# neu ko ton tai thi tao mot danh sach chua 100 lan ten nguoi dung
        with open('data/names.pkl', 'wb') as f:# luu danh sach vua tao
            pickle.dump(names, f)
    else:# neu da ton tai
        with open('data/names.pkl', 'rb') as f:#mo file
            names=pickle.load(f)
        names=names+[name]*100# tang do dai danh  sach len 100 lan ten nguoi dung
        with open('data/names.pkl', 'wb') as f:
            pickle.dump(names, f)#luu danh sach

    # Tuong tu doi voi luu tru du lieu khuon mat
    if 'faces_data.pkl' not in os.listdir('data/'):
        with open('data/faces_data.pkl','wb') as f:
            pickle.dump(faces_data,f)
    else: 
        with open('data/faces_data.pkl','rb') as f:
            faces=pickle.load(f)
        faces=np.append(faces,faces_data,axis=0)
        with open('data/faces_data.pkl','wb') as f:
            pickle.dump(faces,f)

    with open('static/person_info.csv', 'a', newline='') as csvfile:
        fieldnames = ['Name', 'Email', 'Password']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Check if the file is empty and write header if needed
        if os.path.getsize('static/person_info.csv') == 0:
            writer.writeheader()

        writer.writerow({'Name': name, 'Email': email, 'Password' : password})

    print("Name and email saved successfully.")
    return True

# add_face('Tung', 'tung75csp@gmail.com', '123456')