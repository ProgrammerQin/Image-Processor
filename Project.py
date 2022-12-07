# -*- coding: utf-8 -*-
"""
Created on Tue Nov 15 23:10:13 2022
@author: Group G
"""
import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror
from tkinter.messagebox import showinfo
from tkinter import simpledialog 
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import cv2,datetime,os,glob,img2pdf,warnings
# from skimage import exposure


window = tk.Tk()
window["bg"] = "#5F87FF"
window.geometry('270x590')#Size of the GUI window
window.resizable(True,True)#Prevent the window from getting resized
window.title('Image Processing')#define the title of the window
warnings.simplefilter("ignore")#Show warning

def load_img(event=None): #Image load function
    global read_img #Global variable
    ask_img = askopenfilename(filetypes=[("files type",".jpg")])#Ask user to select the image
    if ask_img: #if ask image is loaded
        try:
            showinfo(title='Image Uploaded',message = ask_img+' has been uploaded!') #show selected image
        except:
            showerror(title='Error',message="Unable to load the image!")#Show Error if iamge is unable to load
        
    read_img = mpimg.imread(ask_img)#Read image provided by the user
    plt.show() #plot the image
    return read_img #Return the image veriable
def hist(): #Histogram function
    if load_img: #Check if the image is loaded
        try:
            img = read_img #Read the return image veriable
            fig = plt.figure() #Plot figure function 
            plt.hist(img.ravel(),bins=256) #Plot the image histogram
            plt.title("\nHistogram Processing\n") #plot title
            plt.show() #Show plot
            fig.savefig('out_1.jpg',dpi = 200) #Save the image into JPG format
        except:
            #Show error if the image is not loaded
            showerror(title='Error',message="Please upload the image first and then try again!")
def contrast(): #Improve contract function
    if load_img: #Check if the image is loaded
        try:
            img = read_img #Read the return image veriable
            img_eq = exposure.equalize_hist(img) #Histogram equalizer to improve contract 
            fig = plt.figure() #Plot figure function
            #Plot orignal and improved images side by side
            plt.subplot(121),plt.imshow(img, 'gray'),plt.title("Histogram Equlizer Processing\n\nOrignal")
            plt.subplot(122),plt.imshow(img_eq, 'gray'),plt.title("Improved Contrast")
            plt.show() #Show iamge
            fig.savefig('out_2.jpg',dpi = 200)# Save the image
        except:
            #Show error if the image is not loaded
            showerror(title='Error',message="Please upload the image first and then try again!")

def pix(): #pixels results function
    if load_img:#Check if the image is loaded
        try:
            img = read_img #Read the return image veriable
            fig = plt.figure() #Plot figure function
            plt.imshow(img) #Plot the image
            plt.title(f'{"Image Pixels Processing %s"}\n' % (np.shape(img),)) #Image title with Pixels result
            plt.show() #Show plot function
            fig.savefig('out_3.jpg',dpi = 200)# Save the Image
        except:
            #Show error if the image is not loaded
            showerror(title='Error',message="Please upload the image first and then try again!")

def grayscale():#grayscale function
    if load_img:#Check if the image is loaded
        try:
            img = read_img #Read the return image veriable
            fig = plt.figure() #Plot figure function
            red_channel =  img[:,:,0] #Read the red channel of the loaded image 
            green_channel = img[:,:,1] #Read the green channel of the loaded image 
            blue_channel =  img [:,:,2] #Read the blue channel of the loaded image 
            gray_image = 0.2989 * red_channel + 0.5870 *green_channel + 0.1140 * blue_channel #Convert into Gray image
            #Plot orignal and gray images side by side
            plt.subplot(121),plt.imshow(img, 'gray'),plt.title("Gray Scalling Image Processing\n\nOrignal")
            plt.subplot(122),plt.imshow(gray_image, 'gray'),plt.title("Gray Image")
            plt.show() #Show plot function
            fig.savefig('out_4.jpg',dpi = 200) #Save the image into JPG format
        except IndexError:
            #Show info if image is already Gray
            showinfo(title='Gray Image',message="The Image is already Gray!")
        except:
            #Show error if the image is not loaded
            showerror(title='Error',message="Please upload the image first and then try again!")

