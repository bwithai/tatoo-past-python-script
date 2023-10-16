In order to run this locally follow the step

```bash
git clone https://github.com/SofttikTech/tatoo-paste-python-script.git
python -m venv my_venv
source my_venv/bin/activate
pip install -r requirements.txt
ucivorn main:app
```

## How to use this API
Now go to your workspace in postman to create a new http request
- open header section add `key` Content-Type and `value` multipart/form-data
- open body section and select `form-data` add `key` base_image type `file` and `value` select_your_base_image_file
- same for `tattoo_images`

### _width and height:_

width and height are the dimensions of the tattoo image (tattoo_image).
They represent the width and height of the tattoo image in pixels.

### _x_position and y_position:_
x_position and y_position represent the pixel coordinates on the base image (base_image) where the tattoo will be overlaid.

_**x_position**_ represents the horizontal (x-axis) position in pixels.

_**y_position**_ represents the vertical (y-axis) position in pixels.