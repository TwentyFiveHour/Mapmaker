__author__ = 'Aaron Kaufman'
import tkinter
from tkinter import PhotoImage
from PIL import Image, ImageTk


class City(object):

    def __init__(self):
        self.image = 'images/b_rook.png'

    def get_pic_string(self):
        return self.image

    def get_image(self, x_size, y_size):
        image = Image.open("images/b_rook.png")
        image = image.resize((x_size, y_size), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(image)
        return photo