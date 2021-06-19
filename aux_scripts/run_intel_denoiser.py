import os
import glob
import argparse

#python run_denoiser.py "C:\\Users\\Bernardo Silva\\Desktop\\Dataset\\dataset_4_png\\" "C:\\Users\\Bernardo Silva\\Desktop\\Dataset\\dataset_4_nvidia_results_png\\"

if __name__ == "__main__":
    command = "\"C:\\Users\\nreis\\Desktop\\LEI\\Optix\\build\\Release\\intel_image_denoiser.exe\""

    parser = argparse.ArgumentParser(description="Loads png images and loads them into png files")
    parser.add_argument("i",type=str)
    parser.add_argument("o",type=str)
    args = parser.parse_args()

    INPUT_PATH = args.i
    OUTPUT_PATH = args.o

    noisy_list = sorted(glob.glob(INPUT_PATH+"*_color.png"))
    albedo_list = sorted(glob.glob(INPUT_PATH+"*_albedo.png"))
    normal_list = sorted(glob.glob(INPUT_PATH+"*_normal.png"))
    for file in noisy_list:
        nr = file.split("\\")[-1]
        nr = nr.split("_")[0]
        com = command + " -i \""+file+"\""
        com = com + " -o \"" + OUTPUT_PATH + nr + "_prediction.png\" "
        if albedo_list:
            com = com + "-a \""+INPUT_PATH+nr+"_albedo.png\" " 
        if normal_list:
            com = com + "-n \""+INPUT_PATH+nr+"_normal.png\" " 
        print(com)
        stream = os.popen(com)
        output = stream.read()
        print(output)