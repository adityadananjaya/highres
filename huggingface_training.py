# import packages
import os
os.environ['PYTORCH_CUDA_ALLOC_CONF'] = 'expandable_segments:True'
from transformers import AutoFeatureExtractor, AutoModelForObjectDetection, TrainingArguments, Trainer, AutoImageProcessor
from datasets import Dataset, Features, ClassLabel, Sequence, Value, Image
import xml.etree.ElementTree as ET
from PIL import Image as PILImage
import albumentations as A
import numpy as np
from functools import partial
import torch
torch.cuda.empty_cache()
torch.cuda.memory_summary(device=None, abbreviated=False)
from transformers.image_transforms import center_to_corners_format
from dataclasses import dataclass
from torchmetrics.detection.mean_ap import MeanAveragePrecision
from pprint import pprint
import gc
gc.collect()

MODEL_NAME = "facebook/detr-resnet-50"
ID_TO_LABEL = { 0: "Boat"}
LABEL_TO_ID = { "Boat": 0 }

def LoadDataset(images_path, labels_path):
    """
    Loads dataset for training
    
    @Param
    dataset_path : String
        file pathway to dataset

    Returns None
    """

    """
    if "validation" not in cppe5:
        split = cppe5["train"].train_test_split(0.15, seed=1337)
        cppe5["train"] = split["train"]
        cppe5["validation"] = split["test"]
    """
    # Collect files and sort them alphabetically
    image_files = sorted([f for f in os.listdir(images_path) if f.endswith('.jpg') or f.endswith('.png')])
    annotation_files = sorted([f for f in os.listdir(labels_path) if f.endswith('.xml')])

    # Get labels in correct format
    labels_set = set()

    for ann_file in annotation_files:
        ann_path = os.path.join(labels_path, ann_file)
        tree = ET.parse(ann_path)
        root = tree.getroot()

        for obj in root.findall('object'):
            label = obj.find('name').text
            labels_set.add(label)

    # labels_list = sorted(list(labels_set))

    features = Features({
        'image_id': Value(dtype='string'),
        'image': Image(),  # Automatically handles image loading
        'width': Value(dtype='int32'),
        'height': Value(dtype='int32'),
        'objects': Sequence({
            'id': Value(dtype='int32'),
            'area': Value(dtype='float32'),
            'bbox': Sequence(Value('float32'), length=4),  # [xmin, ymin, xmax, ymax]
            'category': Value(dtype='int32'),
        })
    })

    data_entries = []
    image_id = 0

    for img_file, ann_file in zip(image_files, annotation_files):
        img_path = os.path.join(images_path, img_file)
        ann_path = os.path.join(labels_path, ann_file)

        # Parse XML annotation
        tree = ET.parse(ann_path)
        root = tree.getroot()

        objects = []
        annotation_id = 0

        for obj in root.findall('object'):

            label = obj.find('name').text
            bbox = obj.find('bndbox')
            xmin = float(bbox.find('xmin').text)
            ymin = float(bbox.find('ymin').text)
            xmax = float(bbox.find('xmax').text)
            ymax = float(bbox.find('ymax').text)
            objects.append({
                'id': annotation_id,
                'area': float((xmax - xmin) * (ymax - ymin)),
                'bbox': [xmin, ymin, xmax - xmin, ymax - ymin], # Convert to COCO format
                'category': 0
            })

            annotation_id += 1


        img = PILImage.open(img_path)
        width, height = img.size
        data_entries.append({
            'image_id': "0" + str(image_id) if len(str(image_id)) < 2 else str(image_id),
            'image': img_path,
            'width': width,
            'height': height,
            'objects': objects
        })

        image_id += 1
    
    dataset = Dataset.from_list(data_entries, features=features)

    return dataset

def format_images(image_id, categories, areas, bboxes):
    """Format one set of image annotations to the COCO format

    Args:
        image_id (str): image id. e.g. "0001"
        categories (List[int]): list of categories/class labels corresponding to provided bounding boxes
        areas (List[float]): list of corresponding areas to provided bounding boxes
        bboxes (List[Tuple[float]]): list of bounding boxes provided in COCO format
            ([center_x, center_y, width, height] in absolute coordinates)

    Returns:
        dict: {
            "image_id": image id,
            "annotations": list of formatted annotations
        }
    """
    annotations = []
    for category, area, bbox in zip(categories, areas, bboxes):
        formatted_annotation = {
            "image_id": image_id,
            "category_id": category,
            "iscrowd": 0,
            "area": area,
            "bbox": list(bbox),
        }
        annotations.append(formatted_annotation)

    return {
        "image_id": image_id,
        "annotations": annotations,
    }


