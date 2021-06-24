import os
import glob
import argparse

#python run_denoiser.py "C:\\Users\\Bernardo Silva\\Desktop\\Dataset\\dataset_4_exr\\" "C:\\Users\\Bernardo Silva\\Desktop\\Dataset\\dataset_4_nvidia_results_exr\\"

if __name__ == "__main__":
    command = "\"C:\\ProgramData\\NVIDIA Corporation\\OptiX SDK 7.3.0\\SDK\\build\\bin\\Release\\optixDenoiser.exe\""

    parser = argparse.ArgumentParser(description="Loads png images and loads them into exr files")
    parser.add_argument("i",type=str)
    parser.add_argument("o",type=str)
    args = parser.parse_args()

    INPUT_PATH = args.i
    OUTPUT_PATH = args.o

    noisy_list = sorted(glob.glob(INPUT_PATH+"*_noisy.exr"))
    albedo_list = []#sorted(glob.glob(INPUT_PATH+"*_albedo.exr"))
    normal_list = []#sorted(glob.glob(INPUT_PATH+"*_normal.exr"))

    for file in noisy_list:
        nr = file.split("\\")[-1]
        nr = nr.split("_")[0]
        com = command+" -o \""+OUTPUT_PATH+nr+"_prediction.exr\" "
        if albedo_list:
            com = com + "-a \""+INPUT_PATH+nr+"_albedo.exr\" " 
        if normal_list:
            com = com + "-n \""+INPUT_PATH+nr+"_normal.exr\" " 
        com = com + "\""+file+"\""
        print(com)
        stream = os.popen(com)
        output = stream.read()
        print(output)