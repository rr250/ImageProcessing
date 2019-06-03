#%%
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
        th3 = cv2.adaptiveThreshold(imgray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,3,15)
        y,x=th3.shape
        for i in range(y):
            c=0
            for j in range(x):
                if th3[i][j]==0:
                    c+=1
            if c<15:
                for j in range(x):
                    th3[i][j]=255
        kernel = np.ones((3, 3), np.uint8) 
        closing = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations = 2) 
        image, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        path = os.path.join(outpath,filename)
        if not os.path.exists(path):
            os.makedirs(path)       
        cv2.imwrite(os.path.join(cwd,outpath,filename,'close'+'.jpg'), thresh)
        for i in range(len(contours)):
            cnt = contours[i]
            x,y,w,h = cv2.boundingRect(cnt)
            sub_img = img[y:y+h,x:x+w]
            h1,w1,_= sub_img.shape
            print(i,sub_img.shape)
            if(h1>21 and w1<400 and w1>7 and (h1,w1)!=(33,16) and w1!=15):
                if(w1>38):
                    sub_img1=sub_img[0:h1,0:int(w1/2)]
                    sub_img2=sub_img[0:h1,int(w1/2):w1]
                    cv2.imwrite(os.path.join(cwd,outpath,filename,str(i)+'1'+'.jpg'), sub_img1)
                    cv2.imwrite(os.path.join(cwd,outpath,filename,str(i)+'2'+'.jpg'), sub_img2)
                else:
                    cv2.imwrite(os.path.join(cwd,outpath,filename,str(i)+'.jpg'), sub_img)
    except Exception as e:
        logging.error("Exception occurred", exc_info=True)
    return

#%%    
def contours(images,filenames,outpath,cwd):
    try:
        i=0
        for image in images:
            draw_contours(image,filenames[i],outpath,cwd)
            i+=1
    except Exception as e:
        logging.error("Exception occurred", exc_info=True)
    return

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
    contours(images,filenames,outpath,cwd)
except Exception as e:
   logging.error("Exception occurred", exc_info=True)
    
#%%

    




