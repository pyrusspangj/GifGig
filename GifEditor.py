from PIL import ImageFont, ImageDraw, Image, ImageTk
from Text import Text
import cv2
import imageio
import os
import tkinter as tk
from Gif import Gif
class GifEditor:

    height, width = 0, 0

    editing = True
    frames = []


    def add_text(self, frames, top_text, mid_text, bot_text, size, font, shape, fc):
        txt = Text(frames, top_text, mid_text, bot_text, size, font, shape, fc)
        pils = txt.add_text_to_frames()
        #send = self.pillow_images_to_tkinter(None, pils)
        update = Gif.reassess_frames(Gif, pils)
        return update


    def transformation(self): #1
        transforming = True
        while transforming:
            tfmt = int(input("\n1. Rotate 90° Clockwise\n2. Rotate 90° Cnt-Clockwise\n3. Mirror Vert\n4. Mirror Horz\n5. To quit\n"))
            if tfmt == 1:
                self.frames = self.rotate_frames_90_clockwise(self.frames)
            elif tfmt == 2:
                self.frames = self.rotate_frames_90_counterclockwise(self.frames)
            elif tfmt == 3 or tfmt == 4:
                self.frames = self.mirror_frames(self.frames, tfmt)
            elif tfmt == 5:
                transforming = False


    def create_gif(self):
        self.editing = False
        print(f"Making Gif in {self.directory}, thank you for editing with us!")
        with imageio.get_writer(self.through, mode="I", duration=0.042, loop=0) as writer:
            for frame in self.frames:
                writer.append_data(frame)


    def rotate_frames_90_clockwise(self, frames):
        rotated_frames = []
        for frame in frames:
            # Rotate the frame 90 degrees clockwise
            rotated_frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
            rotated_frames.append(rotated_frame)
        return rotated_frames


    def rotate_frames_90_counterclockwise(self, frames):
        rotated_frames = []
        for frame in frames:
            # Rotate the frame 90 degrees counter-clockwise
            rotated_frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
            rotated_frames.append(rotated_frame)
        return rotated_frames


    def mirror_frames(self, frames, val):
        val -= 3
        mirrored_frames = []
        for frame in frames:
            # Mirror the frame
            mirrored_frame = cv2.flip(frame, val)
            mirrored_frames.append(mirrored_frame)
        return mirrored_frames


    def tkinter_images_to_pillow(self, tk_images, width, height):
        pillow_images = []

        for tk_image in tk_images:
            # Convert the Tkinter PhotoImage to a Pillow Image
            pil_image = ImageTk.getimage(tk_image)

            # Append the PIL Image to the list
            pillow_images.append(pil_image)

        return pillow_images


    def pillow_images_to_tkinter(self, pillow_images):
        tk_images = []
        for pillow_image in pillow_images:
            # Create a Tkinter PhotoImage from the Pillow image
            tk_image = ImageTk.PhotoImage(pillow_image)
            tk_images.append(tk_image)
        return tk_images