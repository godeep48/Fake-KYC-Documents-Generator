from tqdm import tqdm
import os
import cv2
from aadhar import random_id as aadhar_random_id, generate_bg_image as aadhar_generator
from pan import random_id as pan_random_id
from pan import generate_bg_image as pan_generator
from license import random_id as license_random_id
from license import generate_bg_image as license_generator
import argparse

my_parser = argparse.ArgumentParser()

my_parser.add_argument('-af','--aadharfront', action='store', type=str, help="Path to Front face of Aadhar card")
my_parser.add_argument('-ab','--aadharback', action='store', type=str, help="Path to Back face of Aadhar card")
my_parser.add_argument('-p','--pan', action='store', type=str, help="Path to PAN card")
my_parser.add_argument('-l','--license', action='store', type=str, help="Path to License document")
my_parser.add_argument('-c','--count', action='store', type=int, required=True, help="Number of images you want to save")
my_parser.add_argument('-o','--out', action='store', type=str, required=True, help="destination in which you want to save images")


noise_modes = ['gaussian','localvar','poisson','salt','pepper','speckle']

def save_aadhar(doc_front, doc_back, dest_path, count):
    print("Generating Aadhar and its binary masks...")
    for i in tqdm(range(0, count)):
        id = aadhar_random_id(dest_path)
        dir = dest_path+id+'/'
        if not os.path.exists(dir):
            os.makedirs(dir)
        image_dir = dir+"images/"
        mask_dir = dir+"masks/"
        if not os.path.exists(image_dir):
            os.makedirs(image_dir)
        if not os.path.exists(mask_dir):
            os.makedirs(mask_dir)
        image, mask = aadhar_generator(doc_front, doc_back, noise_modes)
        cv2.imwrite(image_dir+id+'.png', image)
        cv2.imwrite(mask_dir+id+'.png', mask)

def save_pan(src_path, dest_path, count):
    print("Generating Pan Card and its binary masks...")
    for i in tqdm(range(0, count)):
        id = pan_random_id(dest_path)
        dir = dest_path+id+'/'
        if not os.path.exists(dir):
            os.makedirs(dir)
        image_dir = dir+"images/"
        mask_dir = dir+"masks/"
        if not os.path.exists(image_dir):
            os.makedirs(image_dir)
        if not os.path.exists(mask_dir):
            os.makedirs(mask_dir)
        image, mask = pan_generator(src_path, noise_modes)
        cv2.imwrite(image_dir+id+'.png', image)
        cv2.imwrite(mask_dir+id+'.png', mask)

def save_license(doc_path, path, count):
    print("Generating License and its binary mask..")
    for i in tqdm(range(0, count)):
        id = license_random_id(path)
        dir = path+id+'/'
        if not os.path.exists(dir):
            os.makedirs(dir)
        image_dir = dir+"images/"
        mask_dir = dir+"masks/"
        if not os.path.exists(image_dir):
            os.makedirs(image_dir)
        if not os.path.exists(mask_dir):
            os.makedirs(mask_dir)
        image, mask = license_generator(doc_path, noise_modes)
        cv2.imwrite(image_dir+id+'.png', image)
        cv2.imwrite(mask_dir+id+'.png', mask)

#save_aadhar("src/aadhar_front.jpg", "src/aadhar_back.jpg", "train/", 2)
#save_pan("src/pan_new.jpg", "train/", 2)
#save_license("src/License_new.jpg", "train/", 2)

args = my_parser.parse_args()

if args.aadharfront is not None and args.aadharback is not None:
    if not os.path.exists(args.aadharfront):
        raise FileNotFoundError("Aadhar card not found")
    if not os.path.exists(args.aadharback):
        raise FileNotFoundError("Aadhar card not found")
    else:
        save_aadhar(args.aadharfront, args.aadharback, args.out, args.count)
if args.pan is not None:
    if not os.path.exists(args.pan):
        raise FileNotFoundError("PAN card not found")
    else:
        save_pan(args.pan, args.out, args.count)
if args.license is not None:
    if not os.path.exists(args.license):
        raise FileNotFoundError("License not Found!")
    else:
        save_license(args.license, args.out, args.count)