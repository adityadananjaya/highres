from ultralytics import YOLO
from ultralytics.solutions import object_counter as oc
from os import listdir
from os.path import join, isdir
from PIL import Image, UnidentifiedImageError
from math import floor
import csv
import sys
import os

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
    model = YOLO("yolov8x.pt")
    yaml_file = "C:\\Users\\shaba\\Desktop\\capstone_project\\capstone_project\\4mp-dataset-labeled\\data.yaml"
    csv_file = 'results.csv'
    csv_header = ['Image', 'Precision', 'Recall', 'mAP50', 'mAP50-95']
    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(csv_header)
    

    results = model.val(data=yaml_file, save_json=True, save_txt=True, imgsz = 1736)
    # for i, image_path in enumerate(results.files):
    #     image_name = os.path.basename(image_path)
    #     precision = results.results_dict['precision'][i]
    #     recall = results.results_dict['recall'][i]
    #     map50 = results.results_dict['metrics/mAP50(B)'][i]
    #     map50_95 = results.results_dict['metrics/mAP50-95(B)'][i]
    print(results.maps)
    exit()
    #     # Write results to CSV
    #     with open(csv_file, 'a', newline='') as file:
    #         writer = csv.writer(file)
    #         writer.writerow([image_name, precision, recall, map50, map50_95])

    # print(f"Results saved to {csv_file}")
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