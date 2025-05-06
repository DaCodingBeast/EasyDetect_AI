import cv2
import tkinter as tk
from cropImage import ImageCropper

class RotatingResizingVideoCapture:
    def __init__(self, path, rotate_code=None):
        self.cap = cv2.VideoCapture(path)
        self.rotate_code = rotate_code
        self.screen_width, self.screen_height = self._get_screen_size()
        
        ret, frame = self.read()
        self.cropper = ImageCropper(frame)
        
        while not ImageCropper.done:
            ret,frame = self.read()
            self.cropper.inputImage(frame)
            self.cropper.draw_box()
            cv2.waitKey(1)  
        self.reset()

    def _get_screen_size(self):
        root = tk.Tk()
        root.withdraw()
        width = root.winfo_screenwidth()
        height = root.winfo_screenheight()
        root.destroy()
        return width, height

    def _resize_to_screen(self, frame):
        h, w = frame.shape[:2]
        scale = min(self.screen_width / w, self.screen_height / h)  # Only shrink
        return cv2.resize(frame, (int(w * scale), int(h * scale)))

    def read(self):
        ret, frame = self.cap.read()
        if not ret:
            return ret, None

        if self.rotate_code is not None:
            frame = cv2.rotate(frame, self.rotate_code)
        
        #resize to normal

        frame = self._resize_to_screen(frame)
        if ImageCropper.done:
            rect = self.cropper.rectangle
            frame = frame[rect[0]:rect[1], rect[2]:rect[3]]
        
        #resize for cropper
        frame = self._resize_to_screen(frame)
        
        return ret, frame
    def readFrame(self, frame):

        if self.rotate_code is not None:
            frame = cv2.rotate(frame, self.rotate_code)

        frame = self._resize_to_screen(frame)
        if ImageCropper.done:
            rect = self.cropper.rectangle
            frame = frame[rect[0]:rect[1], rect[2]:rect[3]]
        
        #resize for cropper
        frame = self._resize_to_screen(frame)
        
        return frame

    def isOpened(self):
        return self.cap.isOpened()

    def release(self):
        self.cap.release()

    def get(self, prop_id):
        return self.cap.get(prop_id)
    
    def reset(self):
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
