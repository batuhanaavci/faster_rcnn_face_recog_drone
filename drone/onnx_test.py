import numpy as np    # we're going to use numpy to process input and output data
import onnxruntime    # to inference ONNX models, we use the ONNX Runtime
import onnx
from onnx import numpy_helper
import urllib.request
import json
import time
from numpy import asarray
import cv2
# display images in notebook
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont

session = onnxruntime.InferenceSession('yolov2_res18_aug.onnx', None)

# img = cv2.imread("test.jpg")
# print(np.shape(img))

im = Image.open('test.jpg')

newsize = (224, 224)
im = im.resize(newsize)

print(type(im))
print(np.shape(im))

print(type(im))

image = asarray(im,dtype='float32')

# image = np.zeros((1,3,1,1),dtype='float32')
image = np.expand_dims(image, axis=0)
# print(image)
print(type(image))
print(np.shape(image))
new_img = image
imm = np.reshape(image,(1,3,224,224))
# new_img[0][0] = image[0][2]
# new_img[0][0] = image[0][2]
# new_img[0][0] = image[0][2]
print(np.shape(imm))

# print(new_img[0][0])
# get the name of the first input of the model
input_name = session.get_inputs()[0].name  
output_name = session.get_outputs()[0].name

print('Input Name:', input_name)
print('Output Name:', output_name)

outputs = session.run([], {input_name: imm})
outputs = np.array(outputs)
# prediction=int(np.argmax(np.array(outputs).squeeze(), axis=0))

print(np.shape(outputs))
print(outputs[:,:,:,3,:])

