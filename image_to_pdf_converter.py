from tkinter import *
from tkinter import ttk
from tkinter import filedialog

from PIL import Image

from pathlib import Path
import sys


class WelcomeFrame(ttk.Frame):

    def __init__(self, root):
        self.file_locations = []
        self.new_file_name = ""
        self.row = 0
        self.dir = Path()

        self.frame = ttk.Frame(root)
        self.frame.grid(padx=10, pady=10, sticky="NSEW")

        welcome = ttk.Label(
            self.frame, text="Welcome to Image to PDF Converter!")
        welcome.grid(row=self.row, sticky="EW")
        self.row += 1

        FileFrame(self.frame, self.row, self.file_locations)
        self.row += 1

        ttk.Label(self.frame, text="What file name should it be saved as?").grid(
            row=self.row, column=0, sticky="W")
        self.new_file_name_entry = ttk.Entry(self.frame)
        self.new_file_name_entry.grid(
            row=self.row, column=1, padx=5, pady=5, sticky="W")
        self.row += 1

        ttk.Button(self.frame, text="Save At",
                   command=self.ask_directory).grid(row=self.row, column=1, padx=5, pady=5, sticky="W")
        self.save_at_row = self.row
        self.row += 2

        button = ttk.Button(self.frame, text="Convert!", command=self.convert)
        button.grid(row=self.row, pady=5, sticky="NEWS")
        root.bind("<Return>", lambda e: self.convert())
        self.row += 1

    def convert(self):
        if (len(self.file_locations) > 0):
            if convert_image_to_pdf(
                    self.file_locations, self.dir, self.new_file_name_entry.get()):
                ttk.Label(self.frame, text="Converted!").grid(
                    row=self.row, pady=5, sticky="NEWS")
            else:
                ttk.Label(self.frame, text="Unsuccessful").grid(
                    row=self.row, pady=5, sticky="NEWS")
        self.row += 1

    def ask_directory(self):
        self.dir = Path(filedialog.askdirectory())
        ttk.Label(self.frame, text=self.dir).grid(
            row=self.save_at_row+1, column=1, sticky="NEWS")


class FileFrame(ttk.Frame):
    def __init__(self, root, row, file_locations):
        self.file_locations = file_locations
        self.row = 0
        self.file_name_col = 1
        self.remove_button_col = 2

        self.frame = ttk.Frame(root)
        self.frame.grid(row=row, columnspan=2, pady=5, sticky="W")

        ttk.Label(self.frame, text="Select files to convert:").grid(
            row=self.row, column=0, pady=5, sticky="W")
        ttk.Button(self.frame, text="Select Files",
                   command=self.input_file_names_frame).grid(row=self.row, column=1, padx=5, pady=5, sticky="W")
        self.row += 1

    def input_file_names_frame(self):
        prev_len = len(self.file_locations)
        input_list = filedialog.askopenfilenames()
        self.file_locations.extend(input_list)

        for i in range(prev_len, len(self.file_locations)):
            self.display_file_location(self.file_locations[i])
            self.display_remove_button(i)
            self.row += 1

    def remove_file(self, index):
        slaves = self.frame.grid_slaves(row=index + 1)
        for slave in slaves:
            slave.destroy()

        self.file_locations.pop(index)

        for i in range(index, len(self.file_locations)):
            slaves = self.frame.grid_slaves(row=i + 2)
            slaves[0].configure(command=lambda i=i: self.remove_file(i))
            print(i)
            slaves[0].grid(row=i + 1)
            slaves[1].grid(row=i + 1)

        self.row -= 1

    def display_file_location(self, file_location):
        my_file = ttk.Label(
            self.frame, text=file_location)
        my_file.grid(row=self.row, column=self.file_name_col,
                     pady=5, sticky="W")

    def display_remove_button(self, index):
        remove_button = ttk.Button(
            self.frame, text="Remove", command=lambda: self.remove_file(index))
        remove_button.grid(
            row=self.row, column=self.remove_button_col, padx=5, sticky="W")


def input_file_names():
    list_of_files = []
    while True:
        try:
            num = int(input("Enter the number of images to convert into a pdf: "))
            break
        except ValueError:
            print("Did not input an integer.")

    for x in range(num):
        list_of_files.append(
            input("Enter the file location of file number {}: ".format(x + 1)))

    return list_of_files


def save_as_pdf(images: list, dir=Path(), new_file_name="image_to_pdf", dpi=300):
    print(str(dir))
    if len(images) == 0:
        print("No images to convert.")
        return False
    elif len(images) == 1:
        images[0].save(dir, "PDF")
    else:
        images[0].save(dir, "PDF",
                       resolution=dpi, save_all=True, append_images=images[1:])
    return True


def convert_image_to_pdf(file_locations: list, dir=Path(), new_file_name="image_to_pdf", dpi=300):
    images = []
    if new_file_name == "":
        new_file_name = "image_to_pdf"
    try:
        for i in range(0, len(file_locations)):
            images.append(Image.open(file_locations[i]))

        if not dir.exists():
            print("Directory does not exist.")
            return False

        dir = dir / (new_file_name + ".pdf")

        default_width = 2550

        for i in range(0, len(images)):
            if images[i].mode != "RGB":
                images[i] = images[i].convert("RGB")
            size = images[i].size
            if (size[0] > size[1]):
                images[i] = images[i].transpose(method=Image.ROTATE_270)
                size = images[i].size
            images[i] = images[i].resize(
                (default_width, int(size[1] * (default_width / size[0]))))

        save_as_pdf(images, dir, new_file_name, dpi)

    except FileNotFoundError:
        print("File Not Found.")
        return False

    for i in range(len(images)):
        images[i].close()

    return True


root = Tk()
root.geometry("500x500")
root.title("Image to PDF Converter")

welcome_frame = WelcomeFrame(root)

root.mainloop()


""" file_locations = input_file_names()
file_locations = gui_input_file_names()
new_file_name = input(
    "Enter the file name it should be saved as (without the extension): ")
if new_file_name == "":
    convert_image_to_pdf(file_locations)
else:
    convert_image_to_pdf(file_locations, new_file_name)
 """
