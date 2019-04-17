import io
import os
import datetime
import time
import Tkinter as tk
from PIL import Image, ImageTk
# from google.cloud import storage

# config values
touch_screen_size = "800x480"
main_menu_font = 'Helvetica 17 bold'

# create main window
main_window = tk.Tk()
main_window.title('Image Capture Helper')
main_window.geometry(touch_screen_size)

## define button functions ##

def new_window_capture():
    capture_window = tk.Toplevel(main_window)
    capture_window.title('Capture Window')
    capture_window.geometry(touch_screen_size)

    capture_buttons = []
    pose_buttons = []

    for x in range(1,17):
        capture_buttons.append(tk.Button(capture_window, text='Capture Image '+str(x), height=3,width=15,command=(lambda x=x: capture_image(x))))

    for x in range(1,5):
        pose_buttons.append(tk.Button(capture_window, text='Capture Pose '+str(x), font='Helvetica 14 bold', height=4, width=15, command=(lambda x=x: capture_pose(x))))
        pose_buttons[x-1].grid(column=x-1, row=0)

    for x in range(16):
        capture_buttons[x].grid(column=x/4, row=x%4+1)

    capture_back = tk.Button(capture_window, text='Close Window', height=3,width=16,command=capture_window.destroy)
    capture_back.grid(column=0,row=5)

def new_window_check():
    check_window = tk.Toplevel(main_window)
    check_window.title('Check Window')
    check_window.geometry(touch_screen_size)

    check_buttons = []
    for x in range(1,17):
        check_buttons.append(tk.Button(check_window, text='Check Image '+str(x), height=4,width=18,command=(lambda x=x: check_image(x))))

    for x in range(16):
        check_buttons[x].grid(column=x/4,row=x%4)

    check_back = tk.Button(check_window, text='Close Window', height=4,width=18,command=check_window.destroy)
    check_back.grid(column=0,row=4)

def capture_pose(pose_num):
    first_photo = (pose_num-1)*4+1
    last_photo = (pose_num-1)*4+4
    try:
        print "captured images " + str(first_photo) + " to " + str(last_photo)
        for x in range(first_photo,last_photo+1):
            camera_select = (x-1)%4
            filename = "/home/pi/webcam/cam" + str(x) + ".jpg"
            print "filename is ", filename, " camera select is ", camera_select
            # os.system("fswebcam -d /dev/video0 -r 1920x1080 -S 5 -q --no-banner "+filename)
    except:
        print "failed to capture pose"

def capture_image(img_num):

    camera_select = (img_num-1)%4
    filename = "/home/pi/webcam/cam" + str(img_num) + ".jpg"
    print "filename is ", filename, " camera select is ", camera_select

    # image capture command
    try:
        os.system("fswebcam -d /dev/video0 -r 1920x1080 -S 5 -q --no-banner "+filename)
    except:
        print "capture failed"

def check_image(img_num):
    real_num = (img_num-1)%4+1
    print "really displaying", real_num
    path = "/home/pi/webcam/cam" + str(real_num) + ".jpg"

    # create image window
    image_window = tk.Toplevel(main_window)
    image_window.title('Image'+str(img_num))
    image_window.geometry(touch_screen_size)

    try:
        # open image
        loaded_img = ImageTk.PhotoImage(Image.open(path).resize((600,480),Image.ANTIALIAS))
        # place image on canvas (left side of screen)
        img_canvas = tk.Canvas(image_window,width=800,height=480)
        img_canvas.grid(row=0,column=0)
        img_canvas.create_image(0,0,image=loaded_img,anchor="nw")
        img_canvas.image = loaded_img
    except:
        print "image viewer failed"

    # create back button
    back_button = tk.Button(image_window, text='Close Window', height=4,width=20,command=image_window.destroy)
    back_button.place(x=600,y=200)
    image_window.mainloop()

def upload_images():
    try:
        firebase_upload()
        upload_window = tk.Toplevel(main_window)
        upload_window.title('Upload Window')
        upload_window.geometry(touch_screen_size)
        upload_message = "Upload Success! Touch to Return Back"
        upload_destroy = tk.Button(upload_window, text=upload_message, font = main_menu_font, height=18, width=60,command=upload_window.destroy).pack()
    except:
        print "error in uploading images"

button_capture = tk.Button(main_window, text='Capture Images', font=main_menu_font, height=4, width=40, command =(lambda: new_window_capture())).pack()
button_check = tk.Button(main_window, text='Check Images', font=main_menu_font, height=4, width=40, command=(lambda: new_window_check())).pack()
button_upload = tk.Button(main_window, text='Upload Images',font=main_menu_font, height=4, width=40, command=(lambda: upload_images())).pack()

main_window.mainloop()

def firebase_upload():

    PROJECT_ID = 'BME590Project'
    CLOUD_STORAGE_BUCKET = 'bme590project.appspot.com'

    for x in range(16):
        filename = "/home/pi/webcam/cam" + str(x+1) + ".jpg"
        client = storage.Client(project=PROJECT_ID)
        bucket = client.bucket(CLOUD_STORAGE_BUCKET)
        blob = bucket.blob(filename)
        with open(filename, "rb") as fp:
           try:
               blob.upload_from_file(fp)
           except:
               print "firebase upload failed"
