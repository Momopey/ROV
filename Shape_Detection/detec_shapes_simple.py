# import the necessary packages
from pyimagesearch.shapedetector import ShapeDetector
import argparse
import imutils
import cv2

# construct the argument parse and parse the arguments
#ap = argparse.ArgumentParser()
#ap.add_argument("-i", "--image", required=True,
               # help="path to the input image")
#args = vars(ap.parse_args())

# load the image and resize it to a smaller factor so that
# the shapes can be approximated better
#image = cv2.imread(args["image"])
image = cv2.imread("whitecircle.png")
image = cv2.imread("differentshapes.jpg")
image = cv2.bitwise_not(image)
#image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
resized = imutils.resize(image, width=200)
image = imutils.resize(image, width=200)
ratio = image.shape[0] / float(resized.shape[0])

# convert the resized image to grayscale, blur it slightly,
# and threshold it
gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
ret,thresh = cv2.threshold(blurred,200, 0, 0)
cv2.findContours(blurred, )

# find contours in the thresholded image and initialize the
# shape detector

