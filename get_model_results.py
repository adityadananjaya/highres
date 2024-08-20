from ultralytics import YOLO
from ultralytics.solutions import object_counter as oc
from os import listdir
from os.path import join, isdir
from PIL import Image
from math import floor
import csv
import sys

# get directory
if(len(sys.argv) != 2 or not isdir(sys.argv[1])):
    print("Please write a valid directory as the command line argument.")
    sys.exit()

# get paths of all images in folder
folder = "pics"
imgs = [join(folder, img) for img in listdir(folder)]

# model -- feel free to add more
model = YOLO("yolov8x.pt")

data = []

# for loop to predict detections
for img in imgs:
    # get resolution of image
    with Image.open(img) as image: 
        xres, yres = image.size
    
    resolution = floor((xres * yres)/1000000)
    
    # predict 
    # TODO : we can add more models here to compare results for different models
    pred = model.predict(img)
    
    det = len(pred[0].boxes)
    conf = pred[0].boxes.conf.mean().item()
    
    row = {'image': img, 'resolution': resolution, 'detections': det, 'average confidence': conf}
    data.append(row)
    
# writing results to CSV
with open('results.csv', 'w+', newline='') as csvfile:
    fieldnames = ['image', 'resolution', 'detections', 'average confidence']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(data)