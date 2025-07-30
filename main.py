import tkinter as tk
import threading
import ctypes
import os
import time
import random

# === CONFIGURATION ===
IMAGE_FOLDER = r"C:\Users\shaal\Desktop\epic\python\images"
DELAY_SECONDS = 5

# === STATE ===
running = False
changer_thread = None

# === WALLPAPER FUNCTION ===
def set_wallpaper(image_path):
    ctypes.windll.user32.SystemParametersInfoW(20, 0, image_path, 3)

def wallpaper_loop():
    global running
    image_files = [f for f in os.listdir(IMAGE_FOLDER) if f.lower().endswith(('.png', '.jpeg', '.jpg', '.bmp'))]
    image_paths = [os.path.join(IMAGE_FOLDER, f) for f in image_files]

    if not image_paths:
        print("No images found.")
        return

    last_image = None
    while running:
        image = random.choice(image_paths)
        while image == last_image and len(image_paths) > 1:
            image = random.choice(image_paths)
        last_image = image
        print(f"Setting wallpaper: {image}")
        set_wallpaper(image)
        time.sleep(DELAY_SECONDS)

# === TOGGLE FUNCTION ===
def toggle():
    global running, changer_thread
    if not running:
        running = True
        button.config(text="Stop")
        changer_thread = threading.Thread(target=wallpaper_loop, daemon=True)
        changer_thread.start()
    else:
        running = False
        button.config(text="Start")

# === BUILD TKINTER WIDGET ===
root = tk.Tk()
root.title("Wallpaper Widget")
root.geometry("200x100")
root.attributes("-topmost", True)
root.resizable(False, False)
root.configure(bg="#222")

# Optional: Remove window border to make it look more like a widget
root.overrideredirect(True)

# Add Start/Stop button
button = tk.Button(root, text="Start", command=toggle, bg="#444", fg="white", font=("Arial", 12))
button.pack(padx=20, pady=20)

# Make widget draggable
def start_move(event):
    root.x = event.x
    root.y = event.y

def do_move(event):
    x = event.x_root - root.x
    y = event.y_root - root.y
    root.geometry(f'+{x}+{y}')

root.bind("<Button-1>", start_move)
root.bind("<B1-Motion>", do_move)

# Close on double-click
def close_app(event):
    global running
    running = False
    root.destroy()

root.bind("<Double-Button-1>", close_app)

# Start the widget
root.mainloop()
