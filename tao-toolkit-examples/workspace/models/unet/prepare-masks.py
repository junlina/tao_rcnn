import os
import numpy as np
import cv2

image_dir = 'workspace/data/multiclass/images'
mask_dir = 'workspace/data/multiclass/masks'
npy_dir = 'workspace/data/multiclass/npy_masks'


image_subdirs = os.listdir(image_dir)

for sd in image_subdirs:
    mask_dir_path = os.path.join(mask_dir, sd)
    if not os.path.exists(mask_dir_path):
        os.makedirs(mask_dir_path)

    # for every image file generate a mask
    for f in os.listdir(os.path.join(image_dir, sd)):
        outfile = os.path.join(mask_dir, sd, f)
        npy_mask = os.path.join(npy_dir, f.replace('.png', '.npy'))

        npy_mask_obj = np.load(npy_mask)
        cv2.imwrite(outfile, npy_mask_obj)