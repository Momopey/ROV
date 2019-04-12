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
image = cv2.imread("whitecircle.png") #read raw image
image = cv2.imread("differentshapes.jpg") #read raw image
image = cv2.imread("6shapes.jpg") #read raw image
image = cv2.bitwise_not(image) #flip the image to negative
#image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
image = imutils.resize(image, width=500) #resize it to 500px in width
#ratio = image.shape[0] / float(resized.shape[0])
ratio = 1.0

cap = cv2.VideoCapture(0) #grab raw video from camera

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read() #read the frame in every loop
    rawResized = imutils.resize(frame, width=500) #resize
    resized = imutils.resize(frame, width=500) #resize
    margin = 5
    resized = resized[margin:margin + (cv2.CAP_PROP_FRAME_HEIGHT - margin*2), margin:margin + (cv2.CAP_PROP_FRAME_WIDTH - margin*2)] #cut the frame by approx 5 pix
    resized = cv2.bitwise_not(resized)
    # Our operations on the frame come here
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (11, 11), 0)
    # Display the resulting frame

    ret, thresh = cv2.threshold(blurred, 100, 120, cv2.THRESH_BINARY)
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    print("Total contour(s) found: " + str(len(cnts)))
    sd = ShapeDetector()
    qualifiedShape = 0
    for c in cnts:
        # compute the center of the contour, then detect the name of the
        # shape using only the contour
        M = cv2.moments(c)
        if (M["m00"] != 0) and (cv2.contourArea(c) > 2000) and (cv2.contourArea(c) < 8000):
            cX = int((M["m10"] / M["m00"]) * ratio)
            cY = int((M["m01"] / M["m00"]) * ratio)
            shape = sd.detect(c)
            print("Possible shape: " + shape)
            # multiply the contour (x, y)-coordinates by the resize ratio,
            # then draw the contours and the name of the shape on the image
            c = c.astype("float")
            c *= ratio
            c = c.astype("int")
            cv2.drawContours(resized, [c], -1, (0, 255, 0), 2)
            cv2.putText(resized, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, (255, 255, 255), 2)
            qualifiedShape += 1
    cv2.imshow('frame', resized)
    cv2.imshow('blurred', blurred)
    cv2.imshow('raw', rawResized)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

'''
# convert the resized image to grayscale, blur it slightly,
# and threshold it
gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
#thresh = cv2.threshold(blurred, 80, 150, cv2.THRESH_BINARY)[1]
ret,thresh = cv2.threshold(blurred, 30, 150, cv2.THRESH_BINARY)
# find contours in the thresholded image and initialize the
# shape detector
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                        cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
sd = ShapeDetector()

#cv2.imshow("Image", blurred)
#cv2.waitKey(0)
# loop over the contours
print("Total contour(s) found: "+ str(len(cnts)))
qualifiedShape = 0
for c in cnts:
    # compute the center of the contour, then detect the name of the
    # shape using only the contour
    M = cv2.moments(c)
    if (M["m00"] != 0) and (cv2.contourArea(c) > 3000):
        cX = int((M["m10"] / M["m00"]) * ratio)
        cY = int((M["m01"] / M["m00"]) * ratio)
        shape = sd.detect(c)
        print("Possible shape: "+ shape)
        # multiply the contour (x, y)-coordinates by the resize ratio,
        # then draw the contours and the name of the shape on the image
        c = c.astype("float")
        c *= ratio
        c = c.astype("int")
        cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
        cv2.putText(image, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, (255, 255, 255), 2)
        qualifiedShape+=1
print("Total qualified contour(s) found: " + str(qualifiedShape))
    # show the output image
cv2.imshow("Image", image)
cv2.waitKey(0)
'''