import cv2
import numpy as np
import time

# replace the red pixels ( or undesired area ) with background pixels to generate the invisibilty feature.

#1. Hue : This channel encodes color information. Hue can be thought of an angle where 0 degree corresponds to the red color, 
#120 degrees corresponds to the green color, and 240 degrees corresponds to the blue color.
#2. Saturation : This channel encodes the intensity/purity of color. For example, pink is less saturated than red.
#3. Value : This channel encodes the brightness of color. Shading and gloss components of an image appear in this channel
#reading the videocapture video  


print(cv2.__version__)  # in order to check the cv2 version 
capture_video = cv2.VideoCapture("video.mp4")   #taking video.mp4 as input. Make your path according to your needs 

#give the camera to warm up
time.sleep(1) 
count = 0 
background = 0 

#capturing the background in range of 60
#you should have video that have some seconds dedicated to background frame so that it could easily save the background image
for i in range(60):
	return_val , background = capture_video.read()
	if return_val == False :
		continue 

background = np.flip(background, axis=1) #flipping of the frame 

# we are reading from video 
while (capture_video.isOpened()):
	return_val, img = capture_video.read()
	if not return_val :
		break 
	count = count + 1
	img = np.flip(img , axis=1)
	# convert the image - BGR to HSV
	# as we focused on detection of red color 
	hsv = cv2.cvtColor(img , cv2.COLOR_BGR2HSV) #converting BGR to HSV for better detection or you can convert it to gray
	# generating mask to detect red color
	# HSV
	# it should be mono-color cloth 
	# lower range
	#-------------------------------------BLOCK----------------------------#
	lower_red = np.array([100, 40, 40])       
	upper_red = np.array([100, 255, 255])
	mask1 = cv2.inRange(hsv,lower_red,upper_red)
   
	lower_red = np.array([155, 40, 40])
	upper_red = np.array([180, 255, 255])
	mask2 = cv2.inRange(hsv,lower_red,upper_red)
	#----------------------------------------------------------------------#
	#the above block of code could be replaced with some other code depending upon the color of your cloth 
	mask1 = mask1+mask2
    # Refining the mask corresponding to the detected red color
	mask1 = cv2.morphologyEx(mask1, cv2.MORPH_OPEN, np.ones((3,3),np.uint8),iterations=2)
	mask1 = cv2.dilate(mask1,np.ones((3,3),np.uint8),iterations = 1)
	mask2 = cv2.bitwise_not(mask1)
    # Generating the final output
	res1 = cv2.bitwise_and(background,background,mask=mask1)
	res2 = cv2.bitwise_and(img,img,mask=mask2)
	cv2.imshow("res1",res1)
	cv2.imshow("res2",res2)
	final_output = cv2.addWeighted(res1,1,res2,1,0)

	#cv2.imshow("INVISIBLE MAN",final_output)
	k = cv2.waitKey(10)
	if k == 27:
		break






