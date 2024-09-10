import os

def voc_data_calc(x_centre, y_centre, width, height):
    """
    Compute VOC label data from YOLO label data: (x_centre, y_centre, width, heigth)
    
    Return tuple: integer label boundary in the form (x_min, y_min, x_max, y_max)
    
    Params:
    x_centre: int
    y_centre: int
    width: int
    height: int

    """

    return (x_centre - width, y_centre - height, x_centre + width, y_centre + height)

def yolotxt_to_voc(folder_path):
    """
    Converts YOLO data to VOC data format

    Returns String[][] : array of string arrays

    Params:
    folder_path : String
        directory containing all the label txt data

    """

    # Open directory containing labels
    dir = os.listdir(folder_path)
    data_arr = []

    for label_file in dir: # Loop over each label

        voc_data_arr = []
        with open(folder_path + '/' + label_file, "r") as f:
            for line in f.readlines():
                # Read YOLO label data
                yolo_data = line.split(" ")
                try: # Attempt to parse data as floats
                    x_centre = float(yolo_data[1])
                    y_centre = float(yolo_data[2])
                    width = float(yolo_data[3])
                    height = float(yolo_data[4])
                except(IndexError): # Corrupted or incorrect format YOLO file
                    print("Missing values")
                    print(yolo_data)

                # Compute and add VOC data tuple to list
                voc_data = voc_data_calc(x_centre, y_centre, width, height)
                voc_data_arr.append(str(voc_data))

        # Add VOC string array to return list
        data_arr.append(voc_data_arr)

    return data_arr
            