from pickle import NONE
import joblib
import cv2
from LoadVideo import FramesMeasured
from PoseDatasets import Dataset
import numpy as np
from PoseDetector import PoseMarker
from VideoWrapperClass import RotatingResizingVideoCapture

modelType = input("Which way is the referee facing? ")
if modelType =="Backward":
    model = joblib.load('random_forest_BackFacing.pkl')
    video = RotatingResizingVideoCapture('Backfacing.MOV',rotate_code= cv2.ROTATE_90_CLOCKWISE)
elif modelType =="Forward":
    model = joblib.load('random_forest.pkl')
    video = RotatingResizingVideoCapture('Hand-Signals-Lvl2.mp4')
elif modelType =="LiveTime":
    model = joblib.load('random_forest_LiveTimeArya.pkl')
    video = cv2.VideoCapture(0)




detector = PoseMarker()
loopNum =0
listOfPoints = []
prediction= "Nothing"

if modelType !="LiveTime":
    video.reset()

while True:
    
    loopNum +=1
    ret, frame = video.read()

    if not ret:
        break

    #process frame
    frame_rgb, points = detector.process(frame)
    # Try again if failed
    if points is None:
        frame_rgb, points = detector.process(frame)

    listOfPoints.append(points)

    if loopNum % FramesMeasured ==0 and not listOfPoints.__contains__(None):
        data = Dataset.getFlattened_TestData(listOfPoints, FramesMeasured)

        array = np.array(data[0]).reshape(1,-1)

        prediction = model.predict(array)
        print(prediction)
        listOfPoints=[]

    cv2.putText(frame,text=prediction[0], org = (300,200), fontFace=0, fontScale=6.0, color = (0,0,255), thickness= 4)
    cv2.imshow('Video', frame)

    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()