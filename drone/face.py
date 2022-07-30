from mtcnn import MTCNN

import cv2
img = cv2.cvtColor(cv2.imread("test.jpg"), cv2.COLOR_BGR2RGB)
detector = MTCNN()
print(detector.detect_faces(img)[0]["box"])