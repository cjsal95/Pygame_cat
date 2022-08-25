import os
import pygame

def readImg(dirname, exts=[".png", ".jpg"]):
    
    img_list = []

    filenames = os.listdir(dirname)
    for filename in filenames:
        full_filename = os.path.join(dirname, filename)
        ext = os.path.splitext(full_filename)[-1]
        if ext in exts: 
            img_list.append(pygame.image.load(full_filename))
    
    return img_list
