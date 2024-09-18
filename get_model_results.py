from ultralytics import YOLO
from ultralytics.solutions import object_counter as oc
from os import listdir
from os.path import join, isdir
from PIL import Image, UnidentifiedImageError
from math import floor
import csv
import sys


def return_yolo_models():
    modelx = YOLO("yolov8x.pt")
    modell = YOLO("yolov8l.pt")
    modelm = YOLO("yolov8m.pt")
    models = YOLO("yolov8s.pt")
    modeln = YOLO("yolov8n.pt")

    all_models = {"extra_large": modelx, "large": modell, "medium": modelm, "small":models, "nano":modeln}
    return all_models

def write_csv_files(data):
    with open('results.csv', 'w+', newline='') as csvfile:
        fieldnames = ['model', 'image', 'resolution', 'detections', 'average confidence']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

def process_with_models(imgs, all_models):
    data = []
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
            # for loop to predict detections
            print(xres, yres)
            pred = model.predict(img, imgsz=[yres, xres])
            
            det = len(pred[0].boxes)
            conf = pred[0].boxes.conf.mean().item()
            
            row = {'model': name, 'image': img, 'resolution': resolution, 'detections': det, 'average confidence': conf}
            data.append(row)
    return data

def process_with_models_labeled():
    print("To be implemented")


def main():
    # get directory
    folder = ""
    if(len(sys.argv) != 2 or not isdir(sys.argv[1])):
        print("Please.")
        sys.exit()
    mode = None
    while mode != 0 and mode != 1:
        mode = int(input("Are you working with labeled or unlabeled data? [0: Unlabeled, 1: Labeled]: "))


    folder = sys.argv[1]

    # get paths of all images in folder
    imgs = [join(folder, img) for img in listdir(folder)]
  
    all_models = return_yolo_models()
    if mode == 0:
        data = process_with_models(imgs, all_models) 
        write_csv_files(data)  
    # writing results to CSV
    elif mode == 1:
        data = process_with_models_labeled()
    

if __name__ == "__main__":
    main()