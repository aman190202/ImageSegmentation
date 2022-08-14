# Segmenetation on Videos

End Goal is to create an efficient model that can provide object segementation in videos without frame rate depreciation.

## Image Segmentation

Image segmentation is the process of partitioning a digital image into multiple image segments, also known as image regions or image objects (sets of pixels). The goal of segmentation is to simplify and/or change the representation of an image into something that is more meaningful and easier to analyze. Image segmentation is typically used to locate objects and boundaries (lines, curves, etc.) in images. More precisely, image segmentation is the process of assigning a label to every pixel in an image such that pixels with the same label share certain characteristics.

## Overview of the Current Model

Pixel 6 optimized segmentation models based on MobilenetEdgeTPUV2 backbone and DeepLab v3+ decoder and head is presented over here. To improve the quality of on-device segmentation models, architecture search to jointly search for the model's feature extractor and the segmentation head is invoked. Autoseg-EdgeTPU is a set of searched segmentation models customized for the Edge TPU in Pixel 6. The feature extractor is derived from Edge TPU search space where a mixture of IBN and fused IBN are used. The segmentation head is an optimized version of Bi-FPN head, with customized number of repeats and feature selection.

For this model, Argmax fusion is applied to improve segmentation model latency. The last two levels of the model (bilinear resizing and Argmax) contribute significantly to latency on the device model. This is due to the large activation size between these layers (512 x 512 x Number of classes). These layers can be merged without significantly impacting quality scores by making Argmax smaller and scaling the classes to the desired size with nearest neighbor.

### Test Case 1 : Indoors
<img src="assets/1-test.gif" width=400 height=400>  <img src="assets/1-seg.gif" width=400 height=400>
### Test Case 2 : Outdoors
<img src="assets/2-test.gif" width=400 height=400>  <img src="assets/2-seg.gif" width=400 height=400>

More examples will be added to analyse the best use case for this model.

## Requirements
1. NumPy
2. MatplotLib
3. TensorFlow
4. TensorFlow Hub
5. OpenCV2


## How to run
```
$ git clone https://github.com/aman190202/ImageSegmentation.git
$ pip install -r requirements.txt
$ python main.py
```
When prompted, Enter the video file to be segmented.

## Working
The [main.py](main.py) employs the three major functions to make the conversion possible

### Video Fragmentation
The program employs the use of OpenCV2 to fragment the desired video into a number of frames and stores them in /tmp.

### Frame Segementation
Frame segmentation employs the use of the tensorflow model with predefined weights stored in the [weights directory](/weights/1). This functions linearly iterates throught the tmp directory and applies segmentation on each image.

### Frame Concatenation
Frame Concatenation concatenates the whole directory linearly at 30 Fps to mimic the nature of the test video. The end result will be stored by the name of 'segmented.MP4'

**Delete the /tmp directory manually to make use of the program again**
## Runtime
The lightweght nature of the current model allows for faster segmentation and takes upto a minute to segment 10 second videos on a Macbook Air M1.



