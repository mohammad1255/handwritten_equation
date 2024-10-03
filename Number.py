import tkinter as tk
import tkinter.messagebox
import win32gui
import numpy as np
import tensorflow as tf
from PIL import ImageGrab

def initialize():
    top = tk.Tk()
    top.geometry("300x350")
    top.title("HCR")
    model = tf.keras.models.load_model("model/model.h5")
    return top, model
# We create a dictionary word_dict to map the integer values with the characters.
word_dict = {0:'0',1:'1',2:'2',3:'3',4:'4',5:'5',6:'6',7:'7',8:'8',9:'9',10:'A',11:'B',12:'C',13:'D',14:'E',15:'F',
             16:'G',17:'H',18:'I',19:'J',20:'K',21:'L',22:'M',23:'N', 24:'O',25:'P',26:'Q',27:'R',28:'S',29:'T',30:'U',
             31:'V',32:'W',33:'X',34:'Y',35:'Z',36:'a',37:'b',38:'c',39:'d',40:'e',41:'f',42:'g',43:'h',44:'i',45:'j',
             46:'k',47:'l',48:'m',49:'n', 50:'o',51:'p',52:'q',53:'r',54:'s',55:'t',56:'u',57:'v',58:'w',59:'x',60:'y',
             61:'z'}
def decode(num):
    return num if num <= 9 else int(num) + 55

def clear():
    canvas.delete("all")

def predict():
    # Step 1 : Getting the canvas ID
    canvas_handle = canvas.winfo_id()
    # Step 2 : Get the canvas from ID
    canvas_rect = win32gui.GetWindowRect(canvas_handle)
    # Step 3 : Get the canvas content
    img = ImageGrab.grab(canvas_rect)
    # Step 4 : Resize the content for CNN input
    img = img.resize((28, 28)).convert("L")
    img = np.array(img)
    img = img.reshape((1, 28, 28, 1))
    img = img / 255.0
    # Step 5 : Predict the image drawn
    Y = model.predict([img])[0]
    tkinter.messagebox.showinfo("Prediction", "it's a " + str(decode(np.argmax(Y))))


def mouse_event(event):
    x, y = event.x, event.y
    canvas.create_oval(x, y, x, y, fill='white', outline='white', width=25)


(root, model) = initialize()
button_frame = tk.Frame(root)

canvas = tk.Canvas(root, bg="black", height=300, width=300)
canvas.bind('<B1-Motion>', mouse_event)
clear_button = tk.Button(button_frame, text="Clear", command=clear)
predict_button = tk.Button(button_frame, text="Predict", command=predict)

canvas.pack()
clear_button.pack(side="left")
predict_button.pack(side="right")

button_frame.pack()
root.mainloop()
