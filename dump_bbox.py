# -*- coding: utf-8 -*-
"""
Created on Sat Jan 23 19:37:14 2021

@author: odusi
"""
import glob
import os
from natsort import natsorted
import cv2
import yaml


def extract_roi(filename):
    im = cv2.imread(filename)
    
    # Select ROI
    r = cv2.selectROI(im)
    #print (r)
    data_dump[0]["bbox"].append(r)



if __name__ == "__main__":
    file_path = "C:\\Users\\odusi\\Documents\\Projects\\ape_project\\flir_humans\\"
    data_dump = [{"bbox":[]}]
    
    #process imgs by extracting bounding boxes
    for root, _, fnames in natsorted(os.walk(file_path)):
        for fname in natsorted(fnames):  
            path = os.path.join(root, fname)
            extract_roi(path)
    
    #save data to yaml file
    with open(r'store_file.yaml', 'w') as file:
        yaml.dump(data_dump, file)
