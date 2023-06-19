import tkinter as tk
import os.path
from tkinter import X, LEFT
import subprocess
import threading
from tkinter import messagebox

def save_values():
    executable_path = path_entry.get()
    authenticator_token = token_entry.get()
    with open('saved_values.txt', 'w') as file:
        file.write(f"{executable_path}\n")
        file.write(f"{authenticator_token}")

def load_values():
    try:
        with open('saved_values.txt', 'r') as file:
            lines = file.readlines()
            executable_path = lines[0].strip()
            authenticator_token = lines[1].strip()
            path_entry.insert(tk.END, executable_path)
            token_entry.insert(tk.END, authenticator_token)
    except FileNotFoundError:
        pass

def execute_command():
    try:
        save_values()
        executable_path = path_entry.get().strip('\"')  # Remove quotes from executable path
        authenticator_token = token_entry.get().strip('\"')  # Remove quotes from token
        command = f'"{executable_path}" "{authenticator_token}"'
        subprocess.call(command, shell=True)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred:\n\n{str(e)}")

def execute_command_thread():
    thread = threading.Thread(target=execute_command)
    thread.start()

# Create the main window
window = tk.Tk()
window.title("Dead Frontier 3D at Work")
window.resizable(False, False)  # Make the window not resizable

# Set window icon if the file exists
icon_file = "dficon.ico"
if os.path.exists(icon_file):
    window.iconbitmap(icon_file)

# Calculate window position at the center of the screen
window_width = 350
window_height = 150
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2
window.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Create the labels and entry fields
path_label = tk.Label(window, text="Executable Path:")
path_label.pack()
path_entry = tk.Entry(window)
path_entry.pack(fill=X, padx=5, pady=5)

token_label = tk.Label(window, text="Authenticator Token:")
token_label.pack()
token_entry = tk.Entry(window)
token_entry.pack(fill=X, padx=5, pady=5)

# Load saved values
load_values()

# Create the execute button
execute_button = tk.Button(window, text="Login", command=execute_command_thread)
execute_button.pack(side=LEFT, padx=5, pady=5)

# Run the application
window.mainloop()
