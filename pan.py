import numpy as np
from skimage.util import random_noise
from scipy import ndimage
import os
import cv2
import json
import random
import string
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

def read_pan(filename):
  if os.path.exists(filename):
    image = cv2.imread(filename)
    #image_rgb = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
    return image
  else:
    print("FileName not exists")

def process_image(filename):
  fake = Faker()
  image = read_pan(filename)

  font                   = cv2.FONT_HERSHEY_SIMPLEX
  bottomLeftCornerOfText = (105,445)
  fontScale              = 2.4
  fontColor              = (0,0,0)
  lineType               = 10

  new_image = image.copy()

  cv2.putText(new_image,'{}'.format(fake.name().upper()), 
      bottomLeftCornerOfText, 
      font, 
      fontScale,
      fontColor,
      lineType)

  bottomLeftCornerOfText = (105,611)
  cv2.putText(new_image, '{}'.format(fake.name().upper()), 
      bottomLeftCornerOfText, 
      font, 
      fontScale,
      fontColor,
      lineType)

  bottomLeftCornerOfText = (105,777)
  cv2.putText(new_image,'{}/{}/{}'.format(random.randint(0,30), random.randint(0,12), random.randint(1950,2010)), 
      bottomLeftCornerOfText, 
      font, 
      fontScale,
      fontColor,
      lineType)
  
  bottomLeftCornerOfText = (105,1025)
  cv2.putText(new_image, ''.join(random.choices(string.ascii_letters.upper() + string.digits, k=10)), 
      bottomLeftCornerOfText, 
      font, 
      fontScale,
      fontColor,
      lineType)

  return new_image

def generate_image(doc_path):
  '''
  Fucntion to place randomly created images of person to document
  '''
  new_image = process_image(doc_path)
  filename, s_img = create_random_person(450, 450)
  y_offset = 909
  x_offset = 1761

  new_image[y_offset:y_offset+s_img.shape[0], x_offset:x_offset+s_img.shape[1]] = s_img
  return new_image

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

def rotate_image(image, angle):
  image_center = tuple(np.array(image.shape[1::-1]) / 2)
  rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
  result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
  return result


def generate_bg_image(filename, noise_modes):
  '''
  FUnction to place document into an A4 sized white background image and adding some random noises using OpenCV.
  So this would look like a scanned document.
  '''
  image = generate_image(filename)
  img_person = cv2.resize(image, (779, 482))
  #img = ndimage.rotate(img, random.randint(-15,15), cval=255) ## Uncomment this line if you need to rotate image.
  bg = np.zeros([1500,1500,3],dtype=np.uint8)
  bg.fill(255)

  y_offset = random.randint(133,588) # 133 # 
  x_offset = random.randint(139, 580) # 139 # 

  bg[y_offset:y_offset+img_person.shape[0], x_offset:x_offset+img_person.shape[1]] = img_person
  
  # Add image binary masks.
  mask_bg = np.zeros([1500,1500,1],dtype=np.uint8)
  #mask = np.ones([img_person.shape[0], img_person.shape[1], 3], dtype=np.uint8)
  #mask.fill(255)
  
  mask_bg[y_offset:y_offset+img_person.shape[0], x_offset:x_offset+img_person.shape[1]] = 255

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
