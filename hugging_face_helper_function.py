from PIL import Image, ImageDraw, ImageFont
def helper(object_detector, image_path, dest):
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()

    results = object_detector(image)

    for result in results:
        print(f"Detected {result['label']} with confidence {result['score']:.2f} at {result['box']}")

    for result in results:
        box = result['box']
        label = result['label']
        score = result['score']
        
        draw.rectangle([(box['xmin'], box['ymin']), (box['xmax'], box['ymax'])], outline="red", width=3)
        
        # Prepare the label and score text
        text = f"{label}: {score:.2f}"
        
        # Calculate text size and location
        text_width = draw.textlength(text, font=font)
        text_height = font.getbbox(text)[1]  # Use getsize to get the height of the text
        text_location = (box['xmin'], box['ymin'] - text_height)
        
        # Draw a filled rectangle for the text background
        draw.rectangle([text_location, (text_location[0] + text_width, text_location[1] + text_height)], fill="red")
        
        # Draw the label and score
        draw.text(text_location, text, fill="white", font=font)

        
        

    # Save the image with bounding boxes
    output_path = dest
    image.save(output_path)

    print(f"Image saved with bounding boxes at {output_path}")