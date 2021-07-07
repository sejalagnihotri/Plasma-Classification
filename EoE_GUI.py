# coding: utf-8

# In[43]:


import os
import cv2 
import numpy as np 
from IPython import display
import streamlit as st
import pandas as pd
import time

st.sidebar.markdown("<h1 style='text-align: left; color: maroon;'>Plasma-Classification </h1>",unsafe_allow_html=True)
st.sidebar.markdown("<h1 style='text-align: left; color: maroon;'></h1>",unsafe_allow_html=True)
st.sidebar.markdown("<h1 style='text-align: left; color: maroon;'></h1>",unsafe_allow_html=True)
st.sidebar.markdown("<h1 style='text-align: left; color: maroon;'></h1>",unsafe_allow_html=True)
st.sidebar.markdown("<h4 style='text-align: left; color: maroon;'>Select Feature:</h4>",unsafe_allow_html=True)
# In[41]:

feature_name=st.sidebar.selectbox("",("Surface Touch Detection", "Area and Other Features"))


DIR="NM_PRUJECT_WITH_MS"

all_folds=os.listdir(DIR)
all_folds.sort()
LOC=DIR+"/"+all_folds[11]
all_files=os.listdir(LOC)
all_files.sort()
LOC=DIR+"/"+all_folds[11]
all_files=os.listdir(LOC)
all_files.sort()
# In[22]:

if feature_name=="Surface Touch Detection":
    image_holder = st.empty()
    
    text_holder=st.empty()
    text_holder5=st.empty() 
    text_holder1=st.empty()
    text_holder2=st.empty()
    text_holder3=st.empty()
    text_holder4=st.empty()
    text_holder9=st.empty()
    text_holder10=st.empty()
    text_holder.text("")
    text_holder5.text("")
    text_holder1.text("")
    text_holder2.text("")
    text_holder3.text("")
    text_holder4.text("")
    text_holder9.text("")
    text_holder10.text("")

    img = cv2.imread(LOC+"/"+all_files[10],cv2.IMREAD_GRAYSCALE) 
    vecR=np.array([1 for i in range(img.shape[1])])
    vecC=np.array([1 for i in range(img.shape[0])])
    for i in all_files:
        img = cv2.imread(LOC+"/"+i,cv2.IMREAD_GRAYSCALE)
        ret,img = cv2.threshold(img,50,255,cv2.THRESH_TOZERO)
        
        norm_row=img.dot(vecR)
        norm_col=img.T.dot(vecC)
        
        image_holder.image(img,width=250)

        # time.sleep(5000)
        if max(norm_row)>100 or max(norm_col)>100:
            text_holder.markdown("<h3 style='text-align: left; color: green;'>Plasma is touching the surface!</h3>",unsafe_allow_html=True)
        else:
            text_holder.markdown("<h3 style='text-align: left; color: red;'>Plasma is not touching the surface!</h3>",unsafe_allow_html=True)
        time.sleep(0.2)
        # st.pyplot(plt)


