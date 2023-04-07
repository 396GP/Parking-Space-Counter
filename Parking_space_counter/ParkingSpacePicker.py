#!/usr/bin/env python
# coding: utf-8

# In[1]:


# 이미지 처리위해 cv2 파일 입출력을 위해 pickle

import cv2
import pickle


# In[2]:


# img = cv2.imread('parking.png')
try: 
    with open('CarParkPos','rb') as f:
        posList = pickle.load(f)
except:
    posList = []


# In[3]:


# 사각형 좌표
rect_start = None
rect_end = None

# 마우스 이벤트 핸들러
def mouseClick(event, x, y, flags, param):
    global rect_start, rect_end, img
    if event == cv2.EVENT_LBUTTONDOWN:
        rect_start = (x, y)
    elif event == cv2.EVENT_LBUTTONUP:
        rect_end = (x, y)
    elif event == cv2.EVENT_MOUSEMOVE and flags == cv2.EVENT_FLAG_LBUTTON:
        # 마우스 왼쪽 버튼이 눌리고 있는 중에만
        if rect_start is not None:
            # 좌상단, 우하단 좌표 계산
            x1, y1 = rect_start
            x2, y2 = x, y
            x, y = min(x1, x2), min(y1, y2)
            w, h = abs(x1 - x2), abs(y1 - y2)

            # 이미지 복사
            img_draw = img.copy()

            # 사각형 그리기
            cv2.rectangle(img_draw, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # 이미지 출력
            cv2.imshow("Image", img_draw)
        else:
            img_draw = img.copy()
            cv2.imshow("Image", img_draw)
    
    # 버그 가능성 있음
    if rect_start and rect_end:
        x1, y1 = rect_start
        x2, y2 = rect_end
        x, y = min(x1, x2), min(y1, y2)
        w, h = abs(x1 - x2), abs(y1 - y2)
        
        posList.append((x, y, w, h))
        
        rect_start, rect_end = None, None
        
        
    if event == cv2.EVENT_RBUTTONDOWN:
        for i, pos in enumerate(posList):
            x1, y1, w, h = pos
            if x1 < x < x1 + w and y1<y<y1+h:
                posList.pop(i)
    
    with open('CarParkPos','wb') as f:
        pickle.dump(posList, f)


# In[4]:


while True:
    # cv2.rectangle(사각형을 넣을 이미지 선택,시작 x,y 좌표,종료 x,y 좌표,색상 RGB(0,0,0),선 두께)
    # cv2.rectangle(img,(150,203),(205,169),(255,0,255),2)
    img_o = cv2.imread('parking.png')
    (h, w) = img_o.shape[:2]
    center = (w // 2, h // 2)
    # 영상의 (center, 각도, 스케일)
    M = cv2.getRotationMatrix2D(center, 0, 1)
    img = cv2.warpAffine(img_o, M, (w, h))
    
    for pos in posList:
         cv2.rectangle(img, (pos[0], pos[1]) ,(pos[0] + pos[2], pos[1] + pos[3]),(255,0,255),2)
    
    cv2.imshow("Image",img)
    cv2.setMouseCallback("Image",mouseClick)
    cv2.waitKey(1)
    
    # 닫기 명령 1을 누르면 닫힘
    if cv2.waitKey(1) == ord('1'): #1 is the Enter Key
        break


# cv2.destroyAllWindows()
