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
import json
from slicing import slice
from json_to_yolo import *
import shutil

def return_yolo_models():
    modelx = YOLO("yolov8x.pt")
    modell = YOLO("yolov8l.pt")
    modelm = YOLO("yolov8m.pt")
    models = YOLO("yolov8s.pt")
    modeln = YOLO("yolov8n.pt")

    all_models = {"extra_large": modelx, "large": modell, "medium": modelm, "small":models, "nano":modeln}
    return all_models

def write_csv_files(data, fieldnames):
    with open('results.csv', 'w+', newline='') as csvfile:
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

def get_imgsz(resolution):
    if(resolution == 4):
        return 2312
    elif(resolution == 16):
        return 4624
    elif(resolution == 64):
        return 9248


def preprocess(image_dir, json_dir, resolution):
    # SLICE
    dirname = os.path.dirname(__file__)
    output_dir = os.path.join(dirname, f"{resolution}mp-sahi/valid/images")
    slice(image_dir, json_dir, output_dir)

    # COCO2YOLO
    sahi_json_dir = os.path.join(output_dir, "sliced_annotations.json_coco.json")
    yolo_dir = os.path.join(dirname, f"{resolution}mp-sahi/valid/labels")
    convert_coco_json_to_yolo(sahi_json_dir, yolo_dir)

    # copy data.yaml
    src = os.path.join(dirname, "data/data.yaml")
    copied_yaml = os.path.join(dirname, f"{resolution}mp-sahi/data.yaml")
    shutil.copyfile(src, copied_yaml)

    os.remove(sahi_json_dir)

    # return directory
    return copied_yaml

def process_with_models_labeled(yaml_directory, resolution):
    models = return_yolo_models()
    yaml_file = yaml_directory
    csv_file = f'{resolution}mp-labeled-results.csv'
    json_file = f'{resolution}mp-labeled-results.json'
    csv_header = ['Model','Precision','Recall','mAP50', 'mAP50-95', 'Fitness', 'preprocess', 'inference', 'loss', 'postprocess'] 
    with open(os.path.join(os.path.expanduser('~'), csv_file), 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(csv_header)
    
    data=[]
    
    for name,model in models.items():
        results = model.val(data=yaml_file, save_json=True, save_txt=True)
        
        mAP50 = results.results_dict['metrics/mAP50(B)']
        precision = results.results_dict['metrics/precision(B)']
        recall = results.results_dict['metrics/recall(B)']
        fitness = results.results_dict['fitness']
        mAP50_95 = results.results_dict['metrics/mAP50-95(B)']

        preprocess = results.speed['preprocess']
        inference = results.speed['inference']
        loss = results.speed['loss']
        postprocess = results.speed['postprocess']

        # Write quantitative results to CSV
        with open(os.path.join(os.path.expanduser('~'), csv_file), 'a', newline='') as file:
            writer = csv.writer(file)
            print(f"writing to {csv_file}")
            writer.writerow([name, mAP50, mAP50_95, recall, precision, fitness, preprocess, inference, loss, postprocess])

        # Write graph results to CSV
        for i in range(4):
            curve = results.curves[i]
            x_label = results.curves_results[i][2]
            x_vals = results.curves_results[i][0].tolist()
            y_label = results.curves_results[i][3]
            y_vals = results.curves_results[i][1].tolist()
            dict_ = {'model': name, 'resolution': resolution, 'curve': curve, x_label:x_vals, y_label:y_vals}
            data.append(dict_)

    with open(os.path.join(os.path.expanduser('~'), json_file), 'a') as f:
        json.dump(data, f)

    print(f"Results saved to {csv_file}")
    print(f"Raw graph data saved to {json_file}")
    
def main():
    
    folder = ""
    mode = None
    #select mode: either data is unlabeled, or labeled, 0 or 1 respectively
    mode = int(sys.argv[1])
    
    # get paths of all images in folder
    all_models = return_yolo_models()
    if mode == 0:
        folder = input("Enter the path of the images: ")
        if not isdir(folder):
            print("Not a valid directory, exiting")
            exit()
        imgs = [join(folder, img) for img in listdir(folder)]
        data = process_with_models(imgs, all_models) 
        fieldnames = ['model', 'image', 'resolution', 'detections', 'average confidence']
        write_csv_files(data, fieldnames)  
    # writing results to CSV
    elif mode == 1:
        dir_input = sys.argv[2]
        dirname = os.path.dirname(__file__)
        yaml_file = os.path.join(dirname, dir_input)
        if not os.path.exists(yaml_file):
            print("YAML file not found in the directory provided, exiting")
            exit()
        resolution = int(sys.argv[3])
        data = process_with_models_labeled(yaml_file, resolution)
    elif mode == 2:
        # SAHI mode
        dirname = os.path.dirname(__file__)
        dir_input = os.path.join(dirname, sys.argv[2])
        json_input = os.path.join(dirname, sys.argv[3])
        if not os.path.exists(dir_input):
            print("Image directory not found!")
        elif not os.path.exists(json_input):
            print("JSON annoation file not found!")
        resolution = sys.argv[4]
        yaml_file = preprocess(dir_input, json_input, resolution)
        process_with_models_labeled(yaml_file, resolution)
    
if __name__ == "__main__":
    main()