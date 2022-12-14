import tkinter
import tkinter.messagebox
import customtkinter
from PIL import Image,ImageTk
import cv2


# Setting up theme of GUI
customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.is_on = True
        self.image = ImageTk.PhotoImage(Image.open("../data/Mars.PNG"))
        self.capture = cv2.VideoCapture(6)

        self.title("Cool Blue")
        self.geometry(f"{1200}x{635}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2, 3), weight=0)

        ###################################################################
        # Create Sidebar for LED, LIghts and Camera controls
        ###################################################################
        self.lights_control = customtkinter.CTkFrame(self)
        self.lights_control.grid(row=3, column=0, rowspan = 1, padx=(5, 5), pady=(10, 10), sticky="nsew")
        self.lights_control.grid_rowconfigure(1, weight=1)

        # Camera
        self.camera_switch = customtkinter.CTkSwitch(master=self.lights_control, text="Camera", command=self.camera_switch)
        self.camera_switch.grid(row=2, column=1, pady=10, padx=20, )

        ###################################################################
        # Create canvas for RPCam live stream
        ###################################################################
        self.picam_frame = customtkinter.CTkFrame(self)
        self.picam_frame.grid(row=0, column=1, rowspan=4, padx=(5, 5), pady=(10, 10), sticky="nsew")
        self.picam_frame.grid_rowconfigure(4, weight=1)

        # self.picam_canvas = tkinter.Canvas(self.picam_frame, width=1730, height=944)
        # self.picam_canvas.pack()

        self.picam_label = customtkinter.CTkLabel(master=self.picam_frame)
        self.picam_label.grid(row=0, column=0)
        self.picam_label.pack()
        # self.picam_label.grid(row=0, column=1, columnspan=1, padx=10, pady=10, sticky="")


    #########################################################################
    # Camera Switch
    #########################################################################
    def camera_switch(self, event=None):
        if self.is_on:
            self.capture = cv2.VideoCapture(0)
            print("Cam on")
            self.is_on = False
            self.update_frames()
        else:
            self.close_camera()
            self.image
            print("Cam off")

            self.is_on = True

    def update_frames(self):

        # Change the frame by the initial image and breaks the loop
        if self.is_on:
            self.picam_label.image=self.image
            return
        else:

            _, frame = self.capture.read()

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        #frame = Image.fromarray(frame)
        #frame = ImageTk.PhotoImage(frame)

        img = Image.fromarray(frame)
        # Convert image to PhotoImage
        imgtk = customtkinter.CTkImage(img , size=(1280, 720))
        self.picam_label.imgtk = imgtk
        self.picam_label.configure(image=imgtk)

        self.picam_label.after(1, self.update_frames)
    def close_camera(self):
        self.capture.release()

if __name__ == "__main__":
    app = App()
    app.mainloop()