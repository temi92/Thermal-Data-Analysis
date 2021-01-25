# -*- coding: utf-8 -*-
"""
Created on Sat Jan 23 11:41:36 2021

@author: odusi
"""

import cv2
import numpy as np
import tifffile as tf
import glob
import flir_image_extractor
import yaml
import os
from natsort import natsorted
from PIL import Image
import matplotlib.pyplot as plt



IMG_EXTENSIONS = [
    '.jpg', '.JPG', '.jpeg', '.JPEG',
    '.png', '.PNG', '.ppm', '.PPM', '.bmp', '.BMP',
]

def is_image_file(filename):
    return any(filename.endswith(extension) for extension in IMG_EXTENSIONS)


def get_temp(img_filename,fir,pixel_pos):
    fir.process_image(img_filename)
    look_up_temp = fir.get_thermal_np()
    temp  = look_up_temp[int(pixel_pos[0]), int(pixel_pos[1])]
    return temp

def get_roi(bbox):
    pixel_pos = bbox[1] + bbox[3]/2, bbox[0] + bbox[2]/2
    return pixel_pos


def load_yaml(yaml_file):
    
    with open(yaml_file) as file:
        # The FullLoader parameter handles the conversion from YAML
        # scalar values to Python the dictionary format
        bboxs = yaml.load(file, Loader=yaml.FullLoader)
        return bboxs

def get_stats(results):
    mean = []
    std_dev = []
    variance = []
    for data in results:
        mean.append(np.mean(data))
        std_dev.append(np.std(data))
        variance.append(np.var(data))
    return mean, std_dev, variance


def plot_data(x, y):
    """
    x is mean and y is std_dev
    """
    x_pos = np.arange(len(x))
    fig, ax = plt.subplots()
    ax.set_ylabel("temp (celcius)")
    ax.set_xticks(x_pos)
    labels = list(map(str, x_pos))
    ax.set_xticklabels(labels)
    ax.set_title("temp measurement for various aribatary distances")
    ax.errorbar(x_pos,x, yerr=y, alpha=0.5, ecolor="black", capsize=10)
    
    
    #save the figure and show
    plt.tight_layout()
    plt.savefig("results.png")
    plt.show()

if __name__ == "__main__":
    yaml_file = "store_file.yaml"
    data = load_yaml(yaml_file)
    
    
    fir = flir_image_extractor.FlirImageExtractor()
    #file_path = "C:\\Users\\odusi\\Documents\\Projects\\ape_project\\flir_humans\\"
    #path to image directory...
    file_path  = data[0]["image_folder"][0]
    
    i = 0
    results = []
    for root, _, fnames in natsorted(os.walk(file_path)):
      
        temps = []
        for fname in natsorted(fnames):
                  
            frame = cv2.imread(os.path.join(root, fname))
                   
            bbox = data[1]["bbox"][i]
            # Draw bounding box
            
            """
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            cv2.rectangle(frame, p1, p2, (255,0,0), 2, 1)
         
            cv2.imshow("result", frame)
            cv2.waitKey(0)
            """
            pixel_pos = get_roi(bbox)
            temp = get_temp(os.path.join(root, fname), fir, pixel_pos)
            print ("temp is {}".format(temp))
            temps.append(temp)
           
            i = i+1
        results.append(temps)
    #make sure there are no empty list in lists
    results = np.array([np.array(r) for r in results if r])
    #get variance
    
 
    mean, std, var = get_stats(results)
    print ("maximum variance is {}".format(max(var)))

    #print ("mean is {}".format(mean))
    print ("minimum variance is {}".format(min(var)))
    plot_data(mean, std)
       
