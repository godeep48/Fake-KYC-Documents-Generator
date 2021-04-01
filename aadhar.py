import numpy as np
from skimage.util import random_noise
from scipy import ndimage
import os
import cv2
import json
import random
from tqdm import tqdm
import uuid
import requests
from faker import Faker

def filename_generator(path):
    '''
    Function to create random unique filenames
    '''
    dir = path
    if not os.path.exists(dir):
        os.makedirs(dir)
    id = str(uuid.uuid4())
    if not os.path.exists(path+id+".jpg"):
        return path+id+".jpg"
    else:
        filename_generator()

def create_random_person(height, width):
    '''
    Function to download random unreal persons from site:thispersondoesnotexists.com
    More info on how it works: https://arxiv.org/abs/1912.04958
    '''
    filename = filename_generator("static/person/")
    f = open(filename,'wb')
    f.write(requests.get('https://thispersondoesnotexist.com/image', headers={'User-Agent': 'My User Agent 1.0'}).content)
    f.close()
    person_img = cv2.imread(filename, -1)
    s_img = cv2.resize(person_img, (width, height))
    #cv2.imwrite(filename, s_img)
    return filename, s_img

def read_aadhar(filename):
    if os.path.exists(filename):
        image = cv2.imread(filename)
        #image_rgb = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        return image
    else:
        print("FileName not exists")


def process_image(filename_front, filename_back):
    fake = Faker()
    image_front = read_aadhar(filename_front)
    image_back = read_aadhar(filename_back)

    aadhar_no = str(random.randint(1111,9999))+" "+str(random.randint(1111,9999))+" "+str(random.randint(1111,9999))
    font                   = cv2.FONT_HERSHEY_SIMPLEX
    bottomLeftCornerOfText = (750,430)
    fontScale              = 1.5
    fontColor              = (0,0,0)
    lineType               = 2

    cv2.putText(image_front,'Name: {}'.format(fake.name()), 
        bottomLeftCornerOfText, 
        font, 
        fontScale,
        fontColor,
        lineType)

    bottomLeftCornerOfText = (750,530)
    cv2.putText(image_front,'DOB : {}/{}/{}'.format(random.randint(0,30), random.randint(0,12), random.randint(1950,2000)), 
        bottomLeftCornerOfText, 
        font, 
        fontScale,
        fontColor,
        lineType)

    bottomLeftCornerOfText = (750,630)
    cv2.putText(image_front, random.choice(["Male", "Female"]), 
        bottomLeftCornerOfText, 
        font, 
        fontScale,
        fontColor,
        lineType)

    fontScale              = 3
    lineType               = 8
    bottomLeftCornerOfText = (750,1167)
    cv2.putText(image_front,'{}'.format(aadhar_no), 
        bottomLeftCornerOfText, 
        font, 
        fontScale,
        fontColor,
        lineType)
    
    ##### Back Image ####
    
    font                   = cv2.FONT_HERSHEY_SIMPLEX
    bottomLeftCornerOfText = (177,480)
    fontScale              = 1.5
    fontColor              = (0,0,0)
    lineType               = 2

    address = fake.address().split("\n")
    cv2.putText(image_back,'Address: S/O: {}'.format(fake.name()), 
        bottomLeftCornerOfText, 
        font, 
        fontScale,
        fontColor,
        lineType)
    
    bottomLeftCornerOfText = (177, 580)
    address = fake.address().split("\n")
    cv2.putText(image_back,'{}'.format(address[0]), 
        bottomLeftCornerOfText, 
        font, 
        fontScale,
        fontColor,
        lineType)
    
    bottomLeftCornerOfText = (177, 680)
    cv2.putText(image_back,'{}, {}'.format(address[1], random.randint(543543,765765)), 
        bottomLeftCornerOfText, 
        font, 
        fontScale,
        fontColor,
        lineType)
    
    fontScale              = 3
    lineType               = 8
    bottomLeftCornerOfText = (750,1220)
    cv2.putText(image_back,'{}'.format(aadhar_no), 
        bottomLeftCornerOfText, 
        font, 
        fontScale,
        fontColor,
        lineType)

    return image_front, image_back

def generate_image(aadhar_front, aadhar_back):
    '''
    Fucntion to place randomly created images of person to document
    '''
    front_image, back_image = process_image(aadhar_front, aadhar_back)
    filename, s_img = create_random_person(650, 550)
    y_offset = 365
    x_offset = 129

    front_image[y_offset:y_offset+s_img.shape[0], x_offset:x_offset+s_img.shape[1]] = s_img
    return front_image, back_image

def rotate_image(image, angle):
    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
    result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
    return result

def add_noise(image, modes, randomize=True):
    '''
    Adding noise to the image
    '''
    flag = random.choice([0,1]) if randomize==True else 1
    if flag==1:
      mode = random.choice(modes)
      image = random_noise(image, mode=mode)
      noise_img = np.array(255*image, dtype = 'uint8')
      return noise_img
    else:
      return image

# noise_modes = ['gaussian','localvar','poisson','salt','pepper','speckle']

def generate_bg_image(filename_front, filename_back, noise_modes):
    '''
    FUnction to place document into an A4 sized white background image and adding some random noises using OpenCV.
    So this would look like a scanned document.
    '''
    front, back = generate_image(filename_front, filename_back)
    front = cv2.resize(front, (779, 482))
    back = cv2.resize(back, (779, 482))
    #img = ndimage.rotate(img, random.randint(-15,15), cval=255) ## Uncomment this line if you need to rotate image.
    bg = np.zeros([1500,1500,3],dtype=np.uint8)
    bg.fill(255)

    y_offset_front = random.randint(133,288) # 133 # 
    x_offset_front = random.randint(139, 580) # 139 # 
    y_offset_back = random.randint(700,900) # 133 # 
    x_offset_back = random.randint(139, 580) # 139 # 

    bg[y_offset_front:y_offset_front+front.shape[0], x_offset_front:x_offset_front+front.shape[1]] = front
    bg[y_offset_back:y_offset_back+back.shape[0], x_offset_back:x_offset_back+back.shape[1]] = back
    
    # Add image binary masks.
    mask_bg = np.zeros([1500,1500,1],dtype=np.uint8)
    #mask = np.ones([img_person.shape[0], img_person.shape[1], 3], dtype=np.uint8)
    #mask.fill(255)
    
    mask_bg[y_offset_front:y_offset_front+front.shape[0], x_offset_front:x_offset_front+front.shape[1]] = 255
    mask_bg[y_offset_back:y_offset_back+back.shape[0], x_offset_back:x_offset_back+back.shape[1]] = 255

    angle = random.randint(-15,15)
    bg = ndimage.rotate(bg, angle, cval=255, reshape=False) ## Uncomment this line if you dont want to randomly rotate images
    #mask_bg = ndimage.rotate(mask_bg, angle, cval=0, reshape=False) ## Uncomment this line if you dont want to randomly rotate masks
    #bg = rotate_image(bg, angle)
    mask_bg = rotate_image(mask_bg, angle)

    mask_bg[mask_bg!=255]=0

    img = add_noise(bg, noise_modes, True)

    return img, mask_bg

def random_id(dir):
    '''
    Random ID generator.
    Check whether dir name with random id already exists, if not then return the ID.
    '''
    id = str(uuid.uuid4())
    dir_new = dir+id+"/"
    if not os.path.exists(dir_new):
      return id
    else:
      random_id(dir)

