import cv2
import numpy as np
from pynput.mouse import Button, Controller
import wx

mouse = Controller()

app = wx.App(False)
(sx, sy) = wx.GetDisplaySize()
(camx, camy) = (320, 240) # cv2 Frame for with WX
"""
# for blue colore
lowerBound = np.array([110,50,50])
upperBound = np.array([130,255,255])
"""
# for green colore
lowerBound = np.array([33, 80, 40])
upperBound = np.array([102, 255, 255])

cam = cv2.VideoCapture(0)
cam.set(3, camx)
cam.set(4, camy)


kernelOpen = np.ones((5, 5))
kernelClose = np.ones((20, 20))


# Dampling method(this method don't allow mose to move to fast!)
mLocOld = np.array([0, 0])
mouseLoc = np.array([0, 0])
# mouseLoc = mLocOld+(targetLoc-mLocOld)/DampinFactor //" The more DampingValue The more mouse movement will be smoother"
DampinFactor = 2  # This DampingFactor value should be morethen 1(>1)

while True:
	ret, img = cam.read()
	#img = cv2.resize(img, (340,220)) # cv2Frame

	#convert BGR to HSV
	imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

	#creat the Mask
	mask = cv2.inRange(imgHSV, lowerBound, upperBound)

	#mophology
	maskOpen = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernelOpen)
	maskClose = cv2.morphologyEx(maskOpen, cv2.MORPH_CLOSE, kernelClose)
 
	maskFinal = maskClose
	_, conts, h = cv2.findContours(maskFinal.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

	# Opening Objects	
	if(len(conts) == 2):
		mouse.release(Button.left)
		x1, y1, w1, h1 = cv2.boundingRect(conts[0])
		x2, y2, w2, h2 = cv2.boundingRect(conts[1])
		cv2.rectangle(img, (x1, y1), (x1+w1, y1 + h1), (255, 0, 0), 2)
		cv2.rectangle(img, (x2, y2), (x2+w2, y2 + h2), (255, 0, 0), 2)


		# To draw line and DOT co-ordinate to control activity
		cx1 = x1+w1/2
		cy1 = y1+h1/2
		cx2 = x2+w2/2
		cy2 = y2+h2/2
		# find the center of co-ordinate for circle
		cx = (cx1 + cx2)/2
		cy = (cy1+cy2)/2
		cv2.line(img, (cx1, cy1), (cx2, cy2), (255, 0, 0), 2)
		cv2.circle(img, (cx, cy), 2, (0, 0, 255), 2)
		
		mouseLoc=mLocOld+((cx, cy)-mLocOld)/DampinFactor # //" The more DampingValue The more mouse movement will be smoother"
		
		mouse.position = (sx - (mouseLoc[0]*sx/camx),mouseLoc[1]*sy/camy)
		while mouse.position != (sx - (mouseLoc[0]*sx/camx),mouseLoc[1]*sy/camy):
			pass
		mLocOld = mouseLoc
		"""
		mouse.position = (sx - (cx*sx/camx),cy*sy/camy)
		while mouse.position != (sx - (cx*sx/camx),cy*sy/camy):
			pass
		"""
	# Closing objects
	elif(len(conts) == 1):
		x, y, w, h = cv2.boundingRect(conts[0])
		cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0),2)
		cx = x + w/2
		cy = y + h/2
		cv2.circle(img, (cx, cy), (w+h)/4, (0, 0, 255), 2)
		#mouse.position = (sx - (cx*sx/camx),cy*sy/camy)
		
		mouseLoc=mLocOld+((cx, cy)-mLocOld)/DampinFactor # //" The more DampingValue The more mouse movement will be smoother"
		
		mouse.position = (sx - (mouseLoc[0]*sx/camx),mouseLoc[1]*sy/camy)
		while mouse.position != (sx - (mouseLoc[0]*sx/camx),mouseLoc[1]*sy/camy):
			pass
		mLocOld = mouseLoc
		"""
		mouse.position = (sx - (cx*sx/camx),cy*sy/camy)
		while mouse.position != (sx- (cx*sx/camx),cy*sy/camy):
			pass
		"""
		mouse.press(Button.left)
	# cv2.drawContours(img, conts, -1,(255, 0, 0), 3) #NO need of multimple contores
	"""
	# Don't need to draw the rectengle
	for i in range(len(conts)):
		x, y, w, h = cv2.boundingRect(conts[i])
		cv2.rectangle(img, (x, y),(x+w, y+h), (0, 0, 255), 2)
		#cv2.PutText(cv2.framarray(img), str(i+1), (x,y+h),(0, 255, 255))
	"""
	



	cv2.imshow("maskclose", maskClose)
	#cv2.imshow("maskOpen", maskOpen)
	#cv2.imshow("mask", mask)
	cv2.imshow("cam", img)
	
	k = cv2.waitKey(5) & 0xFF
	if k == 27:
		break

cam.release()
cv2.destroyAllWindows()