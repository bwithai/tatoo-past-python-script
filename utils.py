import os
import shutil

from remove_bg import remove_background


def save_img(base_image, dist_path):
    # move file to images directory
    with open(f"{base_image.filename}", "wb") as buffer:
        shutil.copyfileobj(base_image.file, buffer)

    new_file_src = f"{base_image.filename}"
    store_new_file_at_dist = f"{dist_path}"
    shutil.move(new_file_src, store_new_file_at_dist)


def handle_base_img(dist_path, base_image):
    file_name, file_extension = base_image.filename.split('.')
    file_path = os.path.abspath(f"images/{file_name}.{file_extension}")

    try:
        output = remove_background(file_path)
        save_file = os.path.abspath(f"images/remove_bg_reference.png")
        if os.path.exists(save_file):
            os.remove(save_file)
        output.save(f"{dist_path}/remove_bg_reference.png")
    except Exception as e:
        return e
    finally:
        # Delete the temporary file
        os.remove(file_path)
        return "done"


def manage_memory(dist_path):
    # Check if the directory exists
    if os.path.exists(dist_path):
        # If it exists, remove all files in the directory
        for filename in os.listdir(dist_path):
            file_path = os.path.join(dist_path, filename)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(f"Error deleting {file_path}: {e}")
    else:
        # If the directory doesn't exist, create it
        os.makedirs(dist_path)