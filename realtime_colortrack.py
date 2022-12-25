import cv2 as cv
import numpy as np

def nothing(x):
    pass

cv.namedWindow('HSV Tracbar',cv.WINDOW_AUTOSIZE)

# create trackbars to control Hue, Saturation and Value
cv.createTrackbar('Hue_low','HSV Tracbar',81,180,nothing)
cv.createTrackbar('Hue_up','HSV Tracbar',110,180,nothing)
cv.createTrackbar('Saturation_low','HSV Tracbar',56,255,nothing)
cv.createTrackbar('Saturation_up','HSV Tracbar',137,255,nothing)
cv.createTrackbar('Value_low','HSV Tracbar',125,255,nothing)
cv.createTrackbar('Value_up','HSV Tracbar',255,255,nothing)

# Turn on the Camera
Capture = cv.VideoCapture(0)
center = []

while True:
    isOk,frame = Capture.read()
    if not isOk : break

    hsvImg = cv.cvtColor(frame,cv.COLOR_BGR2HSV)
    
    hueLow = cv.getTrackbarPos('Hue_low','HSV Tracbar')
    hueUp = cv.getTrackbarPos('Hue_up','HSV Tracbar')
    saturationLow = cv.getTrackbarPos('Saturation_low','HSV Tracbar')
    saturationUp = cv.getTrackbarPos('Saturation_up','HSV Tracbar')
    valueLow = cv.getTrackbarPos('Value_low','HSV Tracbar')
    valueUp = cv.getTrackbarPos('Value_up','HSV Tracbar')

    colorLow = np.array([hueLow,saturationLow,valueLow])
    colorUp =np.array([hueUp,saturationUp,valueUp])

    #choose a color range
    maskColor = cv.inRange(hsvImg,colorLow,colorUp)
    
    #Selection of contours based on the selected mask
    contours,_ = cv.findContours(maskColor,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)

    for cont in contours:
        if cv.contourArea(cont) >= 500:
            rect = cv.minAreaRect(cont)            
            boxPoint = cv.boxPoints(rect)
            boxPoint = np.int32(boxPoint)

            # (x,y),r = cv.minEnclosingCircle(cont)
            center.append((boxPoint[1,0],boxPoint[1,1])) 

            cv.drawContours(frame,[boxPoint],-1,(0,255,0),thickness=2)
            cv.circle(frame,(boxPoint[1,0],boxPoint[1,1]),4,(255,0,0),thickness=-1) 
            cv.putText(frame,str((boxPoint[1,0],boxPoint[1,1])),(boxPoint[1,0],boxPoint[1,1]),cv.FONT_HERSHEY_PLAIN,2,(0,0,255)) 

    bitwiseAndImage = cv.bitwise_and(frame,frame,mask=maskColor)        

    #track x,y
    # for cen in center:
    #     cv.circle(frame,(int(cen[0]),int(cen[1])),3,(255,0,0),thickness=5)

    # cv.imshow('mask Image',maskColor)
    cv.imshow('HSV Tracbar',bitwiseAndImage)
    cv.imshow('frame',frame)

    key = cv.waitKey(10)
    if key == 27: break
    elif key== ord('c') : center=[]

cv.destroyAllWindows()
Capture.release()