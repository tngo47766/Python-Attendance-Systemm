from tkinter.simpledialog import askstring
from sklearn.neighbors import KNeighborsClassifier
import cv2
import pickle
import numpy as np
import os
import csv
import time
from datetime import datetime
from win32com.client import Dispatch
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import sort_data

def speak(str1):
    speak = Dispatch("SAPI.SpVoice")
    speak.Speak(str1)

# Load the face detection classifier
facedetect = cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')

# Load the trained model and data
with open('data/names.pkl', 'rb') as w:
    LABELS = pickle.load(w)
with open('data/faces_data.pkl', 'rb') as f:
    FACES = pickle.load(f)
knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(FACES, LABELS)

imgBackground = cv2.imread("background_new.png")

COL_NAMES = ['NAME', 'TIME']

# Email configuration
sender_email = 'pythonattendancesystem@gmail.com'  # Your email address
sender_password = 'joow tcyj mssp rbed'  # Your email password
smtp_server = 'smtp.gmail.com'  # SMTP server (for Gmail)

def send_email(subject, message, receiver_email):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # Attach the message to the email
    msg.attach(MIMEText(message, 'plain'))

    try:
        # Establish a secure session with the SMTP server using your Gmail account
        server = smtplib.SMTP(smtp_server, 587)
        server.starttls()
        server.login(sender_email, sender_password)

        # Send the message
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)
        server.quit()
        print(f"Email sent successfully to {receiver_email}")
    except Exception as e:
        print(f"Email could not be sent: {e}")


def runModule():
    done = False
    video = cv2.VideoCapture(0)  # 0 for webcam

    while True:
        ret, frame = video.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        faces = facedetect.detectMultiScale(gray, 1.3, 5)
        
        for (x, y, w, h) in faces:
            crop_img = frame[y:y + h, x:x + w, :]
            resize_img = cv2.resize(crop_img, (50, 50)).flatten().reshape(1, -1)
            output = knn.predict(resize_img)
            ts = time.time()
            date = datetime.fromtimestamp(ts).strftime("%d-%m-%y")
            timestamp = datetime.fromtimestamp(ts).strftime("%H:%M-%S")
            exist = os.path.isfile("Attendance/Attendance_" + date + ".csv")
            cv2.putText(frame, str(output[0]), (x, y - 15), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (50, 50, 255), 1)
            attendance = [str(output[0]), str(timestamp)]
            k = cv2.waitKey(1)
            if k == ord('o') or k == ord('O'):
                done = True
                speak("Attendance Accepted..")
                time.sleep(2)
                if exist:
                    with open("Attendance/Attendance_" + date + ".csv", "a") as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow(attendance)
                    csvfile.close()
                else:
                    with open("Attendance/Attendance_" + date + ".csv", "a") as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow(COL_NAMES)
                        writer.writerow(attendance)
                    csvfile.close()

                # Read recipient's email from person_info.csv based on the person's name
                recipient_email = None
                with open('static/person_info.csv', 'r', newline='') as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        if row['Name'] == str(output[0]):
                            recipient_email = row['Email']
                            break

                if recipient_email:
                    # Send an email to the person whose attendance is accepted
                    email_subject = 'Attendance Accepted'
                    email_message = f'Hello {str(output[0])}, your attendance has been accepted.'

                    send_email(email_subject, email_message, recipient_email)

        imgBackground[162:162 + 480, 55:55 + 640] = frame
        cv2.imshow("Diem Danh", imgBackground)
        k = cv2.waitKey(1)

        if k == ord('q') or k == ord('Q'):
            break

    video.release()
    cv2.destroyAllWindows()
    sort_data.run()
    return done
