# todo: Overlay and resize it
# import cv2
# import numpy as np
#
# # Load the base image (the image you want to overlap onto)
# base_image = cv2.imread('human_back.jpg')
#
# # Load the image to be overlapped
# texture_image = cv2.imread('tattoo.jpg')
#
# # Get the dimensions of the base image
# height, width, _ = base_image.shape
#
# # Resize the texture image to match the size of the base image
# texture_image = cv2.resize(texture_image, (width, height))
#
# # Apply the texture to the base image using a blending technique (e.g., multiply)
# result_image = cv2.multiply(base_image, texture_image, scale=1.0/255)
#
# # Save the resulting image
# cv2.imwrite('result_image.jpg', result_image)


import cv2

from schemas import SelectedRegion


def place_tatoo(remove_bgr_img, tattoo, meta_data: SelectedRegion, dist_path):
    # Load the base image (the image you want to overlap onto)
    # base_image = cv2.imread('man_back2.jpg')
    base_image = cv2.imread(remove_bgr_img)

    # Load the image to be overlapped
    # tattoo_image = cv2.imread('tattoo3.jpg')
    tattoo_image = cv2.imread(tattoo)

    # Resize the tattoo image to a smaller size
    # tattoo_height, tattoo_width, _ = tattoo_image.shape
    # scale_factor = new_height / tattoo_height
    # new_width = int(tattoo_width * scale_factor)
    new_height = int(meta_data.height)
    new_width = int(meta_data.width)
    resized_tattoo = cv2.resize(tattoo_image, (new_width, new_height))

    # Get the dimensions of the base image
    base_height, base_width, _ = base_image.shape

    # Define the position to overlay the tattoo (e.g., upper left corner)
    x_position = int(meta_data.x)
    y_position = int(meta_data.y)

    # Create a mask for the tattoo (convert to grayscale)
    tattoo_gray = cv2.cvtColor(resized_tattoo, cv2.COLOR_BGR2GRAY)

    # Invert the mask to create a transparency mask
    _, tattoo_mask = cv2.threshold(tattoo_gray, 100, 255, cv2.THRESH_BINARY_INV)

    # Extract the region of interest (ROI) from the base image
    roi = base_image[y_position:y_position + new_height, x_position:x_position + new_width]

    # Blend the resized tattoo onto the ROI while preserving the background
    for c in range(0, 3):
        roi[:, :, c] = (
                resized_tattoo[:, :, c] * (tattoo_mask / 255.0) +
                roi[:, :, c] * (1.0 - tattoo_mask / 255.0)
        )

    # Save the resulting image
    cv2.imwrite(f'{dist_path}/place_tattoo.jpg', base_image)