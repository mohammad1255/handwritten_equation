import tkinter as tk
from tkinter import filedialog, Label
from tkinter import messagebox
from PIL import Image, ImageTk
import cv2 as cv
import numpy as np
import imutils
import win32api
from keras.models import load_model
import matplotlib.pyplot as plt
dict_word = {0:'A',1:'B',2:'C',3:'D',4:'E',5:'F',6:'G',7:'H',8:'I',9:'J',10:'K',11:'L',12:'M',13:'N',14:'O',15:'P',16:'Q',17:'R',18:'S',19:'T',20:'U',21:'V',22:'W',23:'X',24:'Y',25:'Z'}
model = load_model('best_model.h5')
def sort_contours(cnts, method="left-to-right"):
    reverse = False
    i = 0
    if method == "right-to-left" or method == "bottom-to-top":
        reverse = True
    if method == "top-to-bottom" or method == "bottom-to-top":
        i = 1
    boundingBoxes = [cv.boundingRect(c) for c in cnts]
    (cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes),
    key=lambda b:b[1][i], reverse=reverse))
    return (cnts, boundingBoxes)

def get_letters(img_path):
    letters = []
    image = cv.imread(img_path)
    gray1 = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    ret, thresh1 = cv.threshold(gray1, 127, 255, cv.THRESH_BINARY_INV)
    dilated = cv.dilate(thresh1, None, iterations=2)
    cnts = cv.findContours(dilated.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sort_contours(cnts, method="left-to-right")[0]

    for c in cnts:
        if cv.contourArea(c) > 10:
            (x, y, w, h) = cv.boundingRect(c)
            roi = gray1[y:y + h, x:x + w]
            plt.imshow(roi)
            plt.show()
            thresh = cv.threshold(roi, 0, 255, cv.THRESH_BINARY_INV | cv.THRESH_OTSU)[1]
            thresh = cv.resize(thresh, (28, 28), interpolation=cv.INTER_CUBIC)
            gray = cv.medianBlur(thresh, 5)
            ret, gray = cv.threshold(gray, 75, 180, cv.THRESH_BINARY)
            gray = gray / 255.0  
            gray = cv.resize(gray, (28, 28))
            gray = np.reshape(gray, (28, 28))
            pred = dict_word[np.argmax(model.predict(np.reshape(gray, (1, 28, 28, 1))))]
            letters.append(pred)

    return letters, image
class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Handwritten Character Recognition")
        window_width = 500
        window_height = 500
        screen_width = win32api.GetSystemMetrics(0)
        screen_height = win32api.GetSystemMetrics(1)
        x = int((screen_width - window_width) / 2)
        y = int((screen_height - window_height) / 2)
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")
        image = Image.open("background.jpg")
        image = image.resize((500, 500))
        self.background_image = ImageTk.PhotoImage(image)
        self.background_label = tk.Label(self, image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.label = Label(self, text="مشروع أعد لنيل درجة الإجازة في الهندسة المعلوماتية ", font=("Arial", 14))
        self.label.pack(pady=20)
        self.image_label = Label(self,text='إشراف الدكتور باسل زيتي', font=("Arial", 14))
        self.image_label.pack(pady=20)
        self.image_label1 = Label(self,text=' إعداد الطلاب زين يوسف حيدر بدور شذا أبو ليث', font=("Arial", 14))
        self.image_label1.pack(pady=20)

        self.result_label = Label(self, text="", font=("Arial", 14))
        self.result_label.pack(pady=20)

        self.upload_button = tk.Button(self, text="Upload Image", command=self.upload_image)
        self.upload_button.pack(pady=20)

    def upload_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            letters, image= get_letters(file_path)
            s=''
            for i in letters:
                s+=i
            # cv.putText(image, i, (0,0), cv.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
            self.result_label.config(text=s)
            plt.imshow(image)
            plt.show()

if __name__ == "__main__":
    app = Application()
    app.mainloop()
