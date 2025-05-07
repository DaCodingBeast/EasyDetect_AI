from pickle import NONE
import joblib
import cv2
from LoadVideo import FramesMeasured
from PoseDatasets import Dataset
import numpy as np
from PoseDetector import PoseMarker
from VideoWrapperClass import RotatingResizingVideoCapture
modelType = "LiveTime"
# modelType = input("Which way is the referee facing? ")
if modelType =="Backward":
    model = joblib.load('random_forest_BackFacing.pkl')
    video = RotatingResizingVideoCapture('Backfacing.MOV',rotate_code= cv2.ROTATE_90_CLOCKWISE)
elif modelType =="Forward":
    model = joblib.load('random_forest.pkl')
    video = RotatingResizingVideoCapture('Hand-Signals-Lvl2.mp4')
elif modelType =="LiveTime":
    model = joblib.load('random_forest_LiveTimeArya.pkl')
    capController = cv2.VideoCapture(2)
    video = RotatingResizingVideoCapture('aryaDancing.mp4')
    capController.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    capController.set(cv2.CAP_PROP_FRAME_HEIGHT, 800)


detector = PoseMarker()
loopNum =0
listOfPoints = []
prediction= "Nothing"

video.reset()


ret,frame = capController.read()

def getPointsFromFrame():
    global ret,frame
    ret,frame = capController.read()
    frame_rgb, points = detector.process(frame)
    cv2.imshow('Video', frame)
    return frame_rgb, points


while True:
    
    loopNum +=1
    # if modelType =="LiveTime":
    
        # frame = video.readFrame(frame)
    # else:
        # ret, frame = video.read()

    #process frame
    
    # Try again if failed
    frame_rgb, points = getPointsFromFrame()

    while points is None:
        frame_rgb, points = getPointsFromFrame()


    listOfPoints.append(points)

    print(listOfPoints.__contains__(None))

    if loopNum % FramesMeasured ==0 :
        data = Dataset.getFlattened_TestData(listOfPoints, FramesMeasured)

        array = np.array(data[0]).reshape(1,-1)

        prediction = model.predict(array)
        print(prediction)
        listOfPoints=[]
    if prediction[0] == "Nothing":
        prediction[0] = " "
    cv2.putText(frame,text=prediction[0], org = (300,200), fontFace=0, fontScale=6.0, color = (0,0,255), thickness= 4)
    cv2.imshow('Video', frame)

    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()