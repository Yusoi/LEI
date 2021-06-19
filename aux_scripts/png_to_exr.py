import argparse
import tensorflow as tf
import cv2
import numpy as np
import glob

#python png_to_exr.py "C:\\Users\\Bernardo Silva\\Desktop\\LEI\\Optix\\build\\Release\\generated_dataset\\" "C:\\Users\\Bernardo Silva\\Desktop\\LEI\\aux_scripts\\exr\\" "noisy"
#DATASET_PATH = "C:\\Users\\Bernardo Silva\\Desktop\\LEI\\Optix\\build\\Release\\generated_dataset\\"
#OUTPUT_PATH = "C:\\Users\\Bernardo Silva\\Desktop\\LEI\\aux_scripts\\exr\\"

def load_files(img, EXTENSION):
    image = cv2.imread(img,cv2.IMREAD_UNCHANGED)
    if EXTENSION == "normal":
        image = (image/125.5)-1
    else:
        image = image/255.0
    image = image.astype("float32")
    img = img.split("\\")[-1]
    img = img.split("_")[0]
    img = OUTPUT_PATH+img+"_"+EXTENSION+".exr"
    print(img)
    cv2.imwrite(img,image)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Loads png images and loads them into exr files")
    parser.add_argument("i",type=str)
    parser.add_argument("o",type=str)
    parser.add_argument("ext",type=str)
    args = parser.parse_args()

    INPUT_PATH = args.i
    OUTPUT_PATH = args.o
    EXTENSION = args.ext

    file_list = glob.glob(INPUT_PATH+"*_"+EXTENSION+".png")
    for file in file_list:
        load_files(file, EXTENSION)