def noise(): #noise removal function
    if load_img:#Check if the image is loaded
        try:
            img = read_img #Read the return image veriable
            fig = plt.figure() #Plot figure
            if(len(img.shape)<3): #Check if image is Gray
                dst = cv2.fastNlMeansDenoising(img,None,10,7,21)#Noise removal function for gray image
                #Plot orignal and noise removal images side by side
                plt.subplot(121),plt.imshow(img, 'gray'),plt.title("Image Noise Removal Processing\n\nOrignal")
                plt.subplot(122),plt.imshow(dst, 'gray'),plt.title("Noise_Removal")
                plt.show() #Show plot function
                fig.savefig('out_5.jpg',dpi = 200)#Save the image into JPG format 
            
            elif len(img.shape)==3: # Check if the iamge is color
                dst = cv2.fastNlMeansDenoisingColored(img,None,10,10,7,21)#Noise removal function for color image
                #Plot orignal and noise removal images side by side
                plt.subplot(121),plt.imshow(img, 'gray'),plt.title("Image Noise Removal Processing\n\nOrignal")
                plt.subplot(122),plt.imshow(dst, 'gray'),plt.title("Noise_Removal")
                plt.show() #Show plot function
                fig.savefig('out_6.jpg',dpi = 200) #Save the image into JPG format
        except cv2.error:
            #Show the info if the image is 
            showinfo(title='Noiseless Image',message="The Image is already noiseless!")
        except:
            #Show error if the image is not loaded 
            showerror(title='Error',message="Please upload the image first and then try again!")

def img_thr(): #Binary thresh holding function
        # Ask user to input the first binary number from 0-255
        x = simpledialog.askinteger("Input", "Enter first Binary Number from 0-255")
        # Ask user to input the first binary number from 0-255
        y = simpledialog.askinteger("Input", "Enter second Binary Number from 0-255")
        img = read_img #Read the return image veriable
        fig = plt.figure() #Plot figure function
        ret,thresh1 = cv2.threshold(img,x,y,cv2.THRESH_BINARY) #image thresh holding process
        #Images titels
        titles = ['Image Binary Thresholding Processing\n\nOriginal Image','Binary Thresholding']
        images = [img, thresh1]#concatenate the orginal and thresh hold image 
        for i in range(2):#for loop to plot both images
             plt.subplot(1,2,i+1),plt.imshow(images[i],'gray')#plot both image side by side
             plt.title(titles[i])#Add the titels to the plot
        plt.show()#Show plot function
        fig.savefig('out_7.jpg',dpi = 200)#Save the image into JPG format

def sketch(): #Pencile sketch function
    if load_img:#Check if the image is loaded
        try:
            img = read_img #Read the return image veriable
            fig = plt.figure() #Plot figure function
            gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #convert image to gray
            inverted_gray_image = 255 - gray_image #invert the gray image
            blurred_img = cv2.GaussianBlur(inverted_gray_image, (21,21),0)# convert gray imge to gaussian blur
            inverted_blurred_img = 255 - blurred_img #invert the Gaussian blur image
            #Convert inverted gaussian blur image to pencile sketch 
            pencil_sketch_IMG = cv2.divide(gray_image, inverted_blurred_img, scale = 256.0) 
            #Plot orignal and pencile sketch images side by side
            plt.subplot(121),plt.imshow(img, 'gray'),plt.title("Pancile Sketch Processing\n\nOrignal")
            plt.subplot(122),plt.imshow(pencil_sketch_IMG, 'gray'),plt.title("Pencil Sketch")
            plt.show() #Show plot function
            fig.savefig('out_8.jpg',dpi = 200)#Save the image into JPG format
        except cv2.error:
            #Show the error if the image is Gray
            showerror(title='Gray Image',message="Pencile sketch function is not for Gray images!")
        except:
            #Show error if the image is not loaded 
            showerror(title='Error',message="Please upload the image first and then try again!") 

def watermark(): #Watermark removal function
    if load_img: #Check if the image is loaded
        try:
            img = read_img #Read the return image veriable
            fig = plt.figure() #Plot figure function
            ret,thresh1 = cv2.threshold(img,127,255,cv2.THRESH_BINARY)#Add binary thresh hold to the image
            #Titles for orignal and watermark remved image
            titles = ['Watermark Removal Processing\n\nOriginal Image','Watermark Removed']
            images = [img, thresh1]#concatenate the orginal and thresh hold image           
            for i in range(2):#for loop to plot both images
                 plt.subplot(1,2,i+1),plt.imshow(images[i],'gray')#plot both image side by side
                 plt.title(titles[i])#Add the titels to the plot
            plt.show()#Show plot function
            fig.savefig('out_9.jpg',dpi = 200)#Save the image into JPG format
        except:
            #Show error if the image is not loaded 
            showerror(title='Error',message="Please upload the image first and then try again!")
