from PIL import ImageFont, ImageDraw, Image
import numpy as np
import cv2
import os

class Text:


    def initialize_crucial_variables(self, width, height):
        self.image_width, self.image_height = width, height
        #self.font = ImageFont.truetype(self.font_name, self.font_size)
        #bbox = self.font.getmask("Example").getbbox()
        #self.txtwidth = bbox[2] - bbox[0]
        #self.txtheight = bbox[3] - bbox[1]
        #x = (self.image_width - self.txtwidth) // 2
        #self.top_text_coord = [x, 1]
        #self.mid_text_coord = [x, self.image_height // 2.5]
        #self.bot_text_coord = [x, self.image_height // 1.3]
        #self.chosen_coord = self.top_text_coord
        self.txtfont = int(min(self.image_height / 5.5, self.image_width / 5.5))


    txtwidth, txtheight = 50, 50
    font_size = 50
    font_name = 'impact.ttf'


    def __init__(self, frames, text1, text2, text3, font_size, font_name, shape, fc):
        self.frames = frames
        self.initialize_crucial_variables(shape[0], shape[1])
        self.top_text = text1
        self.mid_text = text2
        self.bot_text = text3
        self.font_size = font_size if font_size != -1 else self.txtfont
        self.font_name = font_name if font_name != "Imp" else 'impact.ttf'
        self.text_color = fc
        self.outline_color = (0, 0, 0) 


    def create_outlined_text_image(self, frame, text, font, chosen_coord):
        draw = ImageDraw.Draw(frame)

        for dx in [-1, 1]:
            for dy in [-1, 1]:
                outline_x = chosen_coord[0] + dx
                outline_y = chosen_coord[1] + dy
                draw.text((outline_x, outline_y), text, fill=self.outline_color, font=font, align="center")

        draw.text((chosen_coord[0], chosen_coord[1]), text, fill=self.text_color, font=font, align="center")

        return frame

    def add_text_to_frames(self):

        font = ImageFont.truetype(self.font_name, size=self.font_size)

        bbox1 = font.getmask(self.top_text).getbbox()
        bbox2 = font.getmask(self.mid_text).getbbox()
        bbox3 = font.getmask(self.bot_text).getbbox()

        x1, x2, x3 = 0, 0, 0
        y1, y2, y3 = 1, 1, 1

        if isinstance(bbox1, tuple):
            width1 = bbox1[2] - bbox1[0]
            x1 = (self.image_width - width1) // 2
        if isinstance(bbox2, tuple):
            width2 = bbox2[2] - bbox2[0]
            x2 = (self.image_width - width2) // 2
            y2 = (self.image_height - (bbox2[1] + bbox2[3])) // 2 - 10
        if isinstance(bbox3, tuple):
            width3 = bbox3[2] - bbox3[0]
            x3 = (self.image_width - width3) // 2
            y3 = self.image_height - bbox3[3]*1.5

        modified_frames = []

        for current_frame_tk in self.frames:
            current_frame = current_frame_tk

            combined_frame = self.create_outlined_text_image(current_frame, self.top_text, font, (x1, y1))
            combined_frame = self.create_outlined_text_image(combined_frame, self.mid_text, font, (x2, y2))
            combined_frame = self.create_outlined_text_image(combined_frame, self.bot_text, font, (x3, y3))

            modified_frame_cv = np.array(combined_frame)
            modified_frames.append(modified_frame_cv)

        return modified_frames
