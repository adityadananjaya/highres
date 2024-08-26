def voc_data_calc(x_centre, y_centre, width, height):
    # Return x_min, y_min, x_max, y_max
    return (x_centre - width, y_centre - height, x_centre + width, y_centre + height)

def yaml_to_voc(label_file):
    with open(label_file, "r") as f:
        for line in f.readlines():
            yaml_data = line.split(" ")

            try:
                object_label = int(yaml_data[0])
                x_centre = float(yaml_data[1])
                y_centre = float(yaml_data[2])
                width = float(yaml_data[3])
                height = float(yaml_data[4])
            except(IndexError):
                print("Missing values")
                print(yaml_data)

            voc_data = voc_data_calc(x_centre, y_centre, width, height)
            print(voc_data)