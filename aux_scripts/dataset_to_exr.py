import subprocess
import argparse

#python dataset_to_exr.py "C:\\Users\\Bernardo Silva\\Desktop\\Dataset\\dataset_4\\test\\" "C:\\Users\\Bernardo Silva\\Desktop\\Dataset\\dataset_4_exr\\test\\"

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="Loads png images and loads them into exr files")
    parser.add_argument("i",type=str)
    parser.add_argument("o",type=str)
    args = parser.parse_args()

    INPUT_PATH = args.i
    OUTPUT_PATH = args.o

    extensions = ["accumulated","albedo","color","noisy","normal"]

    for e in extensions:
        subprocess.call(['python','png_to_exr.py', INPUT_PATH, OUTPUT_PATH, e])

