import os
import glob
import argparse

if __name__ == "__main__":
    command = "\"C:\\ProgramData\\NVIDIA Corporation\\OptiX SDK 7.3.0\\SDK\\build\\bin\\Release\\optixDenoiser.exe\""

    parser = argparse.ArgumentParser(description="Loads png images and loads them into exr files")
    parser.add_argument("i",type=str)
    parser.add_argument("o",type=str)
    args = parser.parse_args()

    INPUT_PATH = args.i
    OUTPUT_PATH = args.o

    file_list = glob.glob(INPUT_PATH+"*_noisy.exr")
    for file in file_list:
        nr = file.split("\\")[-1]
        nr = nr.split("_")[0]
        com = command+" -o \""+OUTPUT_PATH+nr+"_prediction.exr\" " + "\""+file+"\""
        print(com)
        stream = os.popen(com)
        output = stream.read()
        print(output)