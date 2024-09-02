from PIL import Image
import math
import os
import sys

# FUNCTIONS ------------------------------------------------------------------------
def calculate_megapixel(height, width):
    total = height * width

    mp = total / ( 10**6 )

    return mp

def get_size_from_megapixel(cur_height, cur_width, target_mp):
    # Get current megapixel
    if target_mp >= calculate_megapixel(cur_height, cur_width):
        return None
    
    new_height = cur_height
    new_width = cur_width

    # Uses the formula new_height * new_width = ( target_mp * 10**6 )
    # Same ratio hence new_width = new_height * ( cur_width / cur_height )
    # Reduces to new_height * new_height * ( cur_width / cur_height ) = ( target_mp * 10**6 )
    # new_height = sqrt( ( target_mp * 10**6 ) / ( cur_width / cur_height ) )

    new_height = math.sqrt( ( target_mp * (10**6) ) / ( cur_width / cur_height ) )

    new_width = new_height * ( cur_width / cur_height )

    return (round(new_height), round(new_width))

# MAIN -----------------------------------------------------------------------------------

def main():
    # expecting python resolution_change.py folder_path resolutions
    # at least 1 resolution
    # Get system arguments
    n_args = len(sys.argv)

    if n_args < 3:
        return
    
    folder_path = sys.argv[1]

    print(folder_path)

    resolutions = []

    for i in range(2, n_args):
        resolutions.append(int(sys.argv[i]))

    print(resolutions)

    files = os.listdir(folder_path)
    print(files)

    # Make directories for each MP

    for resolution in resolutions:
        os.mkdir(folder_path + "/" + str(resolution) + "MP_images")

    # Create MP version of each image
    for image in files:
        for resolution in resolutions:
            target = Image.open(folder_path + "/" + image)

            #print(target.size)

            #image_ratio = target.size[0]/target.size[1]

            #print(calculate_megapixel(target.size[0], target.size[1]))

            new_size = get_size_from_megapixel(target.size[0], target.size[1], resolution)

            # MP is larger than actual photo MP
            if new_size == None:
                continue

            target = target.resize(new_size, Image.LANCZOS)

            target.save(folder_path + "/" + str(resolution) + "MP_images/" + image, quality=95)

if __name__ == "__main__":
    main()