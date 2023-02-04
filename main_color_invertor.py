import os
import errno
import argparse

from work_color_invertor import ColorInvertor
from colors import COLORS

ap = argparse.ArgumentParser()
ap.add_argument("-t", "--work_type", required=True, type=str, help="Check if it is image or videostream work")
ap.add_argument("-i", "--input_image", required=False, type=str, help="Path to input image")
ap.add_argument("-c", "--color", required=True, type=str, help="Name of color")

args = vars(ap.parse_args())

def start_work():
    type = args["work_type"]
    filename = args["input_image"]
    color_name = args["color"]

    if type not in ["image", "video"]:
        print("Incorrect type of work. Choose 'image' or 'video' key")

    if type == "image" and not os.path.exists(filename):
        print("Can't find image file. Check it path or if it exists")
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), filename)

    if COLORS[color_name] is None:
        print(f"Color name {color_name} is incorrect")
        raise Exception("Current name is incorrect")

    # upload image
    c_inv = ColorInvertor()

    if type == "image":
        c_inv.recolor_hair_image(filename, color_name)
    if type == "video":
        c_inv.recolor_hair_video(color_name)
    

if __name__ == "__main__":
    start_work()