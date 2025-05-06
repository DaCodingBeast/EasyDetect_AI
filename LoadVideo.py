import cv2
from PoseDatasets import Dataset
from PoseDetector import PoseMarker
from VideoWrapperClass import RotatingResizingVideoCapture
import cvDatasetLayout
from cropImage import ImageCropper


FramesMeasured = 10


if __name__ == "__main__":
    video = RotatingResizingVideoCapture("aryaDancing.mp4")
    video.reset()
    
    detector = PoseMarker()
    dataset = Dataset(framesPerSample=FramesMeasured)
    cvTrainingLayout = cvDatasetLayout.Canvas(["Nothing","Hello","Excited","PointLeft","PointRight","Powerful","e","g","h","i","j","k"])

    loopNum =0
    listOfPoints = []


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

        cvTrainingLayout.run()

        cv2.imshow("Video",frame)

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