# Define Augmentation Pipeline
TRAINING_AUGMENTATION = A.Compose([
    A.Perspective(p=0.1),
    A.HorizontalFlip(p=0.5),
    A.RandomBrightnessContrast(p=0.5),
    A.HueSaturationValue(p=0.1),
], bbox_params=A.BboxParams(format="coco", label_fields=["category"], clip=True, min_area=25),
)

VALIDATION_AUGMENTATION = A.Compose(
    [A.NoOp()],
    bbox_params=A.BboxParams(format="coco", label_fields=["category"], clip=True),
)

IMAGE_PROCESSOR = AutoImageProcessor.from_pretrained(
    MODEL_NAME,
    do_resize=True,
    size={"max_height": 6944, "max_width": 9248},
    do_pad=True,
    pad_size={"height": 6944, "width": 9248},
)

# Define Preprocessing Function
def preprocess_batch(sample, training:bool, return_pixel_mask=False):
    """
    Apply augmentations to sample and format annotations in COCO format for object detection
    """

    images = []
    annotations = []

    for image_id, image, objects in zip(sample["image_id"], sample["image"], sample["objects"]):
        image = np.array(image.convert("RGB"))

        # apply augmentations
        if training:
            output = TRAINING_AUGMENTATION(image=image, bboxes=objects["bbox"], category=objects["category"])
        else:
            output = VALIDATION_AUGMENTATION(image=image, bboxes=objects["bbox"], category=objects["category"])
        images.append(output["image"])

        # format annotations in COCO format
        formatted_annotations = format_images(
            image_id, output["category"], objects["area"], output["bboxes"]
        )
        annotations.append(formatted_annotations)

    # Apply the image processor transformations: resizing, rescaling, normalization
    result = IMAGE_PROCESSOR(images=images, annotations=annotations, return_tensors="pt")

    if not return_pixel_mask:
        result.pop("pixel_mask", None)

    return result
    
def collate_fn(sample):
    data = {}
    data["pixel_values"] = torch.stack([x["pixel_values"] for x in sample])
    data["labels"] = [x["labels"] for x in sample]
    if "pixel_mask" in sample[0]:
        data["pixel_mask"] = torch.stack([x["pixel_mask"] for x in sample])
    return data

def convert_bbox_yolo_to_pascal(boxes, image_size):
    """
    Convert bounding boxes from YOLO format (x_center, y_center, width, height) in range [0, 1]
    to Pascal VOC format (x_min, y_min, x_max, y_max) in absolute coordinates.

    Args:
        boxes (torch.Tensor): Bounding boxes in YOLO format
        image_size (Tuple[int, int]): Image size in format (height, width)

    Returns:
        torch.Tensor: Bounding boxes in Pascal VOC format (x_min, y_min, x_max, y_max)
    """
    # convert center to corners format
    boxes = center_to_corners_format(boxes)

    # convert to absolute coordinates
    height, width = image_size
    boxes = boxes * torch.tensor([[width, height, width, height]])

    return boxes

@dataclass
class ModelOutput:
    logits: torch.Tensor
    pred_boxes: torch.Tensor

