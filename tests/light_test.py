import sys 


import unittest
from os import listdir
from os.path import isfile, join
import re
import cv2
from frame_analyzer import light

class LightTest(unittest.TestCase):
    def test_is_on(self):
        images_path = './tests/light-images'
        images_files = [f for f in listdir(images_path) if isfile(join(images_path, f))]
        for image in images_files:
            if image == ".":
                continue
            is_on = re.findall("[0-9]*_(on|off)\.png",image)[0] == "on"

            bright_area_threshold = 50
            if image == "8_on.png":
                bright_area_threshold = 40
                
            self.assertTrue(light.is_on(cv2.imread(images_path+"/"+image), bright_area_threshold) == is_on, "Image "+image)