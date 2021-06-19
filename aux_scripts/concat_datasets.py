import argparse
import cv2
import numpy as np
import glob
import shutil

#python concat_datasets.py "C:\\Users\\Bernardo Silva\\Desktop\\Dataset\\dataset_4\\" "C:\\Users\\Bernardo Silva\\Desktop\\Dataset\\generated_dataset\\" "C:\\Users\\Bernardo Silva\\Desktop\\Dataset\\final_dataset_4\\"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Loads png images and loads them into exr files")
    parser.add_argument("fst",type=str)
    parser.add_argument("snd",type=str)
    parser.add_argument("to",type=str)
    args = parser.parse_args()

    FST_PATH = args.fst
    SND_PATH = args.snd
    TO_PATH = args.to

    fst_accumulated = sorted(glob.glob(FST_PATH+"*_accumulated.png"))
    fst_albedo = sorted(glob.glob(FST_PATH+"*_albedo.png"))
    fst_color = sorted(glob.glob(FST_PATH+"*_color.png"))
    fst_noisy = sorted(glob.glob(FST_PATH+"*_noisy.png"))
    fst_normal = sorted(glob.glob(FST_PATH+"*_normal.png"))
    fst = zip(fst_accumulated,fst_albedo,fst_color,fst_noisy,fst_normal)

    snd_accumulated = sorted(glob.glob(SND_PATH+"*_accumulated.png"))
    snd_albedo = sorted(glob.glob(SND_PATH+"*_albedo.png"))
    snd_color = sorted(glob.glob(SND_PATH+"*_color.png"))
    snd_noisy = sorted(glob.glob(SND_PATH+"*_noisy.png"))
    snd_normal = sorted(glob.glob(SND_PATH+"*_normal.png"))
    snd = zip(snd_accumulated,snd_albedo,snd_color,snd_noisy,snd_normal)

    max_fst = 0

    for img in fst:
        max_fst = max(max_fst,int(img[0].split("\\")[-1].split("_")[0]))
        shutil.copyfile(img[0],TO_PATH+img[0].split("\\")[-1])
        shutil.copyfile(img[1],TO_PATH+img[1].split("\\")[-1])
        shutil.copyfile(img[2],TO_PATH+img[2].split("\\")[-1])
        shutil.copyfile(img[3],TO_PATH+img[3].split("\\")[-1])
        shutil.copyfile(img[4],TO_PATH+img[4].split("\\")[-1])

    for img in snd:
        max_fst = max_fst+1
        shutil.copyfile(img[0],TO_PATH+str(max_fst)+"_accumulated.png")
        shutil.copyfile(img[1],TO_PATH+str(max_fst)+"_albedo.png")
        shutil.copyfile(img[2],TO_PATH+str(max_fst)+"_color.png")
        shutil.copyfile(img[3],TO_PATH+str(max_fst)+"_noisy.png")
        shutil.copyfile(img[4],TO_PATH+str(max_fst)+"_normal.png")