@torch.no_grad()
def compute_metrics(evaluation_results, image_processor, threshold=0.0, id2label=None):
    """
    Compute mean average mAP, mAR and their variants for the object detection task.

    Args:
        evaluation_results (EvalPrediction): Predictions and targets from evaluation.
        threshold (float, optional): Threshold to filter predicted boxes by confidence. Defaults to 0.0.
        id2label (Optional[dict], optional): Mapping from class id to class name. Defaults to None.

    Returns:
        Mapping[str, float]: Metrics in a form of dictionary {<metric_name>: <metric_value>}
    """

    predictions, targets = evaluation_results.predictions, evaluation_results.label_ids

    # For metric computation we need to provide:
    #  - targets in a form of list of dictionaries with keys "boxes", "labels"
    #  - predictions in a form of list of dictionaries with keys "boxes", "scores", "labels"

    image_sizes = []
    post_processed_targets = []
    post_processed_predictions = []

    # Collect targets in the required format for metric computation
    for batch in targets:
        # collect image sizes, we will need them for predictions post processing
        batch_image_sizes = torch.tensor(np.array([x["orig_size"] for x in batch]))
        image_sizes.append(batch_image_sizes)
        # collect targets in the required format for metric computation
        # boxes were converted to YOLO format needed for model training
        # here we will convert them to Pascal VOC format (x_min, y_min, x_max, y_max)
        for image_target in batch:
            boxes = torch.tensor(image_target["boxes"])
            boxes = convert_bbox_yolo_to_pascal(boxes, image_target["orig_size"])
            labels = torch.tensor(image_target["class_labels"])
            post_processed_targets.append({"boxes": boxes, "labels": labels})

    # Collect predictions in the required format for metric computation,
    # model produce boxes in YOLO format, then image_processor convert them to Pascal VOC format
    for batch, target_sizes in zip(predictions, image_sizes):
        batch_logits, batch_boxes = batch[1], batch[2]
        output = ModelOutput(logits=torch.tensor(batch_logits), pred_boxes=torch.tensor(batch_boxes))
        post_processed_output = image_processor.post_process_object_detection(
            output, threshold=threshold, target_sizes=target_sizes
        )
        post_processed_predictions.extend(post_processed_output)

    # Compute metrics
    metric = MeanAveragePrecision(box_format="xyxy", class_metrics=True)
    metric.update(post_processed_predictions, post_processed_targets)
    metrics = metric.compute()

    # Replace list of per class metrics with separate metric for each class
    classes = metrics.pop("classes")
    map_per_class = metrics.pop("map_per_class")
    mar_100_per_class = metrics.pop("mar_100_per_class")
    for class_id, class_map, class_mar in zip(classes, map_per_class, mar_100_per_class):
        class_name = id2label[class_id.item()] if id2label is not None else class_id.item()
        metrics[f"map_{class_name}"] = class_map
        metrics[f"mar_100_{class_name}"] = class_mar

    metrics = {k: round(v.item(), 4) for k, v in metrics.items()}

    return metrics


eval_compute_metrics_fn = partial(
    compute_metrics, image_processor=IMAGE_PROCESSOR, id2label=ID_TO_LABEL, threshold=0.0
)

if __name__ == "__main__":
    try:
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        print(device)
        ds =  LoadDataset("./64mp-pascalvoc-labels-50/images", "./64mp-pascalvoc-labels-50/Annotations")

        split = ds.train_test_split(0.15, seed=1337)

        ds = {
            "train": split["train"],
            "test": split["test"],
            "validation": split["test"]
        }

        preprocess_training = partial(
            preprocess_batch, training=True
        )

        preprocess_validation = partial(
            preprocess_batch, training=False
        )

        ds["train"] = ds["train"].with_transform(preprocess_training)
        ds["validation"] = ds["validation"].with_transform(preprocess_validation)

        model = AutoModelForObjectDetection.from_pretrained(
            MODEL_NAME,
            id2label=ID_TO_LABEL,
            label2id=LABEL_TO_ID,
            ignore_mismatched_sizes=True,
        )
        model = model.to(device)

        training_args = TrainingArguments(
            output_dir="detr_finetuned_boat",
            num_train_epochs=2,
            fp16=True,
            per_device_train_batch_size=2,
            per_device_eval_batch_size=2,
            dataloader_num_workers=0,
            learning_rate=5e-5,
            lr_scheduler_type="cosine",
            weight_decay=1e-4,
            max_grad_norm=0.01,
            metric_for_best_model="eval_map",
            greater_is_better=True,
            load_best_model_at_end=True,
            eval_strategy="epoch",
            save_strategy="epoch",
            save_total_limit=2,
            remove_unused_columns=False,
            eval_do_concat_batches=False,
            push_to_hub=False,
        )

        trainer = Trainer(
            model=model,
            args=training_args,
            train_dataset=ds["train"],
            eval_dataset=ds["validation"],
            tokenizer=IMAGE_PROCESSOR,
            data_collator=collate_fn,
            compute_metrics=eval_compute_metrics_fn,
        )

        trainer.train()
        
        metrics = trainer.evaluate(eval_dataset=ds["test"], metric_key_prefix="test")
        pprint(metrics)

        trainer.save_model()
    except Exception as e:
        print(e)
    finally:
        # Clean up
        del model
        del trainer
        gc.collect()
        torch.cuda.empty_cache()