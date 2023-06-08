import tkinter as tk
import subprocess
import threading

def toggle_button_action():
    global subprocess_obj
    if toggle_button_var.get():
        # Execute the script when the toggle button is turned on
        subprocess_obj = subprocess.Popen(["python", "GestureControl.py"])
        start_loading_circle()
    else:
        # Close the executed script when the toggle button is turned off
        if subprocess_obj:
            subprocess_obj.terminate()
            subprocess_obj = None
        stop_loading_circle()

def start_loading_circle():
    loading_thread = threading.Thread(target=draw_loading_circle)
    loading_thread.start()

def stop_loading_circle():
    canvas.delete("loading_circle")

def draw_loading_circle():
    x = canvas.winfo_width() // 2
    y = canvas.winfo_height() // 2
    radius = 50
    angle = 0

    while toggle_button_var.get():
        canvas.delete("loading_circle")
        canvas.create_arc(x - radius, y - radius, x + radius, y + radius, start=angle, extent=30, outline="blue", width=3, tags="loading_circle")
        angle = (angle + 30) % 360
        canvas.update()
        canvas.after(100)

# Create the main window
window = tk.Tk()
window.title("Toggle Button Example")
window.geometry("300x300")  # Set the window size to 300x300

# Create the title label
title_label = tk.Label(window, text="Windows Gesture Control", font=("Helvetica", 16))
title_label.pack(pady=10)

# Create the toggle button label
toggle_label = tk.Label(window, text="Start the Camera Service:", font=("Helvetica", 12))
toggle_label.pack()

# Create the toggle button
toggle_button_var = tk.BooleanVar()
toggle_button = tk.Checkbutton(window, text="Service", variable=toggle_button_var, command=toggle_button_action)
toggle_button.pack()

subprocess_obj = None  # Initialize subprocess object

# Create the canvas for drawing the loading circle
canvas = tk.Canvas(window, width=200, height=200)
canvas.pack()

# Run the GUI event loop
window.mainloop()
