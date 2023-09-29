# -*- coding: utf-8 -*-
# Copyright (c) The AI Lab. All Rights Reserved


import matplotlib.pyplot as plt
import numpy as np


speed_kmhs = [30, 50, 80, 110, 130]
shutterspeed_us = np.array([0, 35.50, 50, 100, 200, 250, 500])

#Shutter speed in seconds
shutterspeed_s = 0.00025

# Horizontal resotultion (plane of movement of vehicle)
h_resolution = 4096

# Distance from camera to road side in meters
working_distance_meters = 7

# With of object in mm with the given focal lenght, sensor size, and working distance
# See https://thinklucid.com/lens-calculator/
width_of_object_mm = 6546.75 

pixel_blur_in_pixels_list=[]



for speed_kmh in speed_kmhs:

    # calculate speed in meter per secons
    speed_mps=speed_kmh/3.6
    

    # ground sampling distance in mm
    pixels_per_mm = h_resolution/width_of_object_mm
    
    # Calculate movement in mm during exposure tiem
    movement_in_exposuretime_mm = speed_mps*shutterspeed_us/1000
    
    #calculate blur in pixels during exposure time
    pixel_blur_in_pixels = pixels_per_mm*movement_in_exposuretime_mm
    pixel_blur_in_pixels = pixel_blur_in_pixels/2 # divide by two because of bayer filter
    
    pixel_blur_in_pixels_list.append(pixel_blur_in_pixels)
    


# Make plots
plt.figure()
with plt.style.context('ggplot'):
    plt.plot(shutterspeed_us, np.array(pixel_blur_in_pixels_list).T)

    plt.xlabel('Exposure time [µs]')
    plt.ylabel('Perceived pixel blur [pixels]')
    
    plt.axvline(x=35.5, color='green')
    plt.axvline(x=250, color='green')
    
    plt.xlim([0, max(shutterspeed_us)])
    plt.ylim([0, max(pixel_blur_in_pixels)])
    plt.legend([str(x)+' km/h' for x in speed_kmhs], loc="upper left", bbox_to_anchor=(0.1,1.0))
    plt.tight_layout()
    plt.savefig('motion_blur.pdf')
    plt.savefig('motion_blur.png', dpi=300)
