# USAGE
# python test_handwriting.py --model handwriting.model --image images/hello_world.png

# import the necessary packages
import math

from joblib.numpy_pickle_utils import xrange
from tensorflow.keras.models import load_model
from imutils.contours import sort_contours
import numpy as np
import argparse
import imutils
import cv2


def threeVarReturnInteger(indexOnes):
    result = []
    myDict = {
        0: 0,
        1: 1,
        2: 3,
        3: 2,
        4: 4,
        5: 5,
        6: 7,
        7: 6
    }

    keys = [*myDict]
    for j in range(len(indexOnes)):
        for i in range(len(keys)):
            print(myDict[i])
            print(indexOnes[j])
            if keys[i] == indexOnes[j]:
                result.append(myDict[i])
    return result


def fourVarReturnInteger(indexOnes):
    result = []
    myDict = {
        0: 0,
        1: 1,
        2: 3,
        3: 2,
        4: 4,
        5: 5,
        6: 7,
        7: 6,
        8: 12,
        9: 13,
        10: 15,
        11: 14,
        12: 8,
        13: 9,
        14: 11,
        15: 10
    }

    keys = [*myDict]
    for j in range(len(indexOnes)):
        for i in range(len(keys)):
            if keys[i] == indexOnes[j]:
                result.append(myDict[i])
    return result


def fiveVarReturnInteger(indexOnes):
    result = []
    myDict = {
        0: 0,
        1: 1,
        2: 3,
        3: 2,
        4: 16,
        5: 17,
        6: 19,
        7: 18,
        8: 4,
        9: 5,
        10: 7,
        11: 6,
        12: 20,
        13: 21,
        14: 23,
        15: 22,
        16: 12,
        17: 13,
        18: 15,
        19: 14,
        20: 28,
        21: 29,
        22: 31,
        23: 30,
        24: 8,
        25: 9,
        26: 11,
        27: 10,
        28: 24,
        29: 25,
        30: 27,
        31: 26
    }
    keys = [*myDict]
    for j in range(len(indexOnes)):
        for i in range(len(keys)):
            if keys[i] == indexOnes[j]:
                result.append(myDict[i])
    return result


def Sort_Tuple(tup):
    # getting length of list of tuples
    lst = len(tup)
    for i in range(0, lst):

        for j in range(0, lst - i - 1):
            if (tup[j][0] > tup[j + 1][0]):
                temp = tup[j]
                tup[j] = tup[j + 1]
                tup[j + 1] = temp
    return tup


# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
# ap.add_argument("-i", "--image", required=True,
# 	help="path to input image")
# ap.add_argument("-m", "--model", type=str, required=True,
# 	help="path to trained handwriting recognition model")
# args = vars(ap.parse_args())

# load the handwriting OCR model
print("[INFO] loading handwriting OCR model...")
model = load_model('cnn_model.h5')

# load the input image from disk, convert it to grayscale, and blur
# it to reduce noise
image = cv2.imread('images/5var.png')
image = cv2.resize(image, (560, 320))
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# perform edge detection, find contours in the edge map, and sort the
# resulting contours from left-to-right
edged = cv2.Canny(blurred, 30, 150)
cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
                        cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
cnts = sort_contours(cnts, method="top-to-bottom")[0]

# initalise list for holding characters to be recognised
#
chars = []
sortedlist = []
result = []

# loop over the contours
for c in cnts:
    # compute the bounding box of the contour
    res = cv2.boundingRect(c)
    sortedlist.append(res)

# Number of variables in Karnaugh Map
noKMapVars = int(math.log(len(sortedlist), 2))

#
if noKMapVars == 5:
    output = [sortedlist[i:i + 8] for i in range(0, len(sortedlist), 8)]
else:
    output = [sortedlist[i:i + 4] for i in range(0, len(sortedlist), 4)]

for i in range(len(output)):
    result.append(Sort_Tuple(output[i]))
flat_list = [item for sublist in result for item in sublist]
foo = tuple(flat_list)

for i in range(len(foo)):

    (x, y, w, h) = foo[i]

    # filter out bounding boxes, ensuring they are neither too small
    # nor too large
    if (w >= 5 and w <= 150) and (h >= 15 and h <= 120):
        # extract the character and threshold it to make the character
        # appear as *white* (foreground) on a *black* background, then
        # grab the width and height of the thresholded image
        roi = gray[y:y + h, x:x + w]
        thresh = cv2.threshold(roi, 0, 255,
                               cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        (tH, tW) = thresh.shape

        # if the width is greater than the height, resize along the
        # width dimension
        if tW > tH:
            thresh = imutils.resize(thresh, width=28)

        # otherwise, resize along the height
        else:
            thresh = imutils.resize(thresh, height=28)

        # re-grab the image dimensions (now that its been resized)
        # and then determine how much we need to pad the width and
        # height such that our image will be 28x28
        (tH, tW) = thresh.shape
        dX = int(max(0, 28 - tW) / 2.0)
        dY = int(max(0, 28 - tH) / 2.0)

        # pad the image and force 28x28 dimensions
        padded = cv2.copyMakeBorder(thresh, top=dY, bottom=dY,
                                    left=dX, right=dX, borderType=cv2.BORDER_CONSTANT,
                                    value=(0, 0, 0))
        padded = cv2.resize(padded, (28, 28))

        # prepare the padded image for classification via our
        # handwriting OCR model
        padded = padded.astype("float32") / 255.0
        padded = np.expand_dims(padded, axis=-1)

    # update our list of characters that will be OCR'd

    chars.append((padded, (x, y, w, h)))

# extract the bounding box locations and padded characters
boxes = [b[1] for b in chars]
chars = np.array([c[0] for c in chars], dtype="float32")
# OCR the characters using our handwriting recognition model
preds = model.predict(chars)

# define the list of label names
labelNames = "0123456789"
labelNames += "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
labelNames = [l for l in labelNames]

values = []
# loop over the predictions and bounding box locations together
for (pred, (x, y, w, h)) in zip(preds, boxes):
    # find the index of the label with the largest corresponding
    # probability, then extract the probability and label
    i = np.argmax(pred)
    prob = pred[i]
    label = labelNames[i]

    values.append(i)
    # draw the prediction on the image
    print("[INFO] {} - {:.2f}%".format(label, prob * 100))
    cv2.resize(image, (800, 520))
    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.putText(image, label, (x - 10, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 2)
indexOnes = [i for i, e in enumerate(values) if e == 1]
optimised = []
if noKMapVars == 3:
    optimised = (threeVarReturnInteger(indexOnes))
elif noKMapVars == 4:
    optimised = (fourVarReturnInteger(indexOnes))
elif noKMapVars == 5:
    optimised = (fiveVarReturnInteger(indexOnes))
# show the image
cv2.resize(image, (800, 520))
cv2.imshow("Image", image)
cv2.waitKey(0)
