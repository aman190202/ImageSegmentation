import io
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
import tensorflow_hub as hub
import cv2
import os
from PIL import Image as PILImage
 
IMAGE_WIDTH = 512
IMAGE_HEIGHT = 512
keras_layer = hub.KerasLayer('weights/1')
model = tf.keras.Sequential([keras_layer])
model.build([None, IMAGE_WIDTH, IMAGE_HEIGHT, 3])

location= input("Enter the location of the file (must be in MP4) : ") 
save_as= 'segmented.mp4' 

def vid_to_frames(location):
    cam = cv2.VideoCapture(location) 
    try:
        if not os.path.exists('tmp'):
            os.makedirs('tmp')
    except OSError:
        print ('Error: Creating directory of data')

    currentframe = 0
    while(True):
        ret,frame = cam.read()
        if ret:
            name = 'tmp/'+ str(currentframe) + '.jpg'
            cv2.imwrite(name, frame)
            currentframe += 1
        else:
            break
    cam.release()
    cv2.destroyAllWindows()

def frame_segmentation():
    directory = 'tmp'
    for filename in sorted(os.listdir(directory)):
        f = os.path.join(directory, filename)
        # checking if it is a file
        if os.path.isfile(f):
            image = PILImage.open(f).convert('RGB')
            min_dim = min(image.size[0], image.size[1])
            image = image.resize((IMAGE_WIDTH * image.size[0] // min_dim, IMAGE_HEIGHT * image.size[1] // min_dim))
            input_data = np.expand_dims(image, axis=0)
            input_data = input_data[:, :IMAGE_WIDTH,:IMAGE_HEIGHT, :]
            input_data = input_data.astype(np.float) / 128 - 0.5
            output_data = model(input_data)
            assert(output_data.numpy().shape == (1, 512, 512))
            arr=np.squeeze(output_data)
            plt.imshow(arr)
            plt.axis('off')
            plt.savefig(f)
            plt.close()

def frame_to_vid():

    img_array = []
    dir_len=len([name for name in os.listdir('tmp') if os.path.isfile(os.path.join('tmp', name))])
    for i in range(0,dir_len):
        img = cv2.imread('tmp/'+str(i)+'.jpg')
        height, width, layers = img.shape
        size = (width,height)
        img_array.append(img)
    out = cv2.VideoWriter(save_as,cv2.VideoWriter_fourcc(*'MP4V'), 30, size )
    for i in range(len(img_array)):
        out.write(img_array[i])
    out.release()

print('<<<Undergoing Video Fragmentation>>> ')
vid_to_frames(location)
print('<<<Undergoing Frame Segmentation>>>')
frame_segmentation()
print('<<<Undergoing Frame Concatenation>>>')
frame_to_vid()
