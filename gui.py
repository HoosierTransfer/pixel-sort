import dearpygui.dearpygui as dpg
import tkinter as tk
from tkinter import filedialog

input_file = ""
output_file = ""


def open_file_dialog_input():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    print("Selected file:", file_path)
    global input_file
    input_file = file_path

def open_file_dialog_output():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    print("Selected file:", file_path)
    global output_file
    output_file = file_path
    

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

def input_file_callback(file):
    print(file)

def sort_pixels():
    pass

dpg.create_context()

with dpg.file_dialog(directory_selector=False, show=False, callback=input_file_callback, id="input_file", width=700 ,height=400):
    dpg.add_file_extension("Images (*.bmp *.jpeg *.jpg *.jpe *.jp2 *.png *.webp *.pbm *.pgm *.ppm *.pxm *.pnm *.sr *.ras *.tiff *.tif){.bmp,.jpeg,.jpg,.jpe,.jp2,.png,.webp,.pbm,.pgm,.ppm,.pxm,.pnm,.sr,.ras,.tiff,.tif}", color=(0, 255, 255, 255))


with dpg.window(tag="Primary Window", label="Pixel sort", width=800, height=400):
    dpg.add_button(label="Select File", callback=open_file_dialog)
    dpg.add_text("File Path: ")

    dpg.add_text("Select Mask Channel: ")
    dpg.add_combo(items=["Luminance (recomended)", "Hue", "Saturation", "Red", "Green", "Blue"], default_value="Luminance (recomended)", callback=mask_channel_changed)

    dpg.add_text("Select Sort Channel: ")
    dpg.add_combo(items=["Luminance", "Hue", "Saturation", "Red", "Green", "Blue"], default_value="Luminance", callback=sort_channel_changed)

    dpg.add_button(label="Sort Pixels", callback=sort_pixels)


dpg.create_viewport(title='Custom Title', width=800, height=400)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Primary Window", True)
dpg.start_dearpygui()
dpg.destroy_context()