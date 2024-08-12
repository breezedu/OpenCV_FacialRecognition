#!/usr/bin/env python
# coding: utf-8

import cv2 as cv
import time
import datetime
import tkinter as tk
import os 
import pyttsx3 


def capture_image(target_path, cam):
    # Capture image using OpenCV 
    # Adding an extra cv.CAP_DSHOW could significantly improve the image capture time 
    cap = cv.VideoCapture(cam, cv.CAP_DSHOW)  # Replace 0 with your camera index 
    if not cap.isOpened():
        print("Camera does not response.")
        return "Camera_is_open"
    ret, frame = cap.read() 
    save_path = os.path.join( target_path, f"image_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg" ) 
    # print( "Save image to the path:") 
    print(save_path)
    if ret:
        cv.imwrite(save_path, frame)
    cap.release()
    return save_path 

def analyze_posture(image_path):
    # Load image and preprocess
    img = cv.imread(image_path)

    # Implement posture analysis logic using computer vision techniques
    # This is a complex task requiring advanced techniques
    # Potential libraries: OpenCV, TensorFlow, PyTorch
    # Example (placeholder):
    if is_sitting(img):
        return True
    else:
        return False

def is_sitting( image ):
    return True

def send_notification():
    # Play the following sound
    engine = pyttsx3.init()
    engine.setProperty('voice', 'com.apple.speech.synthesis.voice.samantha')
    text = "Hello, time to take a break, you have been sitting too long."
    engine.say(text)
    engine.runAndWait()
    # Create a Tkinter popup window
    root = tk.Tk()
    root.title("Posture Alert")
    root.geometry("1024x800")
    label = tk.Label(root, text="You've been sitting in front of the computer for too long! Take a break.")
    label.pack(pady=20)
    root.mainloop()



# In[8]:



def detect_person(image_path):
    """Detects if a person is present in the given image.

    Args:
        image_path (str): The path to the image file.

    Returns:
        bool: True if a person is detected, False otherwise.
    """
    if image_path == "Camera_is_open":
        return True

    # Load the pre-trained face detection model
    #face_cascade = cv.CascadeClassifier(cv.data.haarcascades + 'haarcascade_frontalface_default.xml') 
    face_cascade = cv.CascadeClassifier(os.path.join(os.getcwd(), 'haarcascade_frontalface_default.xml')) 
    body_cascade = cv.CascadeClassifier(os.path.join(os.getcwd(), 'haarcascade_upperbody.xml')) 
    eye_cascade  = cv.CascadeClassifier(os.path.join(os.getcwd(), 'haarcascade_eye_tree_eyeglasses.xml') )

    # Load the image
    img = cv.imread(image_path)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # Detect faces in the image
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    body  = body_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    eye   = eye_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    print("Faces: " + str( len(faces) ) + " Body: " + str( len(body) ) + " Eye: " + str( len(eye)) )

    # If any faces are detected, a person is present
    if len(faces) + len(body) + len(eye) > 0:
        return True
    else:
        return False


# In[9]:


# import os
# default_path = os.getcwd() 

def main():
    start_time = time.time() 
    sitting_time = 0 
    break_time = 0 
    target_path = os.path.join(os.getcwd(), "Pictures") 
    # if the path does not exit, create one: 
    if not os.path.exists(target_path):
        os.makedirs(target_path)
    
    # integer input
    print("Please select the camera, 0 for laptop default, 1 for extra camera:")
    cam_num = int(input()) 
    
    print("Please input how often you would like to take a break, every 60 mins?") 
    break_every_Xmin = int(input()) 
    
    print("Please input how long a break should take, 5-10 mins?") 
    break_min = int(input()) 
    
    while True:
        # target_path = os.path.join(os.getcwd(), "Pictures") 
        # if the path does not exit, create one: 
        
        image_path = capture_image( target_path, cam_num)    
                
        #if analyze_posture(image_path):
        if detect_person( image_path ):
            sitting_time = time.time() - start_time 
            print("The person has been sitting here for " + str(sitting_time) + " seconds." )
            
            if sitting_time >= break_every_Xmin*60:     # total sitting time more than 60 mins
                send_notification()
                sitting_time = 0
                start_time = time.time() 
        else:
            break_time += 1                #if no people detected, break_time plus 1 min 
            print( "The person just took a 1-min break.")
            if( break_time > break_min):   #if no people detected for a while, i.e. 10 mins, the person just took a break
                sitting_time = 0
                start_time = time.time() 
        time.sleep(60)  # 60 seconds per loop, take a photo every min;  
        
        # remove previously saved image
        if os.path.exists( image_path):
           os.remove( image_path) 
        print( str("you have been sitting there for: " + str(sitting_time )) )
        
        
if __name__ == "__main__":
    main()


# Example usage
# image_path = 'image_path'
#if detect_person(image_path):
#    print("Person detected in the image.")
#else:
#    print("No person detected in the image.")

