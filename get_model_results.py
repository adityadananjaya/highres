from ultralytics import YOLO
from ultralytics.solutions import object_counter as oc
from os import listdir
from os.path import join, isdir
from PIL import Image, UnidentifiedImageError
from math import floor
import csv
import sys
import os
from pathlib import Path

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

def process_with_models_labeled(yaml_directory, resolution):
    models = return_yolo_models()
    yaml_file = yaml_directory
    csv_file = f'{resolution}mp-labeled-results.csv'
    csv_header = ['Model','Precision','Recall','mAP50', 'mAP50-95', 'Fitness'] 
    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(csv_header)

    for name,model in models.items():
        results = model.val(data=yaml_file, save_json=True, save_txt=True)
        print(results.curves_results)
    
        
        mAP50 = results.results_dict['metrics/mAP50(B)']
        precision = results.results_dict['metrics/precision(B)']
        recall = results.results_dict['metrics/recall(B)']
        fitness = results.results_dict['fitness']
        mAP50_95 = results.results_dict['metrics/mAP50-95(B)']
        # Write results to CSV
        with open(csv_file, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([name, mAP50, mAP50_95, recall, precision, fitness])

    print(f"Results saved to {csv_file}")
    
    
def main():
    
    folder = ""
    mode = None
    #select mode: either data is unlabeled, or labeled, 0 or 1 respectively
    while mode != 0 and mode != 1:
        mode = int(input("Are you working with labeled or unlabeled data? [0: Unlabeled, 1: Labeled]: "))
    

    

    # get paths of all images in folder
    
  
    all_models = return_yolo_models()
    if mode == 0:
        folder = input("Enter the path of the images: ")
        if not isdir(folder):
            print("Not a valid directory, exiting")
            exit()
        imgs = [join(folder, img) for img in listdir(folder)]
        data = process_with_models(imgs, all_models) 
        write_csv_files(data)  
    # writing results to CSV
    elif mode == 1:
        yaml_file = input("Enter the path of the YAML configuration: ")
        if not os.path.exists(yaml_file):
            print("YAML file not found in the directory provided, exiting")
            exit()
        resolution = int(input("Please enter resolution of the dataset: [4: 4 megapixel, 16: 16 megapixel, 64: 64 megapixel]: "))
        data = process_with_models_labeled(yaml_file, resolution)
    

if __name__ == "__main__":
    main()