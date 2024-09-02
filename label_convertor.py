import os

def voc_data_calc(x_centre, y_centre, width, height):
    # Return x_min, y_min, x_max, y_max
    return (x_centre - width, y_centre - height, x_centre + width, y_centre + height)

def yolotxt_to_voc(folder_path):
    dir = os.listdir(folder_path)
    data_arr = []

    for label_file in dir:

        voc_data_arr = []
        with open(folder_path + '/' + label_file, "r") as f:
            for line in f.readlines():
                # print(line)
                yolo_data = line.split(" ")
                try:
                    x_centre = float(yolo_data[1])
                    y_centre = float(yolo_data[2])
                    width = float(yolo_data[3])
                    height = float(yolo_data[4])
                except(IndexError):
                    print("Missing values")
                    print(yolo_data)

                voc_data = voc_data_calc(x_centre, y_centre, width, height)
                voc_data_arr.append(str(voc_data))

        data_arr.append(voc_data_arr)

    return data_arr
            