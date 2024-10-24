import os
from ultralytics import YOLO
import torch
def train_yolo_model_x(image_directory, yaml_directory, epochs_no):

# Load the YOLOv8x model
    model = YOLO(directory)
    # Train the model
    results = model.train(
        resume = True,
        data='/home/ubuntu/yolo-custom-dataset/data.yaml',
        epochs=epochs_no, 
        project='yolov8x_custom', 
        device=0               
    )
    print(results)


if __name__ == "__main__":
    directory = input("Please enter the directory of the model: ")
    data = input("Please enter the directory of the yaml configuration file of the data: ")
    epochs_no=int(input("Please enter the number of epochs you want to train the model for: "))
    train_yolo_model_x(directory, data, epochs_no)