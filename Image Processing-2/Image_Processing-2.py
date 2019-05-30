#%%
import csv
import glob
import sys
import logging
import numpy as np
from matplotlib import pyplot as plt
import cv2
import os

#%%
def load_images_from_folder(folder):
    try:
        images = []
        csvs = []
        for filename in os.listdir(folder):
            img = cv2.imread(os.path.join(folder,filename))
            if img is not None:
                images.append(img)
            exten=os.path.splitext(filename)[1]
            if exten == '.csv':
                csvs.append(filename)
    except Exception as e:
        logging.error("Exception occurred", exc_info=True)
    return images,csvs

#%%
def roi(images, csvs, inpath, outpath, cwd):
    try:
        for (image, csvfile) in zip(images,csvs):
            roi_per_csv(image, csvfile, inpath, outpath, cwd)
    except Exception as e:
        logging.error("Exception occurred", exc_info=True)

#%%
def roi_per_csv(image, csvfile, inpath, outpath, cwd):
    try:
        csv_reader = csv.reader(open(os.path.join(inpath,csvfile)), delimiter='|')     
        for row in csv_reader:
            cord=row[2]
            filename=row[0]
            if '-' in cord:
                mcords=cord.split("-")
                subfilenames=row[4].split("?")
                subfilenames.pop()
                if not os.path.exists(os.path.join(outpath,filename)):
                    os.makedirs(os.path.join(outpath,filename))
                i=0
                for mcord in mcords:
                    x,y,w,h = list(map(int, mcord.split(",")))
                    sub_img = image[y:y+h,x:x+w]
                    if subfilenames[0]=='':
                        cv2.imwrite(os.path.join(cwd,outpath,filename,str(i)+'.jpg'), sub_img)
                    else:
                        cv2.imwrite(os.path.join(cwd,outpath,filename,subfilenames[i]+'.jpg'), sub_img)
                        
                    i+=1
            else:
                x,y,w,h = list(map(int, cord.split(",")))
                sub_img = image[y:y+h,x:x+w]
                cv2.imwrite(os.path.join(cwd,outpath,filename+'.jpg'), sub_img)
    except Exception as e:
        logging.error("Exception occurred", exc_info=True)
 
#%%
try:
    outpath=sys.argv[2]
    if not os.path.exists(outpath):
        os.makedirs(outpath)
        logging.basicConfig(filename=os.path.join(outpath,'app.log'), filemode='w', format='%(name)s - %(levelname)s - %(message)s')
except Exception:
   logging.error("Exception occurred")

try:
    images=[]
    cwd=os.getcwd()
    images,csvs=load_images_from_folder(sys.argv[1])
    roi(images,csvs,sys.argv[1],outpath,cwd)
except Exception as e:
   logging.error("Exception occurred", exc_info=True)
    
#%%
