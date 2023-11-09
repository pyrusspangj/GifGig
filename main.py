import tkinter as tk
from Gif_Editor_GUI import GifE
from Gif import Gif

def make_a_gif():
    pass
    #print("Make a Gif!")

#def edit_a_gif():
    #root.destroy()
    #gife_gui = GifE() # <-- Where it all starts

enter = GifE()

#gif = Gif("E:\\Blank Gifs\\elliot-open-season.gif")
#gif.set_frames()


# Create the main application window
#root = tk.Tk()
#root.title("GUI Program")
#root.geometry("720x480")

# Calculate the coordinates for the expanded rectangle
#constant = 30
#expanded_rectangle_x1 = constant
#expanded_rectangle_y1 = constant
#expanded_rectangle_x2 = 720 - constant
#expanded_rectangle_y2 = 480 - constant

# Create the rounded black rectangle
#canvas = tk.Canvas(root, width=720, height=480, highlightthickness=0)

# Calculate the coordinates for the hollowed rectangle
#hollowed_rectangle_x1 = 200
#hollowed_rectangle_y1 = 120
#hollowed_rectangle_x2 = 520
#hollowed_rectangle_y2 = 360

# Create the gradient background from darker purple to lighter purple
#for y in range(480):
    #shade = "#%02x%02x%02x" % (40, 0, 80 + int(160 * (y / 480)))
    #canvas.create_line(0, y, 720, y, fill=shade)

# Create the rounded black rectangle
#canvas.create_arc(expanded_rectangle_x1, expanded_rectangle_y1, expanded_rectangle_x1 + constant, expanded_rectangle_y1 + constant, start=90, extent=90, style=tk.ARC, outline="black", width=10)
#canvas.create_arc(expanded_rectangle_x2 - constant, expanded_rectangle_y1, expanded_rectangle_x2, expanded_rectangle_y1 + constant, start=0, extent=90, style=tk.ARC, outline="black", width=10)
#canvas.create_arc(expanded_rectangle_x1, expanded_rectangle_y2 - constant, expanded_rectangle_x1 + constant, expanded_rectangle_y2, start=180, extent=90, style=tk.ARC, outline="black", width=10)
#canvas.create_arc(expanded_rectangle_x2 - constant, expanded_rectangle_y2 - constant, expanded_rectangle_x2, expanded_rectangle_y2, start=270, extent=90, style=tk.ARC, outline="black", width=10)
#canvas.create_rectangle(expanded_rectangle_x1 + 20, expanded_rectangle_y1, expanded_rectangle_x2 - 20, expanded_rectangle_y2, outline="black", width=10)
#canvas.create_rectangle(expanded_rectangle_x1, expanded_rectangle_y1 + 20, expanded_rectangle_x2, expanded_rectangle_y2 - 20, outline="black", width=10)

# Create the hollowed rectangle with a darker purple color
#canvas.create_rectangle(hollowed_rectangle_x1, hollowed_rectangle_y1, hollowed_rectangle_x2, hollowed_rectangle_y2, outline="#400050", width=0)
#canvas.pack()

# Create the buttons
#center_x = 720 // 2
#center_y = 480 // 2
#button_width = 150
#button_height = 50
#button_x1 = center_x - button_width // 2
#button_x2 = center_x + button_width // 2

# First button
#button1_y1 = center_y - button_height
#button1_y2 = center_y - button_height // 2
#gif_maker = tk.Button(root, text="Gif Maker", bg="cyan", command=make_a_gif)
#gif_maker.place(x=button_x1, y=button1_y1, width=button_width, height=button_height)

# Second button
#button2_y1 = center_y + button_height // 2
#button2_y2 = center_y + button_height
#gif_editor = tk.Button(root, text="Gif Editor", bg="cyan", command=edit_a_gif)
#gif_editor.place(x=button_x1, y=button2_y1, width=button_width, height=button_height)

# Start the Tkinter event loop
#root.mainloop()
