import cv2
import numpy as np

def is_on(image:cv2.Mat,bright_area_threshold:int=50, bright_threshold:int=100) -> bool:
   """Given an image of a light source, checks whether it's on or off

   Args:
       image (cv2.Mat): Opencv image matrix
       bright_area_threshold (int, optional): Percentage of bright pixels from total pixels of the matrix for light source to be considered on. Defaults to 50.
       bright_threshold(int, optional): Threshold for a pixel to be considered bright, taking into account Value from HSV color space. Defaults to 100

   Returns:
       bool: If light source is on, returns True, otherwhise, False
   """
   hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
   mask = cv2.inRange(hsv_image, np.array([0,0,0]),np.array([255,255,bright_threshold]))
   black_pixels = np.sum(mask == 0)
   black_percentage = 0
   if black_pixels > 0:
      black_percentage = (black_pixels / mask.size) * 100
   return black_percentage >= bright_area_threshold

def is_blinking(buffer, fps, interval_limit_seconds, bright_area_threshold=50):
   current_frame = buffer.copy().popleft()
   current_interval_seconds = 0
   frame_counter = 0
   light_changes = 0
   for frame in buffer:
      if is_on(frame, bright_area_threshold) == is_on(current_frame, bright_area_threshold):
         frame_counter = frame_counter + 1
         continue
      current_frame = frame
      current_interval_seconds = 0 if frame_counter == 0 else frame_counter / fps
      if current_interval_seconds >= interval_limit_seconds:
         continue
      light_changes = light_changes + 1
      frame_counter = 0
      if light_changes >= 2:
         return True
   return False