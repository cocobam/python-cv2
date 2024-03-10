import numpy as np
import scipy.ndimage as ndi

import cv2
cap = cv2.VideoCapture('C:\\Users\\User\\Desktop\\數位影像處理\\車道線偵測\\video_day_1.avi')
while(cap.isOpened()):
    ret, frame = cap.read()
    #影像灰階
    
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))    # 取得影像寬度
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # 取得影像高度
    fourcc = cv2.VideoWriter_fourcc('X', 'V', 'I', 'D')          # 設定影片的格式為 MJPG
    out = cv2.VideoWriter('output.avi', fourcc, 20.0, (width,  height))  # 產生空的影片 
    x = 300
    y = 300
    w = 400
    h = 230
    
    xx = 300
    ww = 800
    if(ret == None):
        break
    
    graym = frame[y:y+h, x:x+w]
    graym2 = frame[y:y+h, xx:xx+ww]
  
    

    gray = cv2.cvtColor(graym, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(graym2, cv2.COLOR_BGR2GRAY)
    
    resMin =  cv2.GaussianBlur(gray,(3,3),0)
    resMin2 =  cv2.GaussianBlur(gray2,(3,3),0)
    
    
    graycanny = cv2.Canny(resMin,20,300)
    graycanny2 = cv2.Canny(resMin2,20,300)
    
    kernel= np.array([[-1, -1, -1, -1, -1], [-1, 1, 2, 1, -1], [-1, 2, 4, 2, -1],[-1, 1, 2, 1, -1],
[-1, -1, -1, -1, -1]])
    dst = cv2.filter2D(graycanny,-1,kernel)
    kernel= np.array([[-1, -1, -1, -1, -1], [-1, 1, 2, 1, -1], [-1, 2, 4, 2, -1],[-1, 1, 2, 1, -1],
[-1, -1, -1, -1, -1]])
    dst2 = cv2.filter2D(graycanny2,-1,kernel)
    
    minLineLength=0
    maxLineGap=10
    lines = cv2.HoughLinesP(dst, 1, np.pi/180, 10, minLineLength, maxLineGap)
    lines2 = cv2.HoughLinesP(dst2, 1, np.pi/180, 10, minLineLength, maxLineGap)
    # Draw lines on the image
    
    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv2.line(frame[y:y+h, x:x+w], (x1, y1), (x2, y2), (0, 0, 255), 5)
    for line in lines2:
        x1, y1, x2, y2 = line[0]
        cv2.line(frame[y:y+h, xx:xx+ww], (x1, y1), (x2, y2), (0, 0, 255), 5)
    
    out.write(frame)  
    cv2.imshow('frame',frame)
    cv2.waitKey(27)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()