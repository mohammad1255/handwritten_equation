import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from keras.models import load_model
model = load_model('best_model.h5')
dict_word = {0:'A',1:'B',2:'C',3:'D',4:'E',5:'F',6:'G',7:'H',8:'I',9:'J',10:'K',11:'L',12:'M'
             ,13:'N',14:'O',15:'P',16:'Q',17:'R',18:'S',19:'T',20:'U',21:'V',22:'W',23:'X', 24:'Y',25:'Z'}
images = [cv.imread('image/W.jpg')]
gray = cv.cvtColor(images[0], cv.COLOR_BGR2GRAY)
gray = cv.medianBlur(gray,5)
ret,gray = cv.threshold(gray,75,180,cv.THRESH_BINARY)
element = cv.getStructuringElement(cv.MORPH_RECT,(90,90))
gray = cv.morphologyEx(gray,cv.MORPH_GRADIENT,element)
gray = gray/255.
gray = cv.resize(gray, (28,28)) 
gray = np.reshape(gray, (28, 28))
pred = dict_word[np.argmax(model.predict(np.reshape(gray,(1,28,28,1))))]
cv.putText(images[0], pred, (100,300), cv.FONT_HERSHEY_SIMPLEX, 10, (255, 0, 0), 2)
plt.imshow(images[0])
plt.show()
    