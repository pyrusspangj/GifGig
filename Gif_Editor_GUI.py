import math
import tkinter as tk
from tkinter import filedialog
from fractions import Fraction

import imageio

from Gif import Gif
from PIL import ImageTk
from GifEditor import GifEditor
import numpy as np
import cv2
from Design import Button
import re


class GifE:

    speed = 100
    adjustment_h, adjustment_w = 5, 5
    adjustment_speed = 5
    adjustment_text = 5
    font = "Imp"
    running = "None"
    fc = (255, 255, 255)
    saveto = "C:\\Users\\"
    name = "My_GifGab_Gif"
    displaying_frame = False
    ff, bf, sg = None, None, None


    def __init__(self):
        self.take_gif()
        self.open_gui()

    def browse_and_insert(self):
        file_path = tk.filedialog.askopenfilename(filetypes=[("GIF files", "*.gif")])
        if file_path:
            self.text_field.delete(0, tk.END)  # Clear the existing entry
            self.text_field.insert(0, file_path)  # Insert the selected path

    def clicked_setgif(self):
        self.path = self.text_field.get()
        self.root.destroy()
        self.GIF = Gif(self.path)
        self.frames = self.GIF.get_frames()
        self.add = self.GIF.gif_width()


    def reset(self):
        self.root.destroy()
        newgif = GifE()


    def take_gif(self):
        self.root = tk.Tk()
        self.root.title("Insert Gif")
        self.root.geometry("360x240")  # Increased the height to accommodate the button

        canvas = tk.Canvas(self.root, width=360, height=240)
        for y in range(480):
            shade = "#%02x%02x%02x" % (40, 0, 80 + int(160 * (y / 480)))
            canvas.create_line(0, y, 720, y, fill=shade)

        canvas.create_rectangle((360*0.5)-100, (240*0.2)-15, (360*0.5)+100, (240*0.2)+15, width=10)

        canvas.pack()

        self.browse_button = tk.Button(self.root, text="Browse GIF File", font=Button.standard, bg=Button.button_bg, command=self.browse_and_insert)
        self.browse_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=200)

        # Add a label above the text field with a transparent border
        label = tk.Label(self.root, text="Enter Gif Directory", font=("Arial", 18), bd=5, bg="gray",
                         highlightthickness=0, borderwidth=0)
        label.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

        # Create a text field with a transparent border
        self.text_field = tk.Entry(self.root, font=("Arial", 12), bg=canvas['background'], bd=0, highlightthickness=0,
                              highlightbackground=canvas['background'])
        self.text_field.place(relx=0.5, rely=0.65, anchor=tk.CENTER, width=250)

        # Add a cyan button underneath the text field
        cyan_button = tk.Button(self.root, text="Submit", font=("Arial", 14), bg="cyan", bd=0, command=self.clicked_setgif)
        cyan_button.place(relx=0.5, rely=0.8, anchor=tk.CENTER, width=120)


        self.root.mainloop()

    def open_gui(self):
        # Create the main application window
        self.root = tk.Tk()
        self.root.title("Gif Editor")
        self.x, self.y = int((720+(self.add/2))), int((480+(self.add/8)))
        self.root.geometry(f"{str(self.x)}x{str(self.y)}")
        self.root.resizable(width=False, height=False)

        self.max_dim = [self.x - (Button.constant * 3 + Button.spacing * 3 + 60), self.y-60]
        self.fs = int(min(self.GIF.gif_height() / 5.5, self.GIF.gif_width() / 5.5))

        # Calculate the coordinates for the expanded rectangle
        constant = 30
        #self.expanded_rectangle_x1 = constant - 5
        #self.expanded_rectangle_y1 = constant - 5
        #self.expanded_rectangle_x2 = self.GIF.gif_width() + constant + 10
        #self.expanded_rectangle_y2 = self.GIF.gif_height() + constant + 10

        # Create the rounded black rectangle
        self.canvas = tk.Canvas(self.root, width=self.x, height=self.y, highlightthickness=0)

        # Calculate the coordinates for the hollowed rectangle
        #self.hollowed_rectangle_x1 = 200
        #self.hollowed_rectangle_y1 = 120
        #self.hollowed_rectangle_x2 = self.GIF.gif_width() + constant
        #self.hollowed_rectangle_y2 = self.GIF.gif_height() + constant

        # Create the gradient background from darker purple to lighter purple
        for n in range(self.y):
            shade = "#%02x%02x%02x" % (40, 0, 80 + int(160 * (n / self.y)))
            self.canvas.create_line(0, n, self.x, n, fill=shade)

        #self.canvas.create_rectangle(self.expanded_rectangle_x1, self.expanded_rectangle_y1, self.expanded_rectangle_x2,
                                #self.expanded_rectangle_y2, outline="black", width=10)
        # Create the hollowed rectangle with a darker purple color
        #self.canvas.create_rectangle(self.hollowed_rectangle_x1, self.hollowed_rectangle_y1, self.hollowed_rectangle_x2,
                                #self.hollowed_rectangle_y2, outline="#400050", width=0)
        self.canvas.pack()

        #self.adset = Advanced_Settings(self.x, self.y, self.adjustment_w, self.adjustment_h, self.fs, self.adjustment_text, self.speed, self.adjustment_speed)

        self.my_menu = tk.Menu(self.root)

        self.file_menu = tk.Menu(self.my_menu)
        self.my_menu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="New", command=self.reset)
        self.file_menu.add_command(label="Save As", command=self.save_as)
        self.file_menu.add_command(label="Exit", command=self.root.destroy)

        self.settings_menu = tk.Menu(self.my_menu)
        self.my_menu.add_cascade(label="Advanced Settings", menu=self.settings_menu)
        self.settings_menu.add_command(label="Change Font Size", command=self.change_font_size)
        self.settings_menu.add_command(label="Change Font Color", command=self.change_font_color)
        self.settings_menu.add_command(label="Change Font", command=self.change_font)
        self.settings_menu.add_command(label="Change Duration", command=self.change_duration)
        self.settings_menu.add_command(label="Change Dimensions", command=self.change_in_dims)
        self.settings_menu.add_command(label="Add Text To Specified Frames", command=self.efbf)
        self.settings_menu.add_command(label="Add White Box & Text", command=self.add_white_box_and_text)

        self.root.config(menu=self.my_menu)

        self.rotate90clock = tk.Button(self.root, text="⟳", bg=Button.button_bg, font=Button.bold, bd=Button.base_bd, command=self.rotate_90_clock)
        self.rotate90clock.place(x=self.x - (Button.constant*3 + Button.spacing*2), y=Button.constant,
                            width=Button.but_w, height=Button.but_h)

        self.rotate90countclock = tk.Button(self.root, text="⟲", bg=Button.button_bg, font=Button.bold, bd=Button.base_bd, command=self.rotate_90_count_clock)
        self.rotate90countclock.place(x=self.x - (Button.constant*3 + Button.spacing), y=Button.constant,
                                 width=Button.but_w, height=Button.but_h)

        self.mirror_x = tk.Button(self.root, text="⇅", bg=Button.button_bg, font=Button.bold, bd=Button.base_bd, command=self.mirror_gif_across_x)
        self.mirror_x.place(x=self.x - (Button.constant*3 + Button.spacing*2), y = Button.constant + Button.spacing,
                                                         width = Button.but_w, height = Button.but_h)

        self.mirror_y = tk.Button(self.root, text="⇆", bg=Button.button_bg, font=Button.bold, bd=Button.base_bd, command=self.mirror_gif_across_y)
        self.mirror_y.place(x=self.x - (Button.constant*3 + Button.spacing), y = Button.constant + Button.spacing,
                       width=Button.but_w, height=Button.but_h)

        self.increase = tk.Button(self.root, text="↑", bg=Button.button_bg, font=Button.bold, bd=Button.base_bd, command=self.increase_size)
        self.increase.place(x=self.x - Button.constant*3, y=Button.constant,
                       width=Button.but_w, height=Button.but_h)

        self.decrease = tk.Button(self.root, text="↓", bg=Button.button_bg, font=Button.bold, bd=Button.base_bd, command=self.decrease_size)
        self.decrease.place(x=self.x - Button.constant*3, y=Button.constant + Button.spacing,
                            width=Button.but_w, height=Button.but_h)

        self.speedup = tk.Button(self.root, text="🐇", bg=Button.button_bg, font=Button.bold, bd=Button.base_bd, command=self.speed_up)
        self.speedup.place(x=self.x - (Button.constant*3 + Button.spacing*3), y=Button.constant,
                           width=Button.but_w, height=Button.but_h)

        self.slowdown = tk.Button(self.root, text="🐢", bg=Button.button_bg, font=Button.bold, bd=Button.base_bd,
                                 command=self.slow_down)
        self.slowdown.place(x=self.x - (Button.constant * 3 + Button.spacing * 3), y=Button.constant + Button.spacing,
                           width=Button.but_w, height=Button.but_h)

        self.submit_text = tk.Button(self.root, text="Submit Text", bg=Button.button_bg, font=("Arial, 15"), bd=Button.base_bd, command=self.add_text)
        self.submit_text.place(x=self.x - (248), y=Button.constant*11, width=150, height=50)

        self.rev = tk.Button(self.root, text="Reverse", bg=Button.button_bg, font=Button.standard,
                              bd=Button.base_bd, command=self.reverse_frames)
        self.rev.place(x=self.x - (248), y=Button.constant*13, width=150, height=50)

        self.top = tk.Entry(self.root, font=("Arial", 15), bg="gray", bd=7, highlightthickness=0,
                                   highlightbackground=self.canvas['background'])
        self.top.place(x=self.x - (173), y=Button.constant*7, anchor=tk.CENTER, width=250)

        self.mid = tk.Entry(self.root, font=("Arial", 15), bg="gray", bd=7, highlightthickness=0,
                            highlightbackground=self.canvas['background'])
        self.mid.place(x=self.x - (173), y=Button.constant*8.5, anchor=tk.CENTER, width=250)

        self.bot = tk.Entry(self.root, font=("Arial", 15), bg="gray", bd=7, highlightthickness=0,
                            highlightbackground=self.canvas['background'])
        self.bot.place(x=self.x - (173), y=Button.constant * 10, anchor=tk.CENTER, width=250)


        #GIF DISPLAYER {

        if not self.displaying_frame:
            # You need to create a list of PhotoImage instances for all frames
            self.tkinter_images = [tk.PhotoImage(data=frm) for frm in self.GIF.frames]

            # Set the initial frame to display
            self.current_frame = 0
            img = self.tkinter_images[self.current_frame]
            self.label = tk.Label(self.root, image=img)
            self.label.pack()
            self.label.place(x=30, y=30)

            self.root.after(self.speed, self.update_frame)

        #GIF DISPLAYER }
        self.root.mainloop()


    def add_text(self):
        top = self.top.get()
        mid = self.mid.get()
        bot = self.bot.get()
        size = self.fs
        font = self.font
        shape = [self.GIF.gif_width(), self.GIF.gif_height()]
        color = self.fc
        pil_im = GifEditor.tkinter_images_to_pillow(None, self.tkinter_images, shape[0], shape[1])
        self.frames = GifEditor.add_text(GifEditor, pil_im, top, mid, bot, size, font, shape, color)
        self.GIF.set_frames(self.frames)

        # Update the displayed frames on the GUI
        #print(type(self.frames[0]))
        self.update_displayed_frames()


    def reverse_frames(self):
        self.frames = self.frames[::-1]
        self.GIF.set_frames(self.frames)
        self.update_displayed_frames()


    def rotate_90_clock(self):
        cvf = self.tkinter_to_cv(self.tkinter_images)
        pp = []
        for frm in cvf:
            pp.append(cv2.cvtColor(frm, cv2.COLOR_BGR2RGB))
        ed_frames = GifEditor.rotate_frames_90_clockwise(GifEditor, pp)
        self.frames = Gif.reassess_frames(Gif, ed_frames)
        self.GIF.height, self.GIF.width, c = ed_frames[0].shape
        self.GIF.set_frames(self.frames)
        self.update_displayed_frames()
        self.reposition()


    def rotate_90_count_clock(self):
        cvf = self.tkinter_to_cv(self.tkinter_images)
        pp = []
        for frm in cvf:
            pp.append(cv2.cvtColor(frm, cv2.COLOR_BGR2RGB))
        ed_frames = GifEditor.rotate_frames_90_counterclockwise(GifEditor, pp)
        self.frames = Gif.reassess_frames(Gif, ed_frames)
        self.GIF.width, self.GIF.height = ed_frames[0].shape[1], ed_frames[0].shape[0]
        self.GIF.set_frames(self.frames)
        self.update_displayed_frames()
        self.reposition()


    def mirror_gif_across_x(self):
        cvf = self.tkinter_to_cv(self.tkinter_images)
        pp = []
        for frm in cvf:
            pp.append(cv2.cvtColor(frm, cv2.COLOR_BGR2RGB))
        ed_frames = GifEditor.mirror_frames(GifEditor, pp, 3)
        self.frames = Gif.reassess_frames(Gif, ed_frames)
        self.GIF.set_frames(self.frames)
        self.update_displayed_frames()
        self.reposition()


    def mirror_gif_across_y(self):
        cvf = self.tkinter_to_cv(self.tkinter_images)
        pp = []
        for frm in cvf:
            pp.append(cv2.cvtColor(frm, cv2.COLOR_BGR2RGB))
        ed_frames = GifEditor.mirror_frames(GifEditor, pp, 4)
        self.frames = Gif.reassess_frames(Gif, ed_frames)
        self.GIF.set_frames(self.frames)
        self.update_displayed_frames()
        self.reposition()


    def speed_up(self):
        self.speed -= self.adjustment_speed
        self.update_displayed_frames()


    def slow_down(self):
        self.speed += self.adjustment_speed
        self.update_displayed_frames()


    def tkinter_to_cv(self, frames):
        opencv_frames = []

        for tk_img in frames:
            pil_img = ImageTk.getimage(tk_img)  # Convert tkinter image to PIL Image
            cv_img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)  # Convert PIL Image to OpenCV format
            opencv_frames.append(cv_img)

        return opencv_frames


    def cv_color_swap(self, frames):
        updated = []
        for frame in frames:
            img = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            updated.append(img)
        return updated


    def update_displayed_frames(self):
        # Update the PhotoImage instances for the new frames
        self.tkinter_images = [tk.PhotoImage(data=frm) for frm in self.frames]

        # Update the current frame being displayed
        self.current_frame = 0
        self.label.config(image=self.tkinter_images[self.current_frame])

        # Call the update_frame function to start updating the frames


    def update_frame(self):
        self.current_frame = (self.current_frame + 1) % len(self.frames)
        self.label.config(image=self.tkinter_images[self.current_frame])
        self.root.after(self.speed, self.update_frame)


    def increase_size(self):
        res = self.tkinter_to_cv(self.tkinter_images)
        resized = []
        for img in res:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            # Get the current image dimensions
            height, width = img.shape[:2]
            # Calculate new dimensions
            new_width = width + self.adjustment_w
            new_height = height + self.adjustment_h
            if new_width > self.max_dim[0]:
                new_width = self.max_dim[0]
            if new_height > self.max_dim[1]:
                new_height = self.max_dim[1]
            # Resize the image using OpenCV
            resized_img = cv2.resize(img, (new_width, new_height))
            # Append the resized image to the "resized" array
            resized.append(resized_img)

        self.frames = Gif.reassess_frames(Gif, resized)
        self.GIF.width, self.GIF.height = resized[0].shape[1], resized[0].shape[0]
        self.GIF.set_frames(self.frames)
        self.update_displayed_frames()
        self.reposition()


    def decrease_size(self):
        res = self.tkinter_to_cv(self.tkinter_images)
        resized = []
        for img in res:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            height, width = img.shape[:2]
            new_width = width - self.adjustment_w
            new_height = height - self.adjustment_h
            if new_width > self.max_dim[0]:
                new_width = self.max_dim[0]
            if new_height > self.max_dim[1]:
                new_height = self.max_dim[1]
            resized_img = cv2.resize(img, (new_width, new_height))
            resized.append(resized_img)

        self.frames = Gif.reassess_frames(Gif, resized)
        self.GIF.width, self.GIF.height = resized[0].shape[1], resized[0].shape[0]
        self.GIF.set_frames(self.frames)
        self.update_displayed_frames()
        self.reposition()

    def efbf(self):
        self.running = "attsf"
        self.asRoot = tk.Tk()
        self.asRoot.title("Advanced Settings")
        self.asRoot.geometry("480x480")
        self.canvas = tk.Canvas(self.asRoot, width=480, height=480, highlightthickness=0)
        for n in range(480):
            shade = "#%02x%02x%02x" % (40, 0, 80 + int(160 * (n / 480)))
            self.canvas.create_line(0, n, 480, n, fill=shade)
        self.canvas.pack()
        ciw = tk.Label(self.asRoot,
                       text=f"Frames: {len(self.tkinter_images)}",
                       font=Button.bold, bg="gray")
        ciw.place(x=20, y=30, height=35)
        self.t = tk.Entry(self.asRoot, bg="gray", font=Button.standard)
        self.t.place(x=(480-250)/2, rely=0.3, width=250, height=35)

        self.m = tk.Entry(self.asRoot, bg="gray", font=Button.standard)
        self.m.place(x=(480-250)/2, rely=0.4, width=250, height=35)

        self.b = tk.Entry(self.asRoot, bg="gray", font=Button.standard)
        self.b.place(x=(480-250)/2, rely=0.5, width=250, height=35)

        select = tk.Label(self.asRoot,
                          text="#-#:",
                          font=Button.standard, bg="gray")
        select.place(relx=0.5, y=30, width=75, height=35)
        self.amount_edit = tk.Entry(self.asRoot, bg="gray", font=Button.standard)
        self.amount_edit.place(relx=0.7, y=30, width=100, height=35)

        but = tk.Button(self.asRoot, bg="gray", text="Submit", font=Button.standard, command=self.add_speci_text)
        but.place(x=(480-70)/2, rely=0.6, width=70, height=35)

        self.asRoot.mainloop()


    def add_speci_text(self):
        frames_str = self.amount_edit.get()
        integers = re.findall(r'\d+', frames_str)
        integers = list(map(int, integers))
        edit = []
        for i, frame in enumerate(self.tkinter_images):
            if i >= integers[0]:
                edit.append(frame)
                if i == integers[1]:
                    break
        top = self.t.get()
        mid = self.m.get()
        bot = self.b.get()
        size = self.fs
        font = self.font
        shape = [self.GIF.gif_width(), self.GIF.gif_height()]
        color = self.fc
        smake = self.tkinter_to_cv(self.tkinter_images.copy())
        #smake = Gif.reassess_frames(Gif, smake)
        smake = Gif.reasses_nocol(Gif, smake)
        #smake = Gif.change_col(Gif, smake)
        pil_im = GifEditor.tkinter_images_to_pillow(None, edit, shape[0], shape[1])
        edited = GifEditor.add_text(GifEditor, pil_im, top, mid, bot, size, font, shape, color)
        #edited = Gif.reassess_frames(Gif, edited)
        frm = []
        num = 0
        for i, frame in enumerate(smake):
            if integers[0] <= i <= integers[1]:
                frm.append(edited[num])
                num += 1
            else:
                frm.append(frame)
            #print(type(frm[i]))
        self.frames = frm.copy()
        self.GIF.set_frames(self.frames)

        # Update the displayed frames on the GUI
        self.update_displayed_frames()
        self.asRoot.destroy()

        #pil_im = GifEditor.tkinter_images_to_pillow(None, self.tkinter_images, shape[0], shape[1])
        #self.frames = GifEditor.add_text(GifEditor, pil_im, top, mid, bot, size, font, shape, color)
        #self.GIF.set_frames(self.frames)

        #self.update_displayed_frames()


    # Repositions all interactables after modification of the Gif's size
    def reposition(self, constant=30, spacing=75):
        if not self.running.__eq__("cfs"):
            self.fs = int(min(self.GIF.gif_height() / 5.5, self.GIF.gif_width() / 5.5))
        if self.GIF.gif_width() > self.max_dim[0] or self.GIF.gif_height() > self.max_dim[1]:
            self.throw_warning()
        #self.submit_text.destroy()
        self.top.destroy()
        self.mid.destroy()
        self.bot.destroy()
        #self.rotate90clock.destroy()
        #self.rotate90countclock.destroy()
        #self.mirror_x.destroy()
        #self.mirror_y.destroy()
        #self.increase.destroy()
        #self.decrease.destroy()
        #self.speedup.destroy()
        #self.slowdown.destroy()


        #self.rotate90clock = tk.Button(self.root, text="⟳", bg=Button.button_bg, font=Button.bold, bd=Button.base_bd,
                                       #command=self.rotate_90_clock)
        #self.rotate90clock.place(x=self.x - (Button.constant * 3 + Button.spacing * 2), y=Button.constant,
                                 #width=Button.but_w, height=Button.but_h)

        #self.rotate90countclock = tk.Button(self.root, text="⟲", bg=Button.button_bg, font=Button.bold,
                                            #bd=Button.base_bd, command=self.rotate_90_count_clock)
        #self.rotate90countclock.place(x=self.x - (Button.constant * 3 + Button.spacing), y=Button.constant,
                                      #width=Button.but_w, height=Button.but_h)

        #self.mirror_x = tk.Button(self.root, text="⇅", bg=Button.button_bg, font=Button.bold, bd=Button.base_bd,
                                  #command=self.mirror_gif_across_x)
        #self.mirror_x.place(x=self.x - (Button.constant * 3 + Button.spacing * 2), y=Button.constant + Button.spacing,
                            #width=Button.but_w, height=Button.but_h)

        #self.mirror_y = tk.Button(self.root, text="⇆", bg=Button.button_bg, font=Button.bold, bd=Button.base_bd,
                                  #command=self.mirror_gif_across_y)
        #self.mirror_y.place(x=self.x - (Button.constant * 3 + Button.spacing), y=Button.constant + Button.spacing,
                            #width=Button.but_w, height=Button.but_h)

        #self.increase = tk.Button(self.root, text="↑", bg=Button.button_bg, font=Button.bold, bd=Button.base_bd,
                                  #command=self.increase_size)
        #self.increase.place(x=self.x - Button.constant * 3, y=Button.constant,
                            #width=Button.but_w, height=Button.but_h)

        #self.decrease = tk.Button(self.root, text="↓", bg=Button.button_bg, font=Button.bold, bd=Button.base_bd,
                                  #command=self.decrease_size)
        #self.decrease.place(x=self.x - Button.constant * 3, y=Button.constant + Button.spacing,
                            #width=Button.but_w, height=Button.but_h)

        #self.speedup = tk.Button(self.root, text="🐇", bg=Button.button_bg, font=Button.bold, bd=Button.base_bd,
                                 #command=self.speed_up)
        #self.speedup.place(x=self.x - (Button.constant * 3 + Button.spacing * 3), y=Button.constant,
                           #width=Button.but_w, height=Button.but_h)

        #self.slowdown = tk.Button(self.root, text="🐢", bg=Button.button_bg, font=Button.bold, bd=Button.base_bd,
                                  #command=self.slow_down)
        #self.slowdown.place(x=self.x - (Button.constant * 3 + Button.spacing * 3), y=Button.constant + Button.spacing,
                            #width=Button.but_w, height=Button.but_h)

        #self.submit_text = tk.Button(self.root, text="Submit Text", bg=Button.button_bg, font=("Arial, 15"),
                                     #bd=Button.base_bd, command=self.add_text)
        #self.submit_text.place(x=self.x - (248), y=Button.constant * 11, width=150, height=50)

        self.top = tk.Entry(self.root, font=("Arial", 15), bg="gray", bd=7, highlightthickness=0)
        self.top.place(x=self.x - (173), y=Button.constant * 7, anchor=tk.CENTER, width=250)

        self.mid = tk.Entry(self.root, font=("Arial", 15), bg="gray", bd=7, highlightthickness=0)
        self.mid.place(x=self.x - (173), y=Button.constant * 8.5, anchor=tk.CENTER, width=250)

        self.bot = tk.Entry(self.root, font=("Arial", 15), bg="gray", bd=7, highlightthickness=0)
        self.bot.place(x=self.x - (173), y=Button.constant * 10, anchor=tk.CENTER, width=250)


    def set_dim(self, x, y):
        self.fs = int(min(y / 5.5, x / 5.5))
        res = self.tkinter_to_cv(self.tkinter_images)
        resized = []
        for img in res:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            new_width = x
            new_height = y
            resized_img = cv2.resize(img, (new_width, new_height))
            resized.append(resized_img)

        self.frames = Gif.reassess_frames(Gif, resized)
        self.GIF.width, self.GIF.height = resized[0].shape[1], resized[0].shape[0]
        self.GIF.set_frames(self.frames)
        self.update_displayed_frames()


    def add_white_box_and_text(self):
        self.asRoot = tk.Tk()
        self.asRoot.title("Advanced Settings")
        self.asRoot.geometry("480x480")
        self.canvas = tk.Canvas(self.asRoot, width=480, height=480, highlightthickness=0)
        for n in range(480):
            shade = "#%02x%02x%02x" % (40, 0, 80 + int(160 * (n / 480)))
            self.canvas.create_line(0, n, 480, n, fill=shade)
        self.canvas.pack()
        ciw = tk.Label(self.asRoot,
                       text=f"Box Size Multiplier (Required)",
                       font=Button.bold, bg="gray")
        ciw.place(x=20, y=30, height=35)
        inf = tk.Label(self.asRoot,
                       text=f"Standard value is 1/2 or 1/3.\nThis means the box will be\n1/2 or 1/3 the size of the gif.\nPlease use fractions.",
                       font=Button.standard, bg="gray")
        inf.place(x=20, y=75, height=90)
        self.wt = tk.Entry(self.asRoot, bg="gray", font=Button.standard)
        self.wt.place(x=(480-250)/2, rely=0.5, width=250, height=35)

        self.wm = tk.Entry(self.asRoot, bg="gray", font=Button.standard)
        self.wm.place(x=(480-250)/2, rely=0.6, width=250, height=35)

        self.wb = tk.Entry(self.asRoot, bg="gray", font=Button.standard)
        self.wb.place(x=(480-250)/2, rely=0.7, width=250, height=35)

        self.box_size = tk.Entry(self.asRoot, bg="gray", font=Button.standard)
        self.box_size.place(relx=0.8, y=30, width=75, height=35)

        but = tk.Button(self.asRoot, bg="gray", text="Submit", font=Button.standard, command=self.whitebox_action)
        but.place(x=(480-70)/2, rely=0.8, width=70, height=35)

        self.asRoot.mainloop()

    def whitebox_action(self):
        self.add_white_box()
        self.add_whitebox_text()


    def add_white_box(self):
        frames = self.tkinter_to_cv(self.tkinter_images)
        #frames = Gif.reasses_nocol(Gif, frames)
        # Define the color of the white box (in BGR format, white is [255, 255, 255])
        white_color = [255, 255, 255]

        # Create a list to store the modified frames
        modified_frames = []

        for frame in frames:
            height, width, _ = frame.shape
            # Create a white box with the same width as the frame
            factor = self.box_size.get()
            numer = float(factor[:factor.index("/")].strip())
            denom = float(factor[factor.index("/") + 1:].strip())
            frac = numer / denom
            white_box = np.full((int(height * frac), width, 3), white_color)

            # Stack the original frame on top of the white box
            modified_frame = np.vstack((white_box, frame))
            modified_frame = cv2.convertScaleAbs(modified_frame)
            # Append the modified frame to the list
            modified_frames.append(modified_frame)
            #print(type(frame))
            #print(type(modified_frame))


        #self.frames = Gif.reassess_frames(Gif, modified_frames)
        self.frames = Gif.reasses_nocol(Gif, modified_frames)
        self.GIF.width, self.GIF.height = modified_frames[0].shape[1], modified_frames[0].shape[0]
        self.GIF.set_frames(self.frames)
        self.update_displayed_frames()


    def add_whitebox_text(self):
        top = self.wt.get()
        mid = self.wm.get()
        bot = self.wb.get()

        font = self.font
        factor = self.box_size.get()
        numer = float(factor[:factor.index("/")].strip())
        denom = float(factor[factor.index("/") + 1:].strip())
        denom += 1
        frac = numer / denom
        size = int(self.fs * (numer/(denom-1)))
        shape = [self.GIF.gif_width(), int(self.GIF.gif_height()*frac)]
        color = self.fc
        smake = self.tkinter_to_cv(self.tkinter_images.copy())
        #smake = Gif.reassess_frames(Gif, smake)
        smake = Gif.reasses_nocol(Gif, smake)
        #smake = Gif.change_col(Gif, smake)
        pil_im = GifEditor.tkinter_images_to_pillow(None, self.tkinter_images.copy(), shape[0], shape[1])
        edited = GifEditor.add_text(GifEditor, pil_im, top, mid, bot, size, font, shape, color)
        #edited = Gif.reassess_frames(Gif, edited)
        self.frames = edited.copy()
        self.GIF.set_frames(self.frames)

        self.update_displayed_frames()
        self.asRoot.destroy()


    def change_in_dims(self):
        self.running = "cid"
        self.asRoot = tk.Tk()
        self.asRoot.title("Advanced Settings")
        self.asRoot.geometry("480x95")
        self.canvas = tk.Canvas(self.asRoot, width=480, height=95, highlightthickness=0)
        for n in range(95):
            shade = "#%02x%02x%02x" % (40, 0, 80 + int(160 * (n / 95)))
            self.canvas.create_line(0, n, 480, n, fill=shade)
        self.canvas.pack()
        ciw = tk.Label(self.asRoot, text=f"Dimensions: {self.tkinter_images[0].width()}x{self.tkinter_images[0].height()}", font=Button.bold, bg="gray")
        ciw.place(x=20, y=30, height=35)
        self.edit = tk.Entry(self.asRoot, bg="gray", font=Button.standard)
        self.edit.place(x=280, y=30, width=100, height=35)
        but = tk.Button(self.asRoot, bg="gray", text="Submit", font=Button.standard, command=self.return_to)
        but.place(x=390, y=30, width=70, height=35)

        self.asRoot.mainloop()


    def change_font_size(self):
        self.running = "cfs"
        self.asRoot = tk.Tk()
        self.asRoot.title("Advanced Settings")
        self.asRoot.geometry("480x95")
        self.canvas = tk.Canvas(self.asRoot, width=480, height=95, highlightthickness=0)
        for n in range(95):
            shade = "#%02x%02x%02x" % (40, 0, 80 + int(160 * (n / 95)))
            self.canvas.create_line(0, n, 480, n, fill=shade)
        self.canvas.pack()
        ciw = tk.Label(self.asRoot,
                       text=f"Font Size: {self.fs}",
                       font=Button.bold, bg="gray")
        ciw.place(x=20, y=30, height=35)
        self.edit = tk.Entry(self.asRoot, bg="gray", font=Button.standard)
        self.edit.place(x=280, y=30, width=100, height=35)
        but = tk.Button(self.asRoot, bg="gray", text="Submit", font=Button.standard, command=self.return_to)
        but.place(x=390, y=30, width=70, height=35)

        self.asRoot.mainloop()


    def change_duration(self):
        self.running = "cd"
        self.asRoot = tk.Tk()
        self.asRoot.title("Advanced Settings")
        self.asRoot.geometry("480x95")
        self.canvas = tk.Canvas(self.asRoot, width=480, height=95, highlightthickness=0)
        for n in range(95):
            shade = "#%02x%02x%02x" % (40, 0, 80 + int(160 * (n / 95)))
            self.canvas.create_line(0, n, 480, n, fill=shade)
        self.canvas.pack()
        ciw = tk.Label(self.asRoot,
                       text=f"Duration (each frame): {self.speed}",
                       font="Helvetica 14 bold", bg="gray")
        ciw.place(x=20, y=30, height=35)
        self.edit = tk.Entry(self.asRoot, bg="gray", font=Button.standard)
        self.edit.place(x=280, y=30, width=100, height=35)
        but = tk.Button(self.asRoot, bg="gray", text="Submit", font=Button.standard, command=self.return_to)
        but.place(x=390, y=30, width=70, height=35)

        self.asRoot.mainloop()


    def change_font_color(self):
        self.running = "cfc"
        self.asRoot = tk.Tk()
        self.asRoot.title("Advanced Settings")
        self.asRoot.geometry("480x95")
        self.canvas = tk.Canvas(self.asRoot, width=480, height=95, highlightthickness=0)
        for n in range(95):
            shade = "#%02x%02x%02x" % (40, 0, 80 + int(160 * (n / 95)))
            self.canvas.create_line(0, n, 480, n, fill=shade)
        self.canvas.pack()
        ciw = tk.Label(self.asRoot,
                       text=f"Font Color: {self.fc}",
                       font="Helvetica 14 bold", bg="gray")
        ciw.place(x=20, y=30, height=35)
        self.edit = tk.Entry(self.asRoot, bg="gray", font=Button.standard)
        self.edit.place(x=280, y=30, width=100, height=35)
        but = tk.Button(self.asRoot, bg="gray", text="Submit", font=Button.standard, command=self.return_to)
        but.place(x=390, y=30, width=70, height=35)

        self.asRoot.mainloop()

    def change_font(self):
        self.running = "cf"
        self.asRoot = tk.Tk()
        self.asRoot.title("Advanced Settings")
        self.asRoot.geometry("480x95")
        self.canvas = tk.Canvas(self.asRoot, width=480, height=95, highlightthickness=0)
        for n in range(95):
            shade = "#%02x%02x%02x" % (40, 0, 80 + int(160 * (n / 95)))
            self.canvas.create_line(0, n, 480, n, fill=shade)
        self.canvas.pack()
        ciw = tk.Label(self.asRoot,
                       text=f"Font: {self.font}",
                       font="Helvetica 14 bold", bg="gray")
        ciw.place(x=20, y=30, height=35)

        def browse_file():
            font_file_path = filedialog.askopenfilename(filetypes=[("Font Files", "*.ttf *.otf")])
            if font_file_path:
                self.edit.delete(0, tk.END)  # Clear any previous text
                self.edit.insert(0, font_file_path)

        browse_button = tk.Button(self.asRoot, bg="gray", text="Browse", font="Helvetica 12", command=browse_file)
        browse_button.place(x=200, y=30, width=70, height=35)

        self.edit = tk.Entry(self.asRoot, bg="gray", font="Helvetica 12")
        self.edit.place(x=280, y=30, width=100, height=35)

        submit_button = tk.Button(self.asRoot, bg="gray", text="Submit", font="Helvetica 12", command=self.return_to)
        submit_button.place(x=390, y=30, width=70, height=35)

        self.asRoot.mainloop()


    def return_to(self):
        e = True
        try:
            self.valu = int(self.edit.get())
        except:
            if self.edit.get().__eq__(""):
                e = False
            elif self.edit.get().__eq__("MAXDIM"):
                self.valu = self.max_dim
                e = False
            if e == True:
                integers = re.findall(r'\d+', self.edit.get())
                integers = list(map(int, integers))
                self.valu = integers[:2]
        if self.running.__eq__("cid"):
            if self.valu[0] > self.max_dim[0]:
                self.valu[0] = self.max_dim[0]
            if self.valu[1] > self.max_dim[1]:
                self.valu[1] = self.max_dim[1]
            self.set_dim(self.valu[0], self.valu[1])
        elif self.running.__eq__("cfs"):
            self.fs = self.valu
            self.reposition()
        elif self.running.__eq__("cd"):
            self.speed = self.valu
            self.update_displayed_frames()
        elif self.running.__eq__("cfc"):
            ed = self.edit.get()
            ed = ed.strip()
            ed = ed[1:len(ed)-1]
            nums = ed.split(",")
            #print(ed)
            #print(nums)
            self.fc = (int(nums[0]), int(nums[1]), int(nums[2]))
            #print(self.fc)
        elif self.running.__eq__("cf"):
            self.font = self.edit.get()
        self.asRoot.destroy()


    def throw_warning(self):
        root = tk.Tk()
        root.title("WARNING")
        root.geometry("520x80")
        warning = tk.Label(root, text="WARNING: Your gif has been altered and has surpassed the bounds given to it.\n"
                                      f"Bounds given to your gif: ( [0, 0] , {self.max_dim} )\n"
                                      "The bounds simply represent the maximum allowed size of your gif.\n"
                                      "This does not affect your gif's details.", font=("Arial, 11"))
        warning.pack()
        root.mainloop()

    def save_as(self):
        self.asRoot = tk.Tk()
        self.asRoot.title("Advanced Settings")
        self.asRoot.geometry("480x240")
        self.canvas = tk.Canvas(self.asRoot, width=480, height=480, highlightthickness=0)
        for n in range(240):
            shade = "#%02x%02x%02x" % (40, 0, 80 + int(160 * (n / 240)))
            self.canvas.create_line(0, n, 480, n, fill=shade)
        self.canvas.pack()
        ciw = tk.Label(self.asRoot,
                       text=f"Thank you for editing with GifGig!",
                       font="Helvetica 14 bold", bg="gray")
        ciw.place(y=30, height=35, x=120)
        name = tk.Label(self.asRoot,
                        text="Gif Name:",
                        font="Helvetica 14 bold", bg="gray")
        name.place(x=20, y=75, height=35, width=100)
        self.nedit = tk.Entry(self.asRoot, bg="gray", font=Button.standard)
        self.nedit.place(x=120, y=75, width=340, height=35)
        direct = tk.Label(self.asRoot,
                          text="Directory:",
                          font="Helvetica 14 bold", bg="gray")
        direct.place(x=20, y=120, height=35, width=100)

        # Create a button to open a folder selection dialog
        self.directory_button = tk.Button(self.asRoot, bg="gray", text="Select Folder", font=Button.standard,
                                          command=self.select_directory)
        self.directory_button.place(x=150, y=120, width=150, height=35)

        but = tk.Button(self.asRoot, bg="gray", text="Submit", font=Button.standard, command=self.save_gif)
        but.place(x=170, y=200, width=70, height=35)

        self.asRoot.mainloop()

    directory_p = ""
    def select_directory(self):
        # Open a folder selection dialog and store the selected directory in self.directory_p
        self.directory_p = filedialog.askdirectory()



    def save_gif(self):
        gif_name = "/" + self.nedit.get() + ".gif"
        #direct = self.saveto if self.directory.get().__eq__("") else self.directory.get()
        if not self.directory_p == "":
            sdg = self.directory_p
            direct = sdg
        else:
            direct = self.saveto
        to = direct + gif_name
        proc_frames = self.tkinter_to_cv(self.tkinter_images)
        proc_frames = self.cv_color_swap(proc_frames)
        #print(f"saving to {direct}")
        #print(f"{to}")
        with imageio.get_writer(to, mode="I", duration=self.speed, loop=0) as writer:
            for frame in proc_frames:
                writer.append_data(frame)
        self.root.destroy()
        self.asRoot.destroy()

