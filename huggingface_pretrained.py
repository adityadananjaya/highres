import torch
import os
import csv
from PIL import Image, ImageDraw
from transformers import AutoImageProcessor, AutoModelForObjectDetection
from compression_change import compression_change


def huggingface_pretrained(models, directories, compressions):
    """
    HuggingFace model pipeline
    
    Returns None

    Parameters:
    models : string[]
        List of huggingface model repositories to be used for the pipeline -> "facebook/detr-resnet-50"
    directories : string[]
        List of dataset directory file paths -> "./dataset/16mp"
    compressions : string[]
        List of compressions we want to do on the datasets
    
    Uses the models to label images in the supplied directories. Creates a folder for each model in each
    directory containing the labelled images. Also creates a csv file in root folder containing the
    model and dataset pair performance statistics.

    """
    
    # Loop over compressions and create new compression datasets
    temp_directory = []
    for dataset in directories:
        temp_directory.append(dataset)
    for dataset in directories:
        compression_change(dataset, compressions)
        for percentage in compressions:
            temp_directory.append(dataset + "/" + str(percentage) + "percent")
        
    directories = temp_directory

    device = "cuda" # Use cuda to run on GPU

    # Create performance csv file
    with open('models_performance_unlabelled.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        field = ["model", "dataset", "average_detections", "average_confidence"]
        writer.writerow(field)

    model_repos = models

    for model_repo in model_repos: # Loop over models
        # Load the huggingface repo
        image_processor = AutoImageProcessor.from_pretrained(model_repo)
        model = AutoModelForObjectDetection.from_pretrained(model_repo)
        model = model.to(device)

        directories = directories

        for directory in directories: # Loop over each directory
            total_detections = 0
            total_confidence = 0

            # Create the folder for labelled images generated from model
            files = os.listdir(directory)
            new_dir = directory + "/" + "_".join(model_repo.split('/'))
            os.mkdir(new_dir)

            total_images = 0
            # Calculate the number of jpg files
            for file in files:
                if file.removesuffix(".jpg") != file:
                    total_images += 1

            for file in files: # Loop over each file in the directory
                if file.removesuffix(".jpg") == file: # Check if file is an image if not skip
                    continue
                
                image = Image.open(directory + "/" + file)

                with torch.no_grad(): # Disable gradient calculation
                    inputs = image_processor(images=[image], return_tensors="pt")
                    outputs = model(**inputs.to(device))
                    target_sizes = torch.tensor([[image.size[1], image.size[0]]])
                    results = image_processor.post_process_object_detection(outputs, threshold=0.3, target_sizes=target_sizes)[0]

                # Create the labels
                for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
                    box = [round(i, 2) for i in box.tolist()]
                    print(
                        f"Detected {model.config.id2label[label.item()]} with confidence "
                        f"{round(score.item(), 3)} at location {box}"
                    )

                    total_detections += 1
                    total_confidence += round(score.item(), 3)


                draw = ImageDraw.Draw(image)

                # Drawing the labels onto the image
                for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
                    box = [round(i, 2) for i in box.tolist()]
                    x, y, x2, y2 = tuple(box)
                    draw.rectangle((x, y, x2, y2), outline="red", width=1)
                    draw.text((x, y), model.config.id2label[label.item()], fill="white")

                image.save(new_dir + "/" + file)

            # Saving the performance statistics to csv
            with open('models_performance_unlabelled.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([model_repo, directory.split('/')[-1], f'{(total_detections/total_images):.2f}',f'{(total_confidence/total_detections):.2f}'])

if __name__ == "__main__":
    # huggingface_pretrained(["facebook/detr-resnet-50", "facebook/detr-resnet-101"], ["./dataset/64mp", "./dataset/16mp","./dataset/4mp"], [90, 80, 70])
    huggingface_pretrained(["facebook/detr-resnet-50"], ["./test_resolution_images"], [90, 80, 70])