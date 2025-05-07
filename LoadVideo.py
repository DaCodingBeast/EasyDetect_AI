import cv2
from PoseDatasets import Dataset
from PoseDetector import PoseMarker
from VideoWrapperClass import RotatingResizingVideoCapture
import cvDatasetLayout


FramesMeasured = 5

def getPointsFromFrame():
    ret,frame = video.read()
    frame_rgb, points = detector.process(frame)
    return frame_rgb, points


if __name__ == "__main__":
    video = RotatingResizingVideoCapture("aryaDancing.mp4")
    video.reset()
    
    detector = PoseMarker()
    dataset = Dataset(framesPerSample=FramesMeasured)
    cvTrainingLayout = cvDatasetLayout.Canvas(["Nothing","Y","M","C","A","b","e","z","z","z","z","z"])

    loopNum =0
    listOfPoints = []


    while True:
        
        loopNum +=1
        frame_rgb, points = getPointsFromFrame()
        while points is None:
            frame_rgb, points = getPointsFromFrame()

        listOfPoints.append(points)

        cvTrainingLayout.run()

        cv2.imshow("Video",frame_rgb)

        while loopNum % FramesMeasured ==0 and cvTrainingLayout.clicked == False:
            cv2.waitKey(1)


        #add to Dataset
        if loopNum % FramesMeasured ==0 and not listOfPoints.__contains__(None):
            dataset.addToDataset(listOfPoints, cvTrainingLayout.label)
            listOfPoints=[]
            cvTrainingLayout.clicked = False

        if cv2.waitKey(25) and 0xFF == ord('q'):
            break

    video.release()
    cv2.destroyAllWindows()