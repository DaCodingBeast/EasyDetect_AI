import cv2

#Need to have the box not be able to go off edge

class ImageCropper():
    done = False
    rectangle = None

    def __init__(self, firstFrame, aspectRatio = .8):
        
        self.aspectRatio = aspectRatio
        height, width = firstFrame.shape[:2]
        self.height = height
        self.width = width

        self.boxCenter =[width//2,height//2]
        self.boxsize = int(min(height,width))

        #First frame
        self.image =firstFrame

        cv2.imshow("Image", firstFrame)
  
        cv2.createTrackbar("BoxSize", "Image", self.boxsize, max(height,width), self.updateTrackbar)    
        cv2.setMouseCallback("Image", ImageCropper.mouse_callback, param=self)


    def inputImage(self,image):
        self.image = image

    def updateTrackbar(self,size):
        self.boxsize = size
    
    def mouse_callback(event, x, y, flags, param):
        self = param
        image = self.image

        self.boxCenter = [x, y]

        if event == cv2.EVENT_LBUTTONDOWN:
            ImageCropper.done = True
            cv2.destroyWindow("Image")

    
    def draw_box(self):
        image = self.image

        boxCenter = self.boxCenter

        BoxHeight = self.boxsize * self.aspectRatio
        BoxWidth = self.boxsize

        x1 = int(boxCenter[0] - BoxWidth//2)
        x2 = int(boxCenter[0] + BoxWidth//2)

        y1 = int(boxCenter[1] - BoxHeight//2)
        y2 = int(boxCenter[1] + BoxHeight//2)

        cv2.rectangle(image, (x1,y1), (x2,y2), (0, 0, 0), 7)

        ImageCropper.rectangle = [y1,y2,x1,x2]
        
        cv2.imshow("Image",image)

    