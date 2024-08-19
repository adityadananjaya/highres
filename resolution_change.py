from PIL import Image

# Functions


def calculate_megapixel(height, width):
    total = height * width

    mp = total / ( 10**6 )

    return mp

def get_size_from_megapixel(cur_height, cur_width, target_mp):
    # Get current megapixel
    if calculate_megapixel(cur_height, cur_width) >= target_mp:
        return None
    
    new_height = cur_height
    new_width = cur_width

    return (new_height, new_width)


if __name__ == "__main__":
    target = Image.open("./test_image.PNG")

    print(target.size)

    image_ratio = target.size[0]/target.size[1]

    # Target 75% ratio

    print(calculate_megapixel(target.size[0], target.size[1]))

    new_size = ( round(target.size[0] * 0.75), round(target.size[1] * 0.75) )

    target = target.resize(new_size, Image.LANCZOS)

    print(calculate_megapixel(target.size[0], target.size[1]))

    target.save("./test_image_scaled.PNG", quality=95)