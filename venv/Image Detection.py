# OpenCV program to perform Edge detection in real time
# import libraries of python OpenCV
# where its functionality resides
import cv2
# np is an alias pointing to numpy library
import numpy as np
import time
import sys
# capture frames from a camera
cap = cv2.VideoCapture(0)
# loop runs if capturing has been initialized
while (1):
    # cv2.imshow('Original',frame)
    ret, frame = cap.read()     # reads frames from a camera
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV) # converting BGR to HSV
    lower_red = np.array([30, 150, 50]) # define lower range of red color in HSV
    upper_red = np.array([255, 255, 180]) # define upper range of red color in HSV
    mask = cv2.inRange(hsv, lower_red, upper_red) # create a red HSV colour boundary and threshold HSV image
    res = cv2.bitwise_and(frame, frame, mask=mask) # Bitwise-AND mask and original image
    #contoured_image = cv2.Canny(frame, 200, 300)     #using canny to contour the original image
    contoured_image = cv2.Canny(frame, 300, 400)  # using canny to contour the original image

    contours, hierarchy = cv2.findContours(cv2.Canny(frame, 200, 300), 1, 2)
    cnt = contours[0]
    M = cv2.moments(cnt) #get image 'moments'
    #cv2.imshow('Contoured',contoured_image)
    z_division_error = 0
    try:
        try:#wrapped in try catch because shape moments kept throwing zero div issues
            # calculate x,y coordinate of center
            cX = abs(int(M["m10"] / M["m00"]))
            cY = abs(int(M["m01"] / M["m00"]))
        except ZeroDivisionError:
            z_division_error += 1
            print('Zero Division Error!, Instances ='+str(z_division_error))
        print("cX:" + str(cX) + ", cY:" + str(cY))
        # Wait for Esc key to stop
        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            print('Tried to close with ESC key!')
            break
        # if cv2.getWindowProperty('Contoured Shape', cv2.WND_PROP_VISIBLE) < 1: #closes on xout
        #     print('Tried to close with window button!')
        #     break
        else:
            image = cv2.line(contoured_image,(cX,0),(cX,contoured_image.shape[1]),(255,255,255),1)
            image = cv2.line(contoured_image, (0,cY), (contoured_image.shape[1],cY), (255,255,255), 1)
            cv2.imshow('Contoured Shape',image)
    except IndexError:
        break
# Close the window
cap.release()
# De-allocate any associated memory usage
cv2.destroyAllWindows()
sys.exit() #exit program having trouble with the program throwing an index error and continuing to run in the background, concurent instances cannot call the camera if the program is still running

