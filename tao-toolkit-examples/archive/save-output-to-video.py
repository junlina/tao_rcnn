import cv2
import numpy as np
import glob

img_array = []

files = glob.glob('workspace/models/unet/outputs/vis_overlay_tlt/*.png')
files.sort()

for filename in files:
    img = cv2.imread(filename)
    h, w, c = img.shape
    size = (w, h)
    img_array.append(img)

out = cv2.VideoWriter('results.mp4', cv2.VideoWriter_fourcc(*'MP4V'), 30, size)

for i in range(len(img_array)):
    out.write(img_array[i])

out.release()

