# import nescessary modules
import cv2
import numpy as np
import time
import sys
import pprint

# run a quick test to see that everything imported
if 'cv2' and 'numpy' and 'time' and 'sys' and 'pprint' in sys.modules.keys():
    True  # if all of the modules are present do nothing and continue
else:
    for M in ('cv2', 'numpy', 'time', 'sys', 'pprint'):
        if M in sys.modules.keys() != True:
            raise ImportError('The test for required modules has failed!')
            sys.exit()


# After confirming that all modules are properly imported, we need to define an error for and test
# to see if the camera is connected, in the event that the camera is not connected, we throw the
# error and terminate.
class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class zCameraError(Error):
    """Exception raised for camera errors.

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, expression, message):
        self.expression = expression
        self.message = message


# Create a function to close an open window
def close(window_name):
    """Defines some closure conditions for open cv2 windows where window_name is the name of the open window, using 'esc' or hitting 'x' causes the window to close and the program to terminate"""
    k = cv2.waitKey(1) & 0xFF
    if k == 27:  # Close window using 'ESC'
        cap.release()
        cv2.destroyAllWindows()
    if cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1:  # Close window using the 'x' in the title bar if the window name string in the following if statement does not match the window's name it will close after drawing for the length of time defined by waitkey
        cap.release()
        cv2.destroyAllWindows()


# Test to see if the camera is connected.
if cv2.VideoCapture(0).read()[0] == False:
    raise CameraError('The Webcam test failed, No Camera is detected!')
    sys.exit()

# Initiate unfiltered video capture under cap
cap = cv2.VideoCapture(0)

# Test to see if 'cap' was hoisted by cv2 (this is apparently an issue, the following was added because type issues were
# occuring involving cap however the root of those issues could not conclusively be linked to 'cap' itself, as far as
# the documentation goes 'cap' can be any unreserved variable)
if cap.isOpened() == False:
    raise CameraError("'Cap' did not hoist!")
    sys.exit()

# Initiate main image capture and process loop, if
while (True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    frame == True #Full Abort if no frames have been grabbed

    # Our operations on the frame come here
    # Change the colorspace for...reasons (Simpler to dissect the colors?, as i've read Colorspaces are just different
    # mathematical organizations of colors and higher values in HSV are greater saturations, so it seems that by
    # converting to HSV we can remove the drastic colors once we mask, by setting the upper and lower values of this
    # drastic scale (HSV cylinder image https://upload.wikimedia.org/wikipedia/commons/thumb/3/33/HSV_color_solid_cylinder_saturation_gray.png/296px-HSV_color_solid_cylinder_saturation_gray.png")
    # upon further consideration, it seems that Masking the image in HSV is better for solid colored object tracking, by
    # nature of the project HSV isnt appropriate

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_red = np.array([30, 150, 50])  # define lower range of red color in HSV (the beginning of the red 'slice of pie')
    upper_red = np.array([255, 255, 180])  # define upper range of red color in HSV (the end of the red 'slice of pie')
    mask = cv2.inRange(hsv, lower_red, upper_red)  # create a red HSV colour boundary and threshold HSV image (The entire slice of pie)
    res = cv2.bitwise_and(frame, frame, mask=mask)  # Bitwise-AND mask and original image
    contoured_image = cv2.Canny(frame, 300, 400)  # using canny to contour the original image

    contours, hierarchy = cv2.findContours(cv2.Canny(frame, 200, 300), 1, 2)
    cnt = contours[0]
    M = cv2.moments(cnt)  # get image 'moments'
    z_division_error = 0
    try:
        try:  # wrapped in try catch because shape moments kept throwing zero div issues
            # calculate x,y coordinate of center
            cX = abs(int(M["m10"] / M["m00"]))
            cY = abs(int(M["m01"] / M["m00"]))
        except ZeroDivisionError:
            z_division_error += 1
            print('Zero Division Error!, Instances =' + str(z_division_error))
            print("cX:" + str(cX) + ", cY:" + str(cY))
            close('Contoured Shape')
        else:
            image = cv2.line(contoured_image, (cX, 0), (cX, contoured_image.shape[1]), (255, 255, 255), 1)
            image = cv2.line(contoured_image, (0, cY), (contoured_image.shape[1], cY), (255, 255, 255), 1)
            cv2.imshow('Contoured Shape', image)
    except IndexError:
        break

    # closure function to keep from redefining how to close the windows etc
    # close('Frame')

# dump the camera from memory and close all cv2 windows if for some reason the loop is closed by someone other than close()
cap.release()
cv2.destroyAllWindows()
sys.exit()  # Exit program having trouble with the program throwing an index error and continuing to run in the background, concurent instances cannot call the camera if the program is still running
