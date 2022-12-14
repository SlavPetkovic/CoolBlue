# -*- coding: utf-8 -*-
# Created i La Selva 18-mars-04 15:15
# Modified i La Selva 19-Januari-07  16:40

from PIL import Image, ImageTk
import Tkinter as tk
import argparse
import time
import datetime
import cv2
import os
import re
import shutil
import smtplib
import subprocess
import urllib
import RPi.GPIO as GPIO
import threading
import picamera

from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders
from email.mime.image import MIMEImage

fromaddr = "xxxxxxxxxxxxxxxxxx@gmail.com"
toaddr = "xxxxxxxxxxxxxxxxxx@gmail.com"
mailpass = "xxxxxxxxxxxxxxx"

device = "TEST_Kam "

path = "/home/pi/"
moveto = "/home/pi/Pictures/saved/"

bilder = "noimage.jpg"
flag = 0
delete_flag = 0

os.system("sudo modprobe bcm2835-v4l2")  # to recognize PiCamera as video0


def do_picam(app):
    global shot
    global texte
    global texmed
    global delete_flag
    global txt_display
    camera = picamera.PiCamera()
    # camera.awb_mode = 'auto'
    camera.brightness = 50
    # camera.rotation= 90
    camera.resolution = (2592, 1944)
    data = time.strftime("%y-%b-%d_(%H%M%S)")
    texte = "picture take at: " + data
    camera.start_preview()
    camera.capture('%s.jpg' % data)
    camera.stop_preview()
    camera.close()  # close Picamera to free resources  to restart the video stream
    shot = '%s.jpg' % data
    dagtid = time.strftime("%y-%b-%d (%H:%M)")
    texte = "picture take:" + time.strftime("%y-%b-%d_(%H%M%S)")
    texmed = device + dagtid
    app.showImg()
    app.textBox.delete("1.0", tk.END)
    app.textBox.insert(tk.END, shot)
    app.textBox.configure(bg="dodgerblue")
    app.textBox.update_idletasks()
    delete_flag = 1
    app.vs.open(0)  # restarting video stream from Pi Camera
    app.enable_buttons()
    txt_display = " " + shot[0:18]


def do_sendMail(app):
    mail = MIMEMultipart()
    mail['Subject'] = str(texmed)
    mail['From'] = fromaddr
    mail['To'] = toaddr
    mail.attach(MIMEText(texte, 'plain'))

    attachment = open(shot, 'rb')
    image = MIMEImage(attachment.read())
    attachment.close()
    mail.attach(image)
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, mailpass)
    text = mail.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()
    app.textBox.delete("1.0", tk.END)
    app.textBox.insert(tk.END, txt_display + "  MAILED OK")
    app.textBox.update_idletasks()
    app.enable_buttons()


