import tkinter as tk
import os.path
import json
from tkinter import X, LEFT
import subprocess
import threading
from tkinter import messagebox
import pyperclip  # Import pyperclip for clipboard access


def save_values():
    executable_path = path_entry.get()
    authentication_token = token_entry.get()
    data = {
        "executable_path": executable_path,
        "authentication_token": authentication_token
    }
    with open('saved_values.json', 'w') as file:
        json.dump(data, file)


def load_values():
    try:
        with open('saved_values.json', 'r') as file:
            data = json.load(file)
            executable_path = data.get("executable_path", "")
            authentication_token = data.get("authentication_token", "")
            path_entry.insert(tk.END, executable_path)
            token_entry.insert(tk.END, authentication_token)
    except FileNotFoundError:
        pass


def fetch_clipboard_content():
    try:
        # Fetch the clipboard content and insert it into the token entry
        clipboard_content = pyperclip.paste().strip()
        if clipboard_content:
            token_entry.delete(0, tk.END)  # Clear the existing content
            token_entry.insert(0, clipboard_content)  # Insert clipboard content
            pyperclip.copy("")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch clipboard content:\n\n{str(e)}")


def execute_command():
    try:
        save_values()
        executable_path = path_entry.get().replace('\"', '').replace('\n',
                                                                     '')  # Remove quotes and blank lines from executable path
        authentication_token = token_entry.get().replace('\"', '').replace('\n',
                                                                           '')  # Remove quotes and blank lines from token
        if not executable_path:
            executable_path = "deadfrontier.exe"

        command = [executable_path, authentication_token]
        subprocess.Popen(command)  # Launch the subprocess program
        window.destroy()  # Close the Python program
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred:\n\n{str(e)}")


def execute_command_thread():
    thread = threading.Thread(target=execute_command)
    thread.setDaemon(True)
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
window_width = 300
window_height = 140
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

token_label = tk.Label(window, text="Authentication Token:")
token_label.pack()
token_entry = tk.Entry(window)
token_entry.pack(fill=X, padx=5, pady=5)

# Load saved values
load_values()

# Fetch clipboard content and prefill the token entry
fetch_clipboard_content()

# Create the execute button
execute_button = tk.Button(window, text="Login", width=10, command=execute_command_thread)
execute_button.pack(side=LEFT, padx=5, pady=5)

# Run the application
window.mainloop()
