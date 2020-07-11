from Tkinter import*
import random
import time;
import cv2
import numpy as np
import os
from PIL import Image
import sqlite3


db = sqlite3.connect('FaceBase.db') #  I have tried: test, test.db, etc....
c = db.cursor()



root = Tk()
root.geometry("1600x800+0+0")
root.title("Attandance Management System")



Tops = Frame(root, width=1600, height=50, bg="powder blue", relief=SUNKEN)
Tops.pack(side=TOP)


f1 = Frame(root, width=500, height=50,  relief=SUNKEN)
f1.pack(side=LEFT)

f2 = Frame(root, width=500, height=50,  relief=SUNKEN)
f2.pack(side=RIGHT)

#--------------------------------Time---------------------------------------#
localtime=time.asctime(time.localtime(time.time()))
#---------------------------------------------------------------------------#
                      
lblInfo = Label(Tops, font=('arial',50,'bold'),text="ATTENDANCE MANAGEMENT SYSTEM",fg="Steel Blue",bd=10,anchor='w');
lblInfo.grid(row=0,column=0);

lblInfo = Label(Tops, font=('arial',30,'bold'), text=localtime, fg="Steel Blue",bd=10,anchor='w');
lblInfo.grid(row=1,column=0);

btnRegister=Button(f1,padx=20,bd=10,font=('arial',20,'bold'),text="Registration",command=lambda: btnRegister())
btnRegister.grid(row=0,column=0)

def btnRegister():

    lblName=Label(f1,font=('arial',16,'bold'), text ="Name", bd=16, anchor='w',justify='left')
    lblName.grid(row=2,column=0)

    txtName=Entry(f1,font=('arial',16,'bold'), textvariable=random, bd=10, insertwidth=4,justify='left')
    txtName.grid(row=2,column=1)

    lblRoll=Label(f1,font=('arial',16,'bold'), text ="Roll Number", bd=16, anchor='w',justify='left')
    lblRoll.grid(row=3,column=0)

    txtRoll=Entry(f1,font=('arial',16,'bold'), textvariable=random, bd=10, insertwidth=4,justify='left')
    txtRoll.grid(row=3,column=1)


    lblClass=Label(f1,font=('arial',16,'bold'), text ="Class", bd=16, anchor='w',justify='left')
    lblClass.grid(row=4,column=0)

    txtClass=Entry(f1,font=('arial',16,'bold'), textvariable=random, bd=10, insertwidth=4,justify='left')
    txtClass.grid(row=4,column=1)


    lblDepartment=Label(f1,font=('arial',16,'bold'), text ="Department", bd=16, anchor='w',justify='left')
    lblDepartment.grid(row=5,column=0)

    txtDepartment=Entry(f1,font=('arial',16,'bold'), textvariable=random, bd=10, insertwidth=4,justify='left')
    txtDepartment.grid(row=5,column=1)


    lblDiv=Label(f1,font=('arial',16,'bold'), text ="Division", bd=16, anchor='w',justify='left')
    lblDiv.grid(row=2,column=2)

    txtDiv=Entry(f1,font=('arial',16,'bold'), textvariable=random, bd=10, insertwidth=4,justify='left')
    txtDiv.grid(row=2,column=3)


    lblEmail=Label(f1,font=('arial',16,'bold'), text ="Email", bd=16, anchor='w',justify='left')
    lblEmail.grid(row=3,column=2)

    txtEmail=Entry(f1,font=('arial',16,'bold'), textvariable=random, bd=10, insertwidth=4,justify='left')
    txtEmail.grid(row=3,column=3)


    lblMobile=Label(f1,font=('arial',16,'bold'), text ="Mobile Number", bd=16, anchor='w',justify='left')
    lblMobile.grid(row=4,column=2)

    txtMobile=Entry(f1,font=('arial',16,'bold'), textvariable=random, bd=10, insertwidth=4,justify='left')
    txtMobile.grid(row=4,column=3)

    lblImage=Label(f1,font=('arial',16,'bold'), text ="Image", bd=16, anchor='w',justify='left')
    lblImage.grid(row=5,column=2)

    btncapture=Button(f1,padx=10,bd=5,font=('arial',10,'bold'),text="Capture",command=lambda: btnClick())
    btncapture.grid(row=5,column=3)

    btncapture = Button(f1, padx=10, bd=5, font=('arial', 10, 'bold'), text="Capture", command=lambda: btnsubmit())
    btncapture.grid(row=6, column=2)

    def btnsubmit():
        c.execute("insert into ram (txtName, txtRoll, txtClass, txtDepartment, txtDiv, txtEmail, txtMobile) values (?, ?, ?, ?, ?, ?, ?)", (txtName, txtRoll, txtClass, txtDepartment, txtDiv, txtEmail, txtMobile))


    def btnClick():
        detector = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml');
        cam = cv2.VideoCapture(0);
        time.sleep(2)

        id=input("Enter your ID : ")
        sampleNum = 0;
        while (True):
            ret, img = cam.read();
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5);
            if (len(faces) != 0):
                for (x, y, w, h) in faces:
                    sampleNum = sampleNum + 1;
                    cv2.imwrite("dataset/User." + str(id) + "." + str(sampleNum) + ".jpg", gray[y:y + h, x:x + w])
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.imshow('frame', img);
            cv2.waitKey(500);
            if (sampleNum > 50):
                break
        cam.release()
        cv2.destroyAllWindows()


