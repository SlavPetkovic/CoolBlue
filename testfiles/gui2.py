# Importing dependencies
import tkinter
import tkinter.messagebox
import customtkinter

# Setting up theme
customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Cool Blue")
        self.geometry(f"{1200}x{700}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame for controls
        self.sidebar_frame = customtkinter.CTkFrame(self, width=200)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, padx=(5, 5), pady=(10, 10), sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Controls",  font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=1, padx=20, pady=(10, 10))
        self.button_up = customtkinter.CTkButton(self.sidebar_frame, text="W", height=10, width=10, command=self.motion_event)
        self.button_up.grid(row=1, column=1, padx=20, pady=10, ipadx=10, ipady=10)
        self.button_down = customtkinter.CTkButton(self.sidebar_frame, text="S", height=10, width=10, command=self.motion_event)
        self.button_down.grid(row=3, column=1, padx=20, pady=10, ipadx=10, ipady=10)
        self.button_left = customtkinter.CTkButton(self.sidebar_frame, text="A", height=10, width=10, command=self.motion_event)
        self.button_left.grid(row=2, column=0, padx=10, pady=10, ipadx=10, ipady=10)
        self.button_right = customtkinter.CTkButton(self.sidebar_frame, text="D", height=10, width=10, command=self.motion_event)
        self.button_right.grid(row=2, column=2, padx=10, pady=10, ipadx=10, ipady=10)
        self.button_stop = customtkinter.CTkButton(self.sidebar_frame, text="Stop", height=10, width=10, command=self.motion_event)
        self.button_stop.grid(row=2, column=1, padx=10, pady=10, ipadx=10, ipady=10)

        # create Video Canvas
        self.picam = customtkinter.CTkCanvas(self, width=800, background="gray")
        self.picam.grid(row=0, column=1, rowspan=2, padx=(5, 5), pady=(20, 20), sticky="nsew")
        self.picam_label = customtkinter.CTkLabel(master=self.picam, text="Live Video", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.picam_label.grid(row=0, column=2, columnspan=1, padx=10, pady=10, sticky="")

        # create sidebar frame for Environmental Variable
        self.measurements = customtkinter.CTkFrame(self, width=200)
        self.measurements.grid(row=0, column=3, rowspan=4, padx=(5, 5), pady=(10, 10), sticky="nsew")
        self.measurements.grid_rowconfigure(4, weight=1)
        self.label_measurements = customtkinter.CTkLabel(master=self.measurements, text="Environment:", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.label_measurements.grid(row=0, column=2, columnspan=1, padx=10, pady=10, sticky="")

        clicked = self.button_up

    def motion_event(self):
        if self.button_up == clicked:
            print("Forward")
        elif self.button_down == clicked:
            print("Backward")
        elif self.button_left == clicked:
            print("Left")
        elif self.button_right == clicked:
            print("Right")
        elif self.button_stop == clicked:
            print("Stop")




        # if button_up pressed down or physical key "w" on keyboard pressed and held down, print "w" until key released or button not being clicked anymore.
        # else if button_down pressed down or physical key "s" on keyboard pressed and held down, print "s" until key released or button not being clicked anymore.
        # else if button_left pressed down or physical key "a" on keyboard pressed and held down, print "a" until key released or button not being clicked anymore.
        # else if button_right pressed down or physical key "d" on keyboard pressed and held down, print "d" until key released or button not being clicked anymore.


if __name__ == "__main__":
    app = App()
    app.mainloop()