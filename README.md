### Note: This repository is a duplicate of the one stored in my university's Github account. It has been reproduced here, with permission from the client. This is a collaborative project involving four group members, whose names have been redacted from this README for privacy.

# High-Res vs Low-Res Images for Long-Range AI Detection of Vehicles

This repository is dedicated to exploring the impact of image resolution on the performance of AI models in detecting construction vehicles over long distances. The project involves using a 128 Megapixel camera system and comparing the results across different resolutions.

## Running the YOLO image validation scripts


- The main program for YOLOv8 model comparisons is the **get_model_results.py**
- To use this program, there are 3 modes: 
  - 0 [unlabeled data], 
  - 1 [labeled data], 
  - 2 [labeled data with SAHI preprocessing]
- Usage instructions:  
    - First install the required packages via the requirements.txt
    ```
    pip install -r requirements.txt
    ```
- Then move to the get_model_results directory:
    ```
    cd get_model_results
    ```

### Mode 0: Unlabeled Data
Process images from a directory and save detection results to a CSV file.
```
python get_model_results.py 0 /path/to/images
```
- Input: Path to the directory containing images.
- Output: results.csv with columns for model name, image path, resolution, number of detections, and average confidence.

### Mode 1: Labeled data
Evaluate models on labeled data using a YAML configuration file and save results to CSV and JSON files.
```
python get_model_results.py 1 /path/to/data.yaml resolution_value
```

- Input:  
    - Path to the YAML file.  
    - Resolution value (e.g., 4, 16, 64).
- Output:
    - resolution_value-mp-labeled-results.csv with metrics like Precision, Recall, mAP50, etc.
    - resolution_value-mp-labeled-results.json containing raw graph data.

### Mode 2: SAHI (Sliced Annotation Handling Interface)
Preprocess images and annotations using slicing, convert them to YOLO format, and evaluate models.

```
python get_model_results.py 2 /path/to/images /path/to/annotations.json resolution_value
```
- Input:  
    - Path to the image directory.
    - Path to the JSON annotation file.
    - Resolution value.
- Output: 
  - Similar outputs as Mode 1 with preprocessed data.

### Location of outputs:
The outputs are always stored in the home directory of the user.

### Example
To process unlabeled images located in /images directory:
```
python get_model_results.py 0 /images
```
To evaluate on labeled data with a YAML configuration at /data.yaml for resolution 16mp:
```
python get_model_results.py 1 /data.yaml 16
```


## Running the Data Dashboard Web App

- Make sure you have Dash, Pandas, and Dash Bootstrap Components installed in your laptop. This can be done using pip in the terminal:
```
pip install dash
pip install pandas
pip install dash-bootstrap-components
```
- Clone the repository
- In your terminal, navigate to the directory of the repository, then the dashboard. For example:
```
cd p01e-high-res
cd dashboard

```

- Within that directory, run app.py, e.g:
```
python3 app.py

```
- If the app runs succesfully, you will be given a localhost link, e.g **http://127.0.0.1:XXXX/**. 
- Copy that link and paste it into the web browser. This should run the app.
- Once you are done, open the terminal back and press CTRL + C. This should terminate the app. 

## Image Compression Script Usage
```
python3 compression_change.py <directory-of-images> <percentage compressions of original required>
```
Example usage:

```
python3 compression_change.py path/to/images 70 80 90
```
The command above takes all the images in path/to/images directory, and compresses them to 70%, 80%, 90% of original, creating 3 separate folders in the directory, named 70, 80, 90 containing their corresponding images.
## YOLO Model-X trained on 64 megapixel images augmented by SAHI slicing:
### [Google Drive Link](https://drive.google.com/drive/folders/15YDI9WOJUP_usr13RWkmId3H91eQxRfH?usp=sharing)

