import tkinter as tk
import cv2

class Gif:

    def __init__(self, path):
        self.cap = cv2.VideoCapture(path)
        self.frames = []
        self.make_frames()

    def make_frames(self):
        while True:
            ret, frame = self.cap.read()
            if not ret or frame is None:
                break

            success, encoded_image = cv2.imencode(".png", frame)
            if not success:
                break

            image_bytes = encoded_image.tobytes()
            self.height, self.width, c = frame.shape
            self.frames.append(image_bytes)

        self.cap.release()


    def reassess_frames(self, frames):
        update = []
        for frame in frames:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            success, encoded_image = cv2.imencode(".png", frame)
            if not success:
                break
            image_bytes = encoded_image.tobytes()
            self.height, self.width, c = frame.shape
            update.append(image_bytes)
        return update

    def reasses_nocol(self, frames):
        update = []
        for frame in frames:
            success, encoded_image = cv2.imencode(".png", frame)
            if not success:
                break
            image_bytes = encoded_image.tobytes()
            self.height, self.width, c = frame.shape
            update.append(image_bytes)
        return update




    def get_frames(self):
        return self.frames

    def gif_width(self):
        return self.width

    def gif_height(self):
        return self.height

    def set_frames(self, frames):
        self.frames = frames