#%%
import sys
import logging
import pdb
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
        imgray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        ret,thresh = cv2.threshold(imgray, 120,255,cv2.THRESH_BINARY)
        image, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        c_img = cv2.drawContours(img, contours, -1, (0, 255, 0), 1)
        path = os.path.join(outpath,filename)
        if not os.path.exists(path):
            os.makedirs(path)
        for i in range(len(contours)):
                                cnt = contours[i]
                                x,y,w,h = cv2.boundingRect(cnt)
                                sub_img = img[y:y+h,x:x+w]
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
    save_images(outpath,c_images,filenames,cwd)
except Exception as e:
   logging.error("Exception occurred", exc_info=True)
    
#%%

    




