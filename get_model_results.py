from ultralytics import YOLO
from ultralytics.solutions import object_counter as oc
from os import listdir
from os.path import join, isdir
from PIL import Image, UnidentifiedImageError
from math import floor
import csv
import sys

# get directory
folder = ""
if(len(sys.argv) != 2 or not isdir(sys.argv[1])):
    print("Please.")
    sys.exit()

folder = sys.argv[1]

# get paths of all images in folder
imgs = [join(folder, img) for img in listdir(folder)]

# model -- feel free to add more
modelx = YOLO("yolov8x.pt")
modell = YOLO("yolov8l.pt")
modelm = YOLO("yolov8m.pt")
models = YOLO("yolov8s.pt")
modeln = YOLO("yolov8n.pt")

all_models = {"extra_large": modelx, "large": modell, "medium": modelm, "small":models, "nano":modeln}

data = []

# for loop to predict detections
for img in imgs:
    # get resolution of image
    try: 
        with Image.open(img) as image: 
            xres, yres = image.size
    except UnidentifiedImageError:
        print(img + " not an  image")
        continue
    
    resolution = floor((xres * yres)/1000000)
    
    for name, model in all_models.items():
        print(xres, yres)
        pred = model.predict(img, imgsz=[yres, xres])
        
        det = len(pred[0].boxes)
        conf = pred[0].boxes.conf.mean().item()
        
        row = {'model': name, 'image': img, 'resolution': resolution, 'detections': det, 'average confidence': conf}
        data.append(row)
    
# writing results to CSV
with open('results.csv', 'w+', newline='') as csvfile:
    fieldnames = ['model', 'image', 'resolution', 'detections', 'average confidence']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(data)