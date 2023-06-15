import dearpygui.dearpygui as dpg
import tkinter as tk
from tkinter import filedialog
import cv2
import os
import numpy as np

input_file = ""
output_file = ""

val1 = 255*0.3
val2 = 255*0.8

def get_sequential_255_indices(arr):
    indices = np.where(arr == 255)[0]

    diff = np.diff(indices)
    split_indices = np.where(diff > 1)[0]

    sequential_indices = np.split(indices, split_indices + 1)

    return sequential_indices

def open_file_dialog_input():
    root = tk.Tk()
    root.withdraw()
    file_types = [
        ("Image files", "*.bmp;*.dib;*.jpeg;*.jpg;*.jpe;*.jp2;*.png;*.webp;*.pbm;*.pgm;*.ppm;*.pxm;*.pnm;*.sr;*.ras;*.tiff;*.tif;*.exr;*.hdr;*.pic"),
        ("All files", "*.*")
    ]
    
    file_path = filedialog.askopenfilename(filetypes=file_types)
    global input_file
    input_file = file_path
    filename, ext = os.path.splitext(file_path)
    global output_file
    output_file = filename + "_sorted.png"
    dpg.set_value("input_file_name", "Selected input file: " + file_path)

sort_channel = 0

mask_channel = 0

def sort_channel_changed(channel):
    match channel:
        case "Luminance":
            sort_channel = 0
        case "Hue":
            sort_channel = 1
        case "Saturation":
            sort_channel = 2
        case "Red":
            sort_channel = 3
        case "Green":
            sort_channel = 4
        case "Blue":
            sort_channel = 5

def mask_channel_changed(channel):
    match channel:
        case "Luminance (recomended)":
            mask_channel = 0
        case "Hue":
            mask_channel = 1
        case "Saturation":
            mask_channel = 2
        case "Red":
            mask_channel = 3
        case "Green":
            mask_channel = 4
        case "Blue":
            mask_channel = 5

def sort_pixels():
    image = cv2.imread(input_file)

    im = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)[..., 2]

    im_sort_channel = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)[..., 0]

    mask = cv2.inRange(im, val1, val2)

    for i in range(len(im)):
        ones = get_sequential_255_indices(mask[i])
        for j in range(len(ones)):
            if len(ones[j]) == 0:
                continue
            sorted_indices = np.argsort(im_sort_channel[i][ones[j][0]:ones[j][-1] + 1])
            image[i][ones[j][0]:ones[j][-1] + 1] = image[i][ones[j][0]:ones[j][-1] + 1][sorted_indices]

    cv2.imwrite(output_file, image)

def set_val1(x):
    val1 = x * 255

def set_val2(x):
    val2 = x * 255

dpg.create_context()

with dpg.window(tag="Primary Window", label="Pixel sort", width=800, height=400):
    dpg.add_button(label="Select Image", callback=open_file_dialog_input)
    dpg.add_text("Selected input file: ", tag="input_file_name")

    dpg.add_text("Select Mask Channel: ")
    dpg.add_combo(items=["Luminance (recomended)", "Hue", "Saturation", "Red", "Green", "Blue"], default_value="Luminance (recomended)", callback=mask_channel_changed)

    dpg.add_text("Select Sort Channel: ")
    dpg.add_combo(items=["Luminance", "Hue", "Saturation", "Red", "Green", "Blue"], default_value="Luminance", callback=sort_channel_changed)

    slider_float1 = dpg.add_slider_float(
        label="Threshold 1",
        default_value=0.3,
        max_value=1.,
        min_value=0.,
        callback=set_val1
    )

    slider_float2 = dpg.add_slider_float(
        label="Threshold 1",
        default_value=0.8,
        max_value=1.,
        min_value=0.,
        callback=set_val2
    )

    dpg.add_button(label="Sort Pixels", callback=sort_pixels)


dpg.create_viewport(title='Custom Title', width=800, height=400)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Primary Window", True)
dpg.start_dearpygui()
dpg.destroy_context()