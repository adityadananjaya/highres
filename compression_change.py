from PIL import Image
import math
import os
import sys

# FUNCTIONS ------------------------------------------------------------------------

def get_file_size(file_path):
    """
    Returns file size in megabytes in 2 decimal points
    
    Parameters:
    file_path : string
        image file path
    """
    
    MB_size = 1000000
    file_size = float("{:.2f}".format(os.path.getsize(file_path) / MB_size))
    return file_size

def change_compression(file_path, percentage_quality, saved_path):
    """
    If file exists, reduces file compression down to percentage_quality and save image
    in the saved_path directory.

    Returns None.

    Parameters:
    file_path : string
        image file path
    percentage_quality : int
        value between 0 and 100
    saved_path : string
        file to save image to
    """

    try:
        file = Image.open(file_path)
    except FileNotFoundError:
        print(f"{file_path} does not exist")
        return

    image_name = file_path.split('/')[-1]

    file.save(saved_path + '/' + image_name, quality=percentage_quality)

    file.close()

    return

# MAIN -----------------------------------------------------------------------------------

def compression_change(folder_path, compressions):
    '''
    
    Generates specified compression versions of the given dataset

    Returns None

    Parameters:
    folder_path : string
        folder containing the images to be transformed
    compressions : int[]
        list of compressions to compress the dataset to. Each compression is stored in a different folder

    '''


    files = os.listdir(folder_path)

    compressions_passed = []

    # Make directories for each resolution
    for percentage in compressions:
        if percentage < 0 or percentage > 100:
            print("Invalid ({}%) percentage size".format(percentage))
        else:
            compressions_passed.append(percentage)
            os.mkdir(folder_path + "/" + str(percentage) + "percent")
        
    # Create MP version of each image
    print(compressions_passed)
    
    for image in files:
        for percentage in compressions_passed:
            change_compression(folder_path + "/" + image, percentage, folder_path + "/" + str(percentage) + "percent")
            

if __name__ == "__main__":
    # Get inputs from command line arguments and passes to resolution_change
    n_args = len(sys.argv)

    if n_args >= 3:
        folder_path = sys.argv[1]

        print(folder_path)

        compressions = []

        for i in range(2, n_args):
            compressions.append(int(sys.argv[i]))
        
        compression_change(folder_path, compressions)