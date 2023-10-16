import base64
import os
import tempfile
import zipfile
from pathlib import Path
from typing import List, Tuple

from fastapi import FastAPI, UploadFile, HTTPException, File, Form, Request
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse

from remove_bg import remove_background
from schemas import SelectedRegion
from skin_canvas import canvas_img
from texture import place_tatoo
from utils import save_img, handle_base_img, manage_memory

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

dist_path = os.path.join(os.getcwd(), 'images')


@app.post("/api/v1/skin-canvas")
# async def load_and_store_pdf_files(base_image: UploadFile, region: SelectedRegion, tattoo_image: UploadFile):
async def load_and_store_pdf_files(base_image: UploadFile, tattoo_images: List[UploadFile] = File(...),
                                   widths: List[int] = Form(...),
                                   heights: List[int] = Form(...),
                                   xs: List[int] = Form(...),
                                   ys: List[int] = Form(...)):
    """
        Upload multiple tattoos with corresponding placement details.

        - **base_image**: The actual image to place tattoo on
        - **tattoo_images**: Upload multiple tattoo image files here.
        - **widths**: Provide a list of width values for each tattoo.
        - **heights**: Provide a list of height values for each tattoo.
        - **xs**: Provide a list of x-coordinate values for each tattoo.
        - **ys**: Provide a list of y-coordinate values for each tattoo.
    """

    manage_memory(dist_path)

    if len(tattoo_images) != len(widths) != len(heights) != len(xs) != len(ys):
        return {"message": "Mismatch in the number of images and placement details."}

    if not base_image:  # or not region or not tattoo_image:
        return {
            "status": 400,
            "result": "please upload baseimage"
        }

    # base_image will be save in images directory
    save_img(base_image, dist_path)

    # remove the saved img (base_image) from images directory and save as remove_bg_reference image
    result = handle_base_img(dist_path, base_image)
    if result != "done":
        return {
            "message": f"remove_background func give: {str(result)}"
        }

    remove_bgr_img_path = f"images/remove_bg_reference.png"

    # Process the uploaded images and placement details here
    for i in range(len(tattoo_images)):
        tattoo_image = tattoo_images[i]
        width = widths[i]
        height = heights[i]
        x = xs[i]
        y = ys[i]

        region = SelectedRegion(width=width, height=height, x=x, y=y)

        # tattoo_image will be save in images directory
        save_img(tattoo_image, dist_path)
        name, ext = tattoo_image.filename.split('.')
        tatoo_img_path = f"images/{name}.{ext}"

        try:
            place_tatoo(remove_bgr_img_path, tatoo_img_path, region,
                        dist_path)  # save place_tattoo.jpg in images directory
        except Exception as e:
            return {
                "message": f"place_tatoo func give: {str(e)}"
            }

        overlay_tatoo_img_path = f"images/place_tattoo.jpg"

        try:
            canvas_img(remove_bgr_img_path, overlay_tatoo_img_path, dist_path)  # save result.jpg in images
        except Exception as e:
            return {
                "message": f"canvas_img func give: {str(e)}"
            }

        os.remove(tatoo_img_path)
        remove_bgr_img_path = "images/result.jpg"

    os.remove("images/remove_bg_reference.png")
    try:
        with open("images/result.jpg", "rb") as image_file:
            # Read the image file as binary data
            image_binary = image_file.read()

            # Encode the binary data as Base64
            base64_data = base64.b64encode(image_binary).decode("utf-8")

            return base64_data
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None