btncTrain=Button(f1,padx=20,bd=10,font=('arial',20,'bold'),text="Trainer",command=lambda: btnTrain()).grid(row=0,column=2)



def btnTrain():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    path = 'dataSet'

    def getImagesWithID(path):
        imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
        faces = []
        IDs = []
        for imagePath in imagePaths:
            faceImg = Image.open(imagePath).convert('L')
            faceNp = np.array(faceImg, 'uint8')
            ID = int(os.path.split(imagePath)[-1].split(".")[1])
            faces.append(faceNp)
            IDs.append(ID)
            cv2.imshow("Trainer", faceNp)
            cv2.waitKey(100)

        return IDs, faces

    Ids, faces = getImagesWithID(path)
    recognizer.train(faces, np.array(Ids))
    recognizer.save('recognizer/trainnerData.yml')
    cv2.destoyAllWindows()



btncDetector=Button(f1,padx=20,bd=10,font=('arial',20,'bold'),text="Detector",command=lambda: btnDetector()).grid(row=0,column=4)


def btnDetector():
    recognizer = cv2.face.LBPHFaceRecognizer_create()

    recognizer.read('recognizer/trainnerData.yml')
    cascadePath = "haarcascade_frontalface_alt.xml"
    faceCascade = cv2.CascadeClassifier(cascadePath);

    cam = cv2.VideoCapture(0)

    # font = cv2.cv.InitFont(cv2.cv.CV_FONT_HERSHEY_SIMPLEX, 1, 1, 0, 1, 1)

    # font for the text written on image
    font = cv2.FONT_HERSHEY_TRIPLEX
    # cv2.putText(img,"Cat",(x,y-10),font,0.55,(0,255,0),1)

    while True:
        ret, im = cam.read()
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.2, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(im, (x, y), (x + w, y + h), (225, 0, 0), 2)
            Id, conf = recognizer.predict(gray[y:y + h, x:x + w])
            if (Id == 21):
                Id = "KAMESHWAR"
            elif (Id == 3):
                Id = "PRATIK"
            else:
                Id = "Unknown"
            cv2.putText(im, str(Id), (x, y - 10), font, 2, (0, 255, 0), 1)
            # cv2.cv.putText(cv2.cv.fromarray(im),str(Id), (x, y+h), font, 255)
        cv2.imshow('DETECTOR', im)
        if cv2.waitKey(1) == ord('q'):
            break
    cam.release()

btncDetector=Button(f1,padx=20,bd=10,font=('arial',20,'bold'),text="Database",command=lambda: btnstop()).grid(row=0,column=5)


def btnstop():
    for row in c.execute('SELECT * FROM ram'):
        print(row)


root.mainloop()
    