class Application:
    def __init__(self, output_path="./"):
        """ Initialize application which uses OpenCV + Tkinter. It displays
            a video stream in a Tkinter window and stores current snapshot on disk """
        self.vs = cv2.VideoCapture(0)  # capture video frames, 0 is your default video camera
        self.output_path = output_path  # store output path
        self.current_image = None  # current image from the camera
        self.root = tk.Tk()  # initialize root window
        defaultbg = self.root.cget('bg')  # set de default grey color to use in labels background
        w = 930  # width for the Tk root
        h = 535  # height for the Tk root
        self.root.resizable(0, 0)
        ws = self.root.winfo_screenwidth()  # width of the screen
        hs = self.root.winfo_screenheight()  # height of the screen
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        self.root.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.root.title("     LA  SELVA - REMOT VIDEO SNAP SHOT     ")  # set window title
        self.root.protocol('WM_DELETE_WINDOW', self.destructor)

        self.panel = tk.Label(self.root)  # initialize image panel
        self.panel.grid(row=0, rowspan=15, column=8, columnspan=25, padx=4, pady=6)

        self.labPic = tk.Label(self.root, bg="grey70")  # initialize image panel
        self.labPic.grid(row=5, column=34, padx=4, pady=6)

        self.textBox = tk.Text(self.root, height=1, width=28, font=('arial narrow', 10, 'bold'), bg="green", fg="white")
        self.textBox.grid(row=6, rowspan=2, column=34, padx=3)
        self.textBox.insert(tk.END, "READY")

        self.botMail = tk.Button(self.root, width=25, font=('arial', 12, 'normal'), text="SEND PICTURE BY MAIL",
                                 activebackground="#00dfdf")
        self.botMail.grid(row=8, column=34, pady=1)
        self.botMail.configure(command=self.sendMail, state="disabled")

        self.botRadera = tk.Button(self.root, width=25, font=('arial', 12, 'normal'), text="DELETE PICTURE",
                                   activebackground="#00dfdf")
        self.botRadera.grid(row=9, column=34, pady=1)
        self.botRadera.configure(command=self.radera, state="disabled")

        self.botSave = tk.Button(self.root, width=25, font=('arial', 12, 'normal'), text="SAVE PICTURE",
                                 activebackground="#00dfdf")
        self.botSave.grid(row=10, column=34, pady=1)
        self.botSave.configure(command=self.movepic, state="disabled")

        self.botShoot = tk.Button(self.root, width=24, font=('arial', 14, 'normal'), text="PICAM-SHOOT",
                                  activebackground="#00dfdf")
        self.botShoot.grid(row=15, column=20)
        self.botShoot.configure(command=self.picam)

        self.botQuit = tk.Button(self.root, width=6, font=('arial narrow', 14, 'normal'), text="CLOSE",
                                 activebackground="#00dfdf")
        self.botQuit.grid(row=15, column=32)
        self.botQuit.configure(command=self.destructor)
        self.video_loop()

    def video_loop(self):
        global test
        global flag
        """ Get frame from the video stream and show it in Tkinter """
        ok, frame = self.vs.read()  # read frame from video stream
        if ok:  # frame captured without any errors
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)  # convert colors from BGR to RGBA
            self.current_image = Image.fromarray(cv2image)  # convert image for PIL
            imgtk = ImageTk.PhotoImage(image=self.current_image)  # convert image for tkinter
            test = cv2image
            self.panel.imgtk = imgtk  # anchor imgtk so it does not be deleted by garbage-collector
            self.panel.config(image=imgtk)  # show the image

        self.root.after(30, self.video_loop)  # call the same function after 30 milliseconds
        if flag == 0:
            flag = 1
            self.show_thumb()

    def snapshot(self):
        imageName = 'cv-' + time.strftime("%Y-%b-%d_(%H%M%S)") + '.jpg'
        cv2.imwrite(imageName, test)

    def picam(self):
        self.disable_buttons()
        self.vs.release()  # release the camera to get all resources
        t = threading.Thread(target=do_picam, args=(self,))
        t.start()

    def showImg(self):
        image = Image.open(shot)
        image = image.resize((252, 195), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(image)
        self.labPic.configure(image=photo)
        self.labPic.image = photo
        self.root.update_idletasks()

    def show_thumb(self):
        image = Image.open(bilder)
        image = image.resize((252, 195), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(image)
        self.labPic.configure(image=photo)
        self.labPic.image = photo
        self.root.update_idletasks()

    def sendMail(self):
        t = threading.Thread(target=do_sendMail, args=(self,))
        t.start()
        self.disable_buttons()
        self.textBox.delete("1.0", tk.END)
        self.textBox.insert(tk.END, "SENDING PICTURE BY MAIL")
        self.textBox.update_idletasks()

    def movepic(self):
        global delete_flag
        pic = shot
        src = path + pic
        dst = moveto + pic
        shutil.move(src, dst)
        self.textBox.delete("1.0", tk.END)
        self.textBox.insert(tk.END, txt_display + "   SAVED")
        self.textBox.configure(bg="darkorange")
        self.textBox.update_idletasks()
        self.botMail.configure(state="disabled")
        self.botSave.configure(state="disabled")
        self.botRadera.configure(state="disabled")
        delete_flag = 2

    def radera(self):
        global delete_flag
        pic = shot
        os.remove(pic)
        self.textBox.delete("1.0", tk.END)
        self.textBox.insert(tk.END, txt_display + "  DELETED ")
        self.textBox.configure(bg="red")
        self.textBox.update_idletasks()
        delete_flag = 2
        self.botMail.configure(state="disabled")
        self.botSave.configure(state="disabled")
        self.botRadera.configure(state="disabled")

    def disable_buttons(self):
        self.botShoot.configure(state="disabled")
        self.botMail.configure(state="disabled")
        self.botSave.configure(state="disabled")
        self.botRadera.configure(state="disabled")
        self.botQuit.configure(state="disabled")

    def enable_buttons(self):
        self.botShoot.configure(state="normal")
        self.botMail.configure(state="normal")
        self.botSave.configure(state="normal")
        self.botRadera.configure(state="normal")
        self.botQuit.configure(state="normal")

    def destructor(self):
        if delete_flag == 1: self.radera()
        self.root.destroy()
        self.vs.release()  # release web camera
        cv2.destroyAllWindows()  # it is not mandatory in this application


# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-o", "--output", default="./Pictures",
                help="path to output directory to store snapshots (default: current folder")
args = vars(ap.parse_args())

# start the app
pba = Application(args["output"])
pba.root.mainloop()







