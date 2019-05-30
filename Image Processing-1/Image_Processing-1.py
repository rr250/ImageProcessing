#%%
import sys
import logging
import pdb
import numpy as np
from matplotlib import pyplot as plt
import cv2
import os

#%%
def load_images_from_folder(folder):
    try:
        images = []
        filenames = []
        for filename in os.listdir(folder):
            img = cv2.imread(os.path.join(folder,filename))
            if img is not None:
                images.append(img)
                filenames.append(filename)
    except Exception as e:
        logging.error("Exception occurred", exc_info=True)
    return images,filenames

#%%
def draw_contours(img,filename,outpath,cwd):
    try:
        kernel = np.ones((5,5),np.uint8)
        c_img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
        #c_img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
        imgray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        ret,thresh = cv2.threshold(imgray, 120,255,cv2.THRESH_BINARY)
        # noise removal
        kernel = np.ones((3,3),np.uint8)
        opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 1)
        dilation = cv2.erode(opening,kernel,iterations = 1)
#        closing = cv2.morphologyEx(dilation, cv2.MORPH_CLOSE, kernel)
#        # sure background area
#        sure_bg = cv2.dilate(opening,kernel,iterations=3)
#        
#        # Finding sure foreground area
#        dist_transform = cv2.distanceTransform(opening,cv2.DIST_L2,5)
#        ret, sure_fg = cv2.threshold(dist_transform,0.7*dist_transform.max(),255,0)
#        
#        # Finding unknown region
#        sure_fg = np.uint8(sure_fg)
#        unknown = cv2.subtract(sure_bg,sure_fg)
#        # Marker labelling
#        ret, markers = cv2.connectedComponents(sure_fg)
#        
#        # Add one to all labels so that sure background is not 0, but 1
#        markers = markers+1
#        
#        # Now, mark the region of unknown with zero
#        markers[unknown==255] = 0
        image, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        kernel = np.ones((5,5),np.uint8)
        path = os.path.join(outpath,filename)
        if not os.path.exists(path):
            os.makedirs(path)        
        for i in range(len(contours)):
                                cnt = contours[i]
                                x,y,w,h = cv2.boundingRect(cnt)
                                sub_img = img[y:y+h,x:x+w]
                                h1,w1,_= sub_img.shape
                                if(h1>20 and i>0):
                                    cv2.imwrite(os.path.join(cwd,outpath,filename,str(i)+'.jpg'), sub_img)
    except Exception as e:
        logging.error("Exception occurred", exc_info=True)
    return c_img

#%%    
def contours(images,filenames,outpath,cwd):
    try:
        c_imgs=[]
        i=0
        for image in images:
            c_img=draw_contours(image,filenames[i],outpath,cwd)
            c_imgs.append(c_img)
            i+=1
    except Exception as e:
        logging.error("Exception occurred", exc_info=True)
    return c_imgs

#%%
def save_images(output,imgs,filenames,cwd):
    try:
        if not os.path.exists(output):
            os.makedirs(output)
        i=0
        for img in imgs:
            cv2.imwrite(os.path.join(cwd,output,filenames[i]+'.jpg'),img)
            i+=1
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
    images,filenames=load_images_from_folder(sys.argv[1])
    c_images=contours(images,filenames,outpath,cwd)
except Exception as e:
   logging.error("Exception occurred", exc_info=True)
    
#%%

    




