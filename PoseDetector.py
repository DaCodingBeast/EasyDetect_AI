import mediapipe as mp
import cv2

class PoseMarker():
    def __init__(self):
        self.pose = mp.solutions.pose
        self.drawing = mp.solutions.drawing_utils
        self.detector = self.pose.Pose(
            static_image_mode=False,  
            model_complexity=1,       
            smooth_landmarks=True,    
            min_detection_confidence=0.5,  
            min_tracking_confidence=0.5    
        )
    def process(self, numpyImage):
        frame_rgb = cv2.cvtColor(numpyImage, cv2.COLOR_BGR2RGB)
        results = self.detector.process(frame_rgb)

        if results.pose_landmarks:
            self.drawing.draw_landmarks(frame_rgb, results.pose_landmarks, self.pose.POSE_CONNECTIONS)
            filteredPoints = PoseMarker.filterLandmarkData(results.pose_landmarks.landmark)
        else:
            filteredPoints = None

        return frame_rgb, filteredPoints
    
    
    def filterLandmarkData(landmarks):
        landmarkList3d =[]
        for landmark_id, landmark in enumerate(landmarks):
            if(landmark_id < 24):
                landmarkList3d.append(landmark.x)
                landmarkList3d.append(landmark.y)
                landmarkList3d.append(landmark.z)
        return landmarkList3d