def save():#Images save into PDF function
    try:
        #Save the images into PDG format file name output with date and time stamp
        with open("output"+datetime.datetime.now().strftime("%Y-%m-%d_%I-%M-%S_%p")+".pdf", 'wb') as f:
            #Store JPG images into PDF format function
            f.write(img2pdf.convert(sorted([i for i in os.listdir('.')
        if i.endswith(".jpg")]))) #Check all the images with JPG format
        #Show info that images iamges saved into PDF file
        showinfo(title='Images Saved to PDF',message ='Images has been saved to PDF file successfully!')
    #Show error if there is no image to save
    except ValueError: showinfo(title='No Image found',message="There is no image to save!")       
def remove():#jpg remove function
    for f in glob.glob("out_*"):#For loop to select all the JPG image named with out_
        os.remove(f)#Remove the result of for loop
def close():#Program close function
    for f in glob.glob("out_*"):#For loop to select all the JPG image named with out_
        os.remove(f)#Remove the result of for loop
    window.destroy()#Close the GUI window function
window.protocol("WM_DELETE_WINDOW", close)#Close the GUI window by clicking x on the GUI window    

# function to change properties of button on hover
def changeOnHover(button, colorOnHover, colorOnLeave):
	# adjusting backgroung of the widget
	# background on entering widget
	button.bind("<Enter>", func=lambda e: button.config(background=colorOnHover))
	# background color on leving widget
	button.bind("<Leave>", func=lambda e: button.config(background=colorOnLeave))
    
#Upload image button initiate the Load_img function when pressed
upload_btn = tk.Button(window, text='Upload  Image',command = load_img,width=17,
                           bg='#AFD7FF',font =('calibri', 12))
upload_btn.pack(pady=10)
changeOnHover(upload_btn, "red", "#AFD7FF")

#Show histogram button initiate the Histogram function when pressed
hist_btn = tk.Button(window, text='Show Histrogram',command = hist,width=17,
                     bg='#AFD7FF',font =('calibri', 12))
hist_btn.pack(pady=10)
changeOnHover(hist_btn, "red", "#AFD7FF")
#Improve contrast button initiate the Contrast function when pressed
hist_equ_btn = tk.Button(window, text='Improve Contrast',command = contrast,width=17,
                       bg='#AFD7FF',font =('calibri', 12))
hist_equ_btn.pack(pady=10)
changeOnHover(hist_equ_btn, "red", "#AFD7FF")

#Show pixels button initiate the Pixel function when pressed
pix_btn = tk.Button(window, text='Show Image Pixels',command= pix,width=17,
                       bg='#AFD7FF',font =('calibri', 12))
pix_btn.pack(pady=10)
changeOnHover(pix_btn, "red", "#AFD7FF")

#Gray scale button initiate the Grayscale function when pressed
grayscale_btn = tk.Button(window, text='Gray Scale',command = grayscale,width=17,
                       bg='#AFD7FF',font =('calibri', 12))
grayscale_btn.pack(pady=10)
changeOnHover(grayscale_btn, "red", "#AFD7FF")

#Noise removal button initiate the Noise function when pressed
noise_btn = tk.Button(window, text='Noise Removal',command = noise,width=17,
                       bg='#AFD7FF',font =('calibri', 12))
noise_btn.pack(pady=10)
changeOnHover(noise_btn, "red", "#AFD7FF")

#Binary thresh hold button initiate the Img_thr function when pressed
img_thr_btn = tk.Button(window, text='Image Threshholding',command = img_thr,width=17,
                       bg='#AFD7FF',font =('calibri', 12))
img_thr_btn.pack(pady=10)
changeOnHover(img_thr_btn, "red", "#AFD7FF")

#Pencile sketch button initiate the Sketch function when pressed
sketch_btn = tk.Button(window, text='Pencil Sketch',command = sketch,width=17,
                       bg='#AFD7FF',font =('calibri', 12))
sketch_btn.pack(pady=10)
changeOnHover(sketch_btn, "red", "#AFD7FF")

#Watermark removal button initiate the Watermark function when pressed
watermark_btn = tk.Button(window, text='Watermark Remove',command = watermark,width=17,
                       bg='#AFD7FF',font =('calibri', 12))
watermark_btn.pack(pady=10)
changeOnHover(watermark_btn, "red", "#AFD7FF")

#Save image to PDF button initiate the save and remove function simultaneously when pressed
save_btn = tk.Button(window, text='Save Images as PDF',command = lambda:[save(),remove()],width=17,
                       bg='#AFD7FF',font =('calibri', 12))
save_btn.pack(pady=10)
changeOnHover(save_btn, "red", "#AFD7FF")

#Close program button initiate the close and remove function simultaneously when pressed
close_btn = tk.Button(window, text='Close  Program',command =lambda:[close(),remove()],width=17,
                       bg='#AFD7FF',font =('calibri', 12))
close_btn.pack(pady=10)
changeOnHover(close_btn, "red", "#AFD7FF")

window.mainloop()#Main GUI window close loop function
