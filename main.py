# import the necessary packages
import numpy as np
import argparse
import cv2
import time
 
#ap = argparse.ArgumentParser()
#ap.add_argument("-i", "--image", required = True, help = "Path to the image")
#args = vars(ap.parse_args())
#image = cv2.imread(args["image"])

#Camera 0
cam = cv2.VideoCapture(0)

while True:
	ret, image = cam.read()
	output = image.copy()
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

	circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1.1, 500)
	 

	if circles is not None:
		# convert the (x, y) coordinates
		circles = np.round(circles[0, :]).astype("int")
	 
		# loop over the (x, y) coordinates and radius of the circles
		c = 0
		for (x, y, r) in circles:
			#draw the circle in the output image
			cv2.circle(output, (x, y), r, (0, 255, 0), 4)
			cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 0, 255), -1)

			#Get color from center of circle
			color = image[x, y]
			rgb = str(color.item(2))+","+str(color.item(1))+","+str(color.item(0))

			cv2.putText(output,rgb, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1,(color.item(0),color.item(1),color.item(2)), 2)
			print("Circle "+str(c)+": "+str(x)+","+str(y)+" Color: "+rgb)
			c+=1
	 
		# show the output image
		cv2.imshow("output", output)
		key = cv2.waitKey(100)
		if key == 27:
			cv2.destroyAllWindows()
			break
