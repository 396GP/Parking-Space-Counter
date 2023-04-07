#!/usr/bin/env python
# coding: utf-8

# In[1]:


# 이미지 처리위해 cv2 파일 입출력을 위해 pickle

import cv2
import pickle


# In[2]:


# img = cv2.imread('parking.png')

width, height = 55, 34

try: 
    with open('CarParkPos','rb') as f:
        posList = pickle.load(f)
except:
    posList = []


# In[3]:


# 마우스 클릭시 네모가 생기는 것을 처리
def mouseClick(events, x, y, flags, params):
    if events == cv2.EVENT_LBUTTONDOWN:
        posList.append((x, y))
    if events == cv2.EVENT_RBUTTONDOWN:
        for i, pos in enumerate(posList):
            x1, y1 = pos
            if x1 < x < x1 + width and y1<y<y1+height:
                posList.pop(i)
    
    with open('CarParkPos','wb') as f:
        pickle.dump(posList, f)


# In[4]:


while True:
    # cv2.rectangle(사각형을 넣을 이미지 선택,시작 x,y 좌표,종료 x,y 좌표,색상 RGB(0,0,0),선 두께)
    # cv2.rectangle(img,(150,203),(205,169),(255,0,255),2)
    img = cv2.imread('parking.png')
    for pos in posList:
         cv2.rectangle(img, pos,(pos[0] + width, pos[1] + height),(255,0,255),2)
    
    cv2.imshow("Image",img)
    cv2.setMouseCallback("Image",mouseClick)
    cv2.waitKey(1)
    
    # 닫기 명령 1을 누르면 닫힘
    if cv2.waitKey(1) == ord('1'): #1 is the Enter Key
        break


# In[5]:


# 모든 창을 닫는 함수
cv2.destroyAllWindows()


# 
