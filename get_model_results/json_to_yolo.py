import os
import json

# Function to convert COCO bbox to YOLO bbox
def convert_bbox_coco_to_yolo(image_width, image_height, bbox):
    # COCO bbox format: [x_min, y_min, width, height]
    x_min, y_min, width, height = bbox

    # Calculate x_center, y_center, normalize values by image size
    x_center = x_min + width / 2.0
    y_center = y_min + height / 2.0

    # Normalize by image width and height
    x_center /= image_width
    y_center /= image_height
    width /= image_width
    height /= image_height

    return [x_center, y_center, width, height]

def convert_coco_json_to_yolo(coco_json_path, output_dir):
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Load COCO JSON
    with open(coco_json_path, 'r') as f:
        coco_data = json.load(f)

    images = {img['id']: img for img in coco_data['images']}
    categories = {cat['id']: cat['name'] for cat in coco_data['categories']}

    # Create a mapping from category name to YOLO class id
    category_to_class_id = {cat_id: idx for idx, cat_id in enumerate(categories.keys())}

    for ann in coco_data['annotations']:
        image_id = ann['image_id']
        category_id = ann['category_id']
        bbox = ann['bbox']

        # Get image details
        image_info = images[image_id]
        image_width = image_info['width']
        image_height = image_info['height']

        # Convert bbox to YOLO format
        yolo_bbox = convert_bbox_coco_to_yolo(image_width, image_height, bbox)

        # Get the YOLO class id
        class_id = 8

        # Prepare YOLO annotation line
        yolo_annotation = f"{class_id} " + " ".join([f"{coord:.6f}" for coord in yolo_bbox]) + "\n"

        # Write YOLO annotation to a txt file (one per image)
        txt_filename = os.path.join(output_dir, f"{os.path.splitext(image_info['file_name'])[0]}.txt")
        with open(txt_filename, 'a') as f:
            f.write(yolo_annotation)

    print(f"YOLO annotations saved to {output_dir}")

if __name__ == "main":
    # Example usage
    coco_json_path = '16mp-coco/sahi-training-64/sliced_annotations.json_coco.json'
    output_dir = '16mp-coco/yolo-labels'

    convert_coco_json_to_yolo(coco_json_path, output_dir)