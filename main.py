# import the necessary garbage
import numpy as np
import argparse
import cv2
import time
import socket

colors = [["Red","1",255,0,0],["Green","2",0,255,0],["Blue","3",0,0,255],["Yellow","4",255,255,0]]

udpPacket = ["0","0","0","0","0","0","0","0"]
UDP_IP = "127.0.0.1"
UDP_PORT = 2000
 
#Camera 0
cam = cv2.VideoCapture(0)

while True:
	ret, image = cam.read()
	output = image.copy()
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

	circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1.2, 100)
	 
	if circles is not None:
		# convert the (x, y) coordinates
		circles = np.round(circles[0, :]).astype("int")
	 
		# loop over the (x, y) coordinates and radius of the circles
		c = 0
		for (x, y, r) in circles:
			try:
				#draw the circle in the output image
				cv2.circle(output, (x, y), r, (0, 255, 0), 4)
				cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 0, 255), -1)
				
				color = image[x, y]
				rgb = str(color.item(2))+","+str(color.item(1))+","+str(color.item(0))

				closestColor = colors[0][0]
				closestColorID = colors[0][1]
				closestColorValue = 765
				
				#Calculate what current color is closest to as defined in colors array
				for item in colors:
					valR = abs(item[2]-color.item(2))
					valG = abs(item[3]-color.item(1))
					valB = abs(item[4]-color.item(0))
		
					RGBSum = valR+valG+valB
					if RGBSum < closestColorValue:
						closestColorValue = RGBSum
						closestColor = item[0]
						closestColorID = item[1]
						
				print("Circle "+str(c)+": "+str(x)+","+str(y)+" Color: "+str(rgb)+" Closest Color: "+closestColor)
				cv2.putText(output,closestColor, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1,(255,255,255), 2)
				udpPacket[c] = closestColorID
				c+=1
			except IndexError:
				print("Debug: Circle outside range")

	#print(udpPacket)
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
	sock.sendto(''.join(udpPacket).encode(), (UDP_IP, UDP_PORT))
	 
	# show the output image
	cv2.imshow("output", output)
	key = cv2.waitKey(10)
	if key == 27:
		cv2.destroyAllWindows()
		break
