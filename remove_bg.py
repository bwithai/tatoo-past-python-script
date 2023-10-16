# Processing the image
from PIL import Image
from rembg import remove


def remove_background(img):
    input_img = Image.open(img)

    # Removing the background from the given Image
    output = remove(input_img)
    output.save("images/remove_bg_reference.png")
    return output

# remove_background("images/result.jpg")