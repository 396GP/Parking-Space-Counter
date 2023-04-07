#!/usr/bin/env python
# coding: utf-8

# In[1]:


import cv2
import csv
import pickle
import cvzone
import numpy as np


# In[2]:


#Video feed
cap = cv2.VideoCapture('parking.mp4')

#Parking Position file loading
with open('CarParkPos','rb') as f:
    posList = pickle.load(f)


# In[3]:


def checkParkingSpace(imgPro):
    
    spaceCounter = 0
    
    for pos in posList:
        x, y, w, h = pos
        
        imgCrop = imgPro[y:y+h,x:x+w]
        # cv2.imshow("imgCropped",imgCrop)
        cv2.imshow(str(x*y),imgCrop)
        
        # crop된 이미지의 픽셀수를 센다 
        count = cv2.countNonZero(imgCrop)
        # 픽셀수를 지정한 위치에 보여준다, height 뒤 숫자로 위치 조정, scale로 글씨 크기 조정, thickness로 글씨 굵기 조절
        cvzone.putTextRect(img, str(count), (x,y+h-10), scale = 1, thickness = 1, offset = 0, colorR=(0,0,255))
        
        # 픽셀 수에 따라 직사각형 색과 굵기를 변화시켜 있는지 없는지를 표시함
        if count < 400:
            color = (0,255,0)
            thickness = 5
            spaceCounter += 1
        else:
            color = (0,0,255)
            thickness = 2
        cv2.rectangle(img,(pos[0], pos[1]),(pos[0] + pos[2], pos[1] + pos[3]),color,2)
    
    # 주차장 남은 자리를 출력하는 부분
    cvzone.putTextRect(img, f'Free: {spaceCounter}/{len(posList)}', (100,50), scale = 3, thickness = 5, offset = 20, colorR=(0,200,0))
    
    # 주차장 남은 자리를 csv파일로 출력하는 부분
    p = open('write.csv','w', newline='')
    wr = csv.writer(p)
    wr.writerow([1, spaceCounter, len(posList)])
    p.close()


# In[4]:


while True:
    
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES,0)
    
    success, img_o = cap.read()
    (h, w) = img_o.shape[:2]
    center = (w // 2, h // 2)
    # 영상의 (center, 각도, 스케일), SpacePicker와 같은 각도와 스케일이어야 함 매우매우 중요
    M = cv2.getRotationMatrix2D(center, 0, 1)
    img = cv2.warpAffine(img_o, M, (w, h))
    
    # 원래 영상의 image를 크롭한 것
    imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray,(3,3),1)
    # 끝의 두 숫자를 적절하게 조정하여 필요한 차량의 픽셀만 나타내게
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
    # 끝 숫자를 조정하여 필요한 차량의 픽셀만 나타나게
    imgMedian = cv2.medianBlur(imgThreshold, 5)
    
    kernel = np.ones((3,3),np.uint8)
    
    #interations가 높아지면 선이 굵어짐
    imgDilate = cv2.dilate(imgMedian,kernel, iterations=1)
    checkParkingSpace(imgDilate)
    
    # parking space 위치 표시 명령어
    # for pos in posList:
    #    cv2.rectangle(img, pos,(pos[0] + width, pos[1] + hei1ght),(255,0,255),2)
    
    cv2.imshow("Image",img)
    
    # 후처리된 이미지 출력
    # cv2.imshow("ImageBlur",imgBlur)
    # cv2.imshow("ImageThreshold",imgThreshold)
    # cv2.imshow("ImageMedian",imgMedian)
    # cv2.imshow("ImageDilate",imgDilate)
    cv2.waitKey(1)
    
    # 닫기 명령 1을 누르면 닫힘
    if cv2.waitKey(1) == ord('1'): #1 is the Enter Key
        break


# cv2.destroyAllWindows()

# In[ ]:




