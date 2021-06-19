import argparse
import tensorflow as tf
import cv2
import numpy as np
import glob

#python exr_to_png.py "C:\\Users\\Bernardo Silva\\Desktop\\Dataset\\dataset_4_nvidia_results_exr\\" "C:\\Users\\Bernardo Silva\\Desktop\\Dataset\\dataset_4_nvidia_results\\" "prediction"
#DATASET_PATH = "C:\\Users\\Bernardo Silva\\Desktop\\LEI\\Optix\\build\\Release\\generated_dataset\\"
#OUTPUT_PATH = "C:\\Users\\Bernardo Silva\\Desktop\\LEI\\aux_scripts\\exr\\"

def load_files(img):
    image = cv2.imread(img,cv2.IMREAD_UNCHANGED)
    image=image*65535
    image[image>65535]=65535
    image = np.uint16(image)
    img = img.split("\\")[-1]
    img = img.split("_")[0]
    img = OUTPUT_PATH+img+"_"+EXTENSION+".png"
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

    file_list = glob.glob(INPUT_PATH+"*_"+EXTENSION+".exr")
    print(file_list)
    for file in file_list:
        load_files(file)