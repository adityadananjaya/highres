import os
import json
from sahi.utils.coco import Coco, CocoCategory, CocoImage, CocoAnnotation
from sahi.slicing import slice_coco
from ultralytics import YOLO

def slice(parent_folder, json_file, output_folder):
    parent_folder = parent_folder
    image_folder = parent_folder
    json_file = json_file
    output_folder = output_folder

    slice_coco(
    coco_annotation_file_path=json_file,
    image_dir=image_folder,
    output_coco_annotation_file_name="sliced_annotations.json",
    output_dir=output_folder,
    slice_height=640,
    slice_width=640,
    overlap_height_ratio=0.2,
    overlap_width_ratio=0.2
    ) 