from pycocotools.cocoeval import COCOeval
from pycocotools.coco import COCO
import csv
import json

def import_predicted(file_name):
    data = {
        'facebook/detr-resnet-50': {
            "images": [],
            "90percent": [],
            "80percent": [],
            "70percent": [],
            "60percent": [],
            "50percent": [],
            "40percent": [],
            "30percent": [],
            "20percent": [],
            "10percent": []
        },
        'facebook/detr-resnet-101': {
            "images": [],
            "90percent": [],
            "80percent": [],
            "70percent": [],
            "60percent": [],
            "50percent": [],
            "40percent": [],
            "30percent": [],
            "20percent": [],
            "10percent": []
        }
    }

    with open(file_name, mode ='r') as file:
        csvFile = csv.reader(file)
        
        # Skip the first two lines
        next(csvFile)
        next(csvFile)



        for lines in csvFile:
            data[lines[0]][lines[1]].append({
                "image_id": lines[2],
                "category_id": 0,
                "bbox": [float(lines[3]), float(lines[4]), float(lines[5]), float(lines[6])],
                "score": float(lines[7])
            })

    return data

def update_image_id(predicted, label_file):
    with open(label_file, 'r') as file:
        data = json.load(file)

    for image in data["images"]:
        image_name = image["file_name"].removesuffix(".jpg").removeprefix("images/")

        print(image_name)

        image_id = image["id"]

        # find the image in our predicted and change to image_id

        for obj in predicted:
            if obj["image_id"] == image_name:
                obj["image_id"]  = int(image_id)
            
    return predicted

def huggingface_evaluation():
    # import predicted labels and actual labels
    print("hello")

if __name__ == "__main__":
    predictedCOCO = import_predicted("models_coco_labels.csv")["facebook/detr-resnet-50"]["10percent"]

    predictedCOCO = update_image_id(predictedCOCO, "./64mp-coco-labels/result.json")

	# load detection JSON file from the disk
    cocoAnnotation = COCO(annotation_file="./64mp-coco-labels/result.json")
    
    # save predictions as a json then load in
    result_json = []

    annotation_id = 0

    for annotation in predictedCOCO:
        result_json.append(annotation)

        annotation_id += 1
	
    # Serializing json
    json_object = json.dumps(result_json, indent=4)
    
    # Writing to sample.json
    with open("result.json", "w") as outfile:
        outfile.write(json_object)
    

	# load detection JSON file from the disk
    cocovalPrediction = cocoAnnotation.loadRes("result.json")
	# initialize the COCOeval object by passing the coco object with
	# ground truth annotations, coco object with detection results
    cocoEval = COCOeval(cocoAnnotation, cocovalPrediction, "bbox")
	
	# run evaluation for each image, accumulates per image results
	# display the summary metrics of the evaluation
    cocoEval.evaluate()
    cocoEval.accumulate()
    cocoEval.summarize()