# In[32]:
elif feature_name=="Area and Other Features":
    image_holder = st.empty()
   
    text_holder=st.empty()
    text_holder5=st.empty()
    text_holder1=st.empty()
    text_holder2=st.empty()
    text_holder3=st.empty()
    text_holder4=st.empty()
    text_holder9=st.empty()
    text_holder10=st.empty()
    
    
    LOC=DIR+"/"+all_folds[11]
    all_files=os.listdir(LOC)
    all_files.sort()
    FPS=5
    TimeFact=1000/5

    img = cv2.imread(LOC+"/"+all_files[0],cv2.IMREAD_GRAYSCALE)
    totalPix=img.shape[0]*img.shape[1]
    buff_row=[img.shape[0]/2,img.shape[0]/2]
    buff_col=[img.shape[1]/2,img.shape[1]/2]
    vecR=np.array([1 for i in range(img.shape[1])])
    vecC=np.array([1 for i in range(img.shape[0])])
    for i in all_files:
        DOWNDIR=False
        RIGHTDIR=False
        UP=0
        DOWN=0
        LEFT=0
        RIGHT=0
        img = cv2.imread(LOC+"/"+i,cv2.IMREAD_GRAYSCALE)
        ret,img = cv2.threshold(img,50,255,cv2.THRESH_TOZERO)
        ret,imgB = cv2.threshold(img,50,255,cv2.THRESH_BINARY)
        norm_row=img.dot(vecR)
        norm_col=img.T.dot(vecC)
        image_holder.image(img,width=250)



        if max(norm_row)>100 or max(norm_col)>100:
            text_holder.markdown("<h3 style='text-align: left; color: green;'>Plasma is touching the surface!</h3>",unsafe_allow_html=True)
            for j in range(norm_row.shape[0]):
                if not DOWNDIR:
                    if norm_row[j]!=0:
                        if j<buff_row[0]:
                            UP+=1
                        elif j==buff_row[0]:
                            pass
                        elif j>buff_row[0]:
                            UP-=1
                        upVel=j-buff_row[0]
                        buff_row[0]=j
                        DOWNDIR=True
                if DOWNDIR:
                    if norm_row[j]==0:
                        if j>buff_row[1]:
                            DOWN+=1
                        elif j==buff_row[1]:
                            pass
                        elif j<buff_row[1]:
                            DOWN-=1
                        downVel=j-buff_row[1]
                        buff_row[1]=j
                        break
            for j in range(norm_col.shape[0]):
                if not RIGHTDIR:
                    if norm_col[j]!=0:
                        if j<buff_col[0]:
                            LEFT+=1
                        elif j==buff_col[0]:
                            pass
                        elif j>buff_row[0]:
                            LEFT-=1
                        rightVel=j-buff_col[0]
                        buff_col[0]=j
                        RIGHTDIR=True
                if RIGHTDIR:
                    if norm_col[j]==0:
                        if j>buff_col[1]:
                            RIGHT+=1
                        elif j==buff_col[1]:
                            pass
                        elif j<buff_row[1]:
                            RIGHT-=1
                        leftVel=j-buff_col[1]
                        buff_col[1]=j
                        break
            if (UP+DOWN+LEFT+RIGHT)==0:
                text_holder5.markdown("<h3 style='text-align: left; color: red;'>Plasma is not moving!</h3>",unsafe_allow_html=True)
            else:
                if (UP>0) and (DOWN>0) and (LEFT>0) and (RIGHT>0):
                    text_holder5.markdown("<h3 style='text-align: left; color: green;'>Plasma is Expanding!</h3>",unsafe_allow_html=True)
                elif (UP<0) and (DOWN<0) and (LEFT<0) and (RIGHT<0):
                    text_holder5.markdown("<h3 style='text-align: left; color: green;'>Plasma is Contracting!</h3>",unsafe_allow_html=True)
                else:
                    if (UP>0) and (DOWN>0):
                        text_holder1.markdown("<h3 style='text-align: left; color: blue;'>Plasma is Expanding Vertically!</h3>",unsafe_allow_html=True)
                    elif ((UP>0) and (DOWN==0)):
                        text_holder1.markdown("<h3 style='text-align: left; color: blue;'>Plasma is Expanding in Upward Direction!</h3>",unsafe_allow_html=True)
                    elif ((UP==0) and (DOWN>0)):
                        text_holder1.markdown("<h3 style='text-align: left; color: blue;'>Plasma is Expanding in Downward Direction!</h3>",unsafe_allow_html=True)
                    elif ((UP<0) and (DOWN==0)):
                        text_holder1.markdown("<h3 style='text-align: left; color: blue;'>Plasma is Contracting in Upward Direction!</h3>",unsafe_allow_html=True)
                    elif ((UP==0) and (DOWN<0)):
                        text_holder1.markdown("<h3 style='text-align: left; color: blue;'>Plasma is Contracting in Upward Direction!</h3>",unsafe_allow_html=True)
                    elif (UP<0) and (DOWN<0):
                        text_holder1.markdown("<h3 style='text-align: left; color: blue;'>Plasma is Contracting Vertically!</h3>",unsafe_allow_html=True)
                    elif (UP>0) and (DOWN<=0):
                        text_holder1.markdown("<h3 style='text-align: left; color: blue;'>Plasma is Moving Up!</h3>",unsafe_allow_html=True)
                    elif (UP<=0) and (DOWN>0):
                        text_holder1.markdown("<h3 style='text-align: left; color: blue;'>Plasma is Moving Down!</h3>",unsafe_allow_html=True)

                    if (LEFT>0) and (RIGHT>0):
                        text_holder3.markdown("<h3 style='text-align: left; color: blue;'>Plasma is Expanding Horizontally!</h3>",unsafe_allow_html=True)
                    elif ((LEFT>0) and (RIGHT==0)):
                        text_holder3.markdown("<h3 style='text-align: left; color: blue;'>Plasma is Expanding in Left Direction!</h3>",unsafe_allow_html=True)
                    elif ((LEFT==0) and (RIGHT>0)):
                        text_holder3.markdown("<h3 style='text-align: left; color: blue;'>Plasma is Expanding in Right Direction!</h3>",unsafe_allow_html=True)
                    elif ((LEFT<0) and (RIGHT==0)):
                        text_holder3.markdown("<h3 style='text-align: left; color: blue;'>Plasma is Contracting in Left Direction!</h3>",unsafe_allow_html=True)
                    elif ((LEFT==0) and (RIGHT<0)):
                        text_holder3.markdown("<h3 style='text-align: left; color: blue;'>Plasma is Contracting in Right Direction!</h3>",unsafe_allow_html=True)
                    elif (LEFT<0) and (RIGHT<0):
                        text_holder3.markdown("<h3 style='text-align: left; color: blue;'>Plasma is Contracting Horizontally!</h3>",unsafe_allow_html=True)
                    elif (LEFT>0) and (RIGHT<=0):
                        text_holder3.markdown("<h3 style='text-align: left; color: blue;'>Plasma is Moving Left!</h3>",unsafe_allow_html=True)
                    elif (LEFT<=0) and (RIGHT>0):
                        text_holder3.markdown("<h3 style='text-align: left; color: blue;'>Plasma is Moving Right!</h3>",unsafe_allow_html=True)
                text_holder9.markdown("<h3 style='text-align: left; color: magenta;'>Plasma's velocity in + X dir. is "+str((upVel-downVel)/TimeFact)+" units/ms</h3>",unsafe_allow_html=True)
                text_holder10.markdown("<h3 style='text-align: left; color: magenta;'>Plasma's velocity in + Y dir. is "+str((rightVel-leftVel)/TimeFact)+" units/ms</h3>",unsafe_allow_html=True)

            imgB=np.multiply(((1/255)*np.ones(imgB.shape)),imgB)
            area=sum(sum(imgB))/totalPix
            text_holder4.markdown("<h3 style='text-align: left; color: maroon;'>Radiating Area: "+str(area)+"</h3>",unsafe_allow_html=True)
        else:
            text_holder.markdown("<h3 style='text-align: left; color: red;'>Plasma is not touching the surface!</h3>",unsafe_allow_html=True)
        time.sleep(0.8)
        text_holder.text("")
        text_holder1.text("")
        text_holder2.text("")
        text_holder3.text("")
        text_holder4.text("")
        text_holder5.text("")