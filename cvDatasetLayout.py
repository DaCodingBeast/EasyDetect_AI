from turtle import fillcolor
import cv2
import numpy as np

class Canvas():
    def __init__(self,labelList:list, totalWidth = 700, totalLength= 920, gridx = 3, gridy = 4):
        self.totalLength = totalLength
        self.totalWidth = totalWidth
        self.gridy = gridy
        self.gridx = gridx


        self.clicked = False
        
        
        image = np.ones((totalLength,totalWidth,3), dtype= np.uint8) * 255

        labels= []
        counter = 0
        for r in range(gridy):
            list = []
            for c in range(gridx):
                text= labelList[counter]
                list.append(text)

                start_point = (totalWidth//gridx *c, totalLength//gridy*r)
                end_xypoint = (totalWidth//gridx * (c+1),totalLength//gridy * (r+1))
                x1,y1 = start_point

                cv2.rectangle(image, start_point, end_xypoint, (250,0,0),10)
                cv2.putText(image,  text, (x1 + (totalWidth//gridx)//6, y1 + (totalLength//gridx)//2 -15), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0),3)
                counter+=1
            labels.append(list)

        self.labels = labels
        self.image = image

    def run(self):
        cv2.imshow("image",self.image)
        cv2.setMouseCallback("image",self.mouse_callback)

    
    def mouse_callback(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:  # Left click
            col =x // (self.totalWidth//self.gridx)
            row = y // (self.totalLength//self.gridy)

            if 0 <= row < self.gridy and 0 <= col < self.gridx:
                self.label =  self.labels[row][col]
                self.clicked= True



    