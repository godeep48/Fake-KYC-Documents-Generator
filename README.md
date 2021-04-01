# Fake KYC Document Generator
**This project is simply for the purpose of education.** The primary objective of this project is to build a deep-learning model to identify and classify (Image segmentation and Classification) the given KYC document and extract the information from them. The model requires tens and thousands of data for better results, and since these are confidential documents, I cannot train the model with original KYC documents (Aadhar, PAN, License). So I come up with a solution by faking KYC document. By this methods we can create more that thousands of images and can train the model with these fake documents.

## Output
Fake KYC Documents (Aadhar card, PAN card and License) in scanned A4 format and its binary mask image for image segmentation

## Requirment
* numpy
* skimage
* scipy
* os
* OpenCV
* json
* random
* string
* tqdm
* uuid
* requests
* [faker](https://pypi.org/project/Faker/)

## How to run?

```
process.py [-h] [-af AADHARFRONT] [-ab AADHARBACK] [-p PAN]
           [-l LICENSE] -c COUNT -o OUT

optional arguments:
  -h, --help            show this help message and exit
  -af AADHARFRONT, --aadharfront AADHARFRONT
                        Path to Front face of Aadhar card
  -ab AADHARBACK, --aadharback AADHARBACK
                        Path to Back face of Aadhar card
  -p PAN, --pan PAN     Path to PAN card
  -l LICENSE, --license LICENSE
                        Path to License document
  -c COUNT, --count COUNT
                        Number of images you want to save
  -o OUT, --out OUT     destination in which you want to save images
```
