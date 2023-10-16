import cv2


def canvas_img(remove_bgr_img, overlay_tattoo_img, dist_path):
    # Load the base image (with a transparent background)
    # base_image = cv2.imread('c.png', cv2.IMREAD_UNCHANGED)
    base_image = cv2.imread(remove_bgr_img, cv2.IMREAD_UNCHANGED)

    # Make a copy of the base image to work with
    outlined_image = base_image.copy()

    # Convert the image to grayscale
    gray_image = cv2.cvtColor(base_image, cv2.COLOR_BGR2GRAY)

    # Find contours in the grayscale image
    contours, _ = cv2.findContours(gray_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Draw the contours on the outlined image
    cv2.drawContours(outlined_image, contours, -1, (0, 0, 255), 2)  # Outline in red, with a thickness of 2

    # Save the outlined image
    # cv2.imwrite(f'{dist_path}/outlined_image.png', outlined_image)

    # Load the "result_image.jpg"
    # result_image = cv2.imread('preview_image.jpg')
    result_image = cv2.imread(overlay_tattoo_img)

    # Create a mask of the outlined region
    mask = cv2.cvtColor(outlined_image, cv2.COLOR_BGR2GRAY)

    # Use the mask to crop the "result_image.jpg"
    result_cropped = cv2.bitwise_and(result_image, result_image, mask=mask)

    # Save or display the cropped result
    cv2.imwrite(f'{dist_path}/result.jpg', result_cropped)
