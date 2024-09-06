# High-Res vs Low-Res Images for Long-Range AI Detection of Vehicles

This repository is dedicated to exploring the impact of image resolution on the performance of AI models in detecting construction vehicles over long distances. The project involves using a 128 Megapixel camera system and comparing the results across different resolutions.

## Team members:

| Student Name                          | Unikey   | Student ID  |
|---------------------------------------|----------|-------------|
| Shabab Saleheen                       | ssal6113 | 520226274   |
| Tolga Sirkeci                        | tsir8879 | 510434883   |
| Putu Gede Aditya Dananjaya          | pdan5295 | 520095245   |
| Broden Suffern                       | bsuf3055 | 510448938   |

### Tutor: Conor Chen, jche4519@uni.sydney.edu.au

### User stories: [Bitbucket Link](https://bitbucket.org/comp3888_m10_3_/capstone_project/src/main/docs/user-stories/user-stories.md)

### Meeting Minutes: [Bitbucket Link](https://bitbucket.org/comp3888_m10_3_/capstone_project/src/main/docs/minutes/meeting_minutes.md)

## Running the program evaluation script [more features to follow]

- The main program for YOLOv8 model comparisons is the **get_model_results.py**
- This file takes a single command line argument, which is the directory of the images
- The program validates the validity of the directory before starting output
- After processing all the images, the product terminates and stores a **results.csv** in the base directory which contains all the essential machine learning data

### Saving object detection output images

- If the user wants, the output images can be automatically saved in a **runs** folder by modifying the parameter for **model.predict()** within the program by providing an argument **save = True**

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

### More entries and updates to follow as project progresses