import subprocess

file_list = glob.glob(INPUT_PATH+"*_noisy.exr")

if __name__ == "__main__":
    command = "C:\\ProgramData\\NVIDIA Corporation\\OptiX SDK 7.3.0\\SDK\\build\\bin\\Release\\optixDenoiser.exe"

    parser = argparse.ArgumentParser(description="Loads png images and loads them into exr files")
    parser.add_argument("i",type=str)
    parser.add_argument("o",type=str)
    args = parser.parse_args()

    INPUT_PATH = args.i
    OUTPUT_PATH = args.o

    file_list = glob.glob(INPUT_PATH+"*_noisy.png")
    for file in file_list:
        load_files(file)