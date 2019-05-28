#!/usr/bin/env python
# coding: utf-8

# In[1]:

import sys
from matplotlib import pyplot as plt
import cv2
import os


# In[2]:


def load_images_from_folder(folder):
    images = []
    filenames = []
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder,filename))
        if img is not None:
            images.append(img)
            filenames.append(filename)
    return images,filenames


# In[3]:


def draw_contours(img,filename,outpath,cwd):
    imgray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    ret,thresh = cv2.threshold(imgray, 120,255,cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    c_img = cv2.drawContours(img, contours, -1, (0, 255, 0), 1)
    path = os.path.join(outpath,filename)
    if not os.path.exists(path):
        os.makedirs(path)
    for i in range(len(contours)):
                            cnt = contours[i]
                            x,y,w,h = cv2.boundingRect(cnt)
                            sub_img = img[y:y+h,x:x+w]
                            cv2.imwrite(os.path.join(cwd,outpath,filename,str(i)+'.jpg'), sub_img)
    return c_img
    


# In[4]:


def contours(images,filenames,outpath,cwd):
    c_imgs=[]
    i=0
    for image in images:
        c_img=draw_contours(image,filenames[i],outpath,cwd)
        c_imgs.append(c_img)
        i+=1
    return c_imgs


# In[5]:


def save_images(output,imgs,filenames,cwd):
    if not os.path.exists(output):
        os.makedirs(output)
    i=0
    for img in imgs:
        cv2.imwrite(os.path.join(cwd,output,filenames[i]+'.jpg'),img)
        i+=1


# In[6]:

if(len(sys.argv)!=3):
    print("Input the filename correctly")
else:
    images=[]
    cwd=os.getcwd()
    outpath=sys.argv[2]
    images,filenames=load_images_from_folder(sys.argv[1])
    c_images=contours(images,filenames,outpath,cwd)
    save_images(outpath,c_images,filenames,cwd)
    

# In[ ]:




