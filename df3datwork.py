import tkinter as tk
from tkinter import ttk, messagebox
import os
import json
import subprocess
import threading
import urllib.request
import pyperclip

autoLogin = "false"
progress_var = None
progress_bar = None
progress_label = None
progress_label_var = None


def extract_inno_setup_installer(installer_path):
    def run_extraction():
        try:

            os.makedirs("Game", exist_ok=True)

            command = ["innounp.exe", "-x", "-y", "-d" + "Game", installer_path]

            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

            while True:
                line = process.stdout.readline()
                if not line:
                    break
                else:
                    progress_label_var.set(f"Extracting: {line}")

            process.wait()

            if process.returncode != 0:
                raise subprocess.CalledProcessError(process.returncode, command)

            os.remove(installer_path)

            window.after(0, execute_command)
        except Exception as e:
            window.after(0, lambda: messagebox.showerror("Error", f"{str(e)}"))

    thread = threading.Thread(target=run_extraction)

    thread.start()


def parse_clipboard():
    clipboard_content = pyperclip.paste().strip()
    token = ""
    download_link = ""
    if clipboard_content and "token" in clipboard_content:
        lines = clipboard_content.splitlines()
        for line in lines:
            if line.startswith("token"):
                token = line.replace("token", "").strip()
            elif line.startswith("http"):
                download_link = line.strip()
    return token, download_link


def load_json():
    if os.path.exists('saved_values.json'):
        with open('saved_values.json', 'r') as file:
            return json.load(file)
    return {}


def save_json(data):
    with open('saved_values.json', 'w') as file:
        json.dump(data, file)


def download_with_progress(url, local_path):
    def reporthook(block_num, block_size, total_size):
        downloaded = block_num * block_size
        percent = int(min(100, downloaded * 100 / total_size))
        progress_var.set(percent)
        progress_label_var.set(f"Downloading... {percent}%")
        progress_bar.update_idletasks()

    try:
        urllib.request.urlretrieve(url, local_path, reporthook)
        extract_inno_setup_installer(local_path)
    except Exception as e:
        window.after(0, lambda: messagebox.showerror("Error", f"{str(e)}"))


def threaded_download(url):
    local_path = os.path.join(os.getcwd(), "Installer.exe")
    progress_var.set(0)
    progress_bar.pack(padx=20, pady=(10, 5), fill=tk.X)
    progress_label.pack(padx=20, pady=(0, 10), fill=tk.X)
    progress_label_var.set("Starting download...")
    thread = threading.Thread(target=download_with_progress, args=(url, local_path))
    thread.start()
    return url


def download_installer_if_needed(new_link, current_link):
    if new_link and new_link != current_link:
        return threaded_download(new_link)
    return current_link


def fetch_clipboard_content():
    try:
        token, new_link = parse_clipboard()
        if not token and not new_link:
            return

        token_entry.delete(0, tk.END)
        token_entry.insert(0, token)

        data = load_json()
        current_link = data.get("download_link", "")

        updated_link = download_installer_if_needed(new_link, current_link)

        data.update({
            "authentication_token": token,
            "autoLogin": autoLogin,
            "download_link": updated_link
        })

        save_json(data)
        pyperclip.copy("")
    except Exception as e:
        messagebox.showerror("Erro", f"Falha ao processar a área de transferência:\n\n{str(e)}")


def save_values():
    global autoLogin
    data = load_json()
    authentication_token = token_entry.get()
    data.update({
        "authentication_token": authentication_token,
        "autoLogin": autoLogin
    })
    save_json(data)


def load_values():
    global autoLogin
    try:
        data = load_json()
        authentication_token = data.get("authentication_token", "")
        autoLogin = data.get("autoLogin", "false")
        token_entry.insert(tk.END, authentication_token)
    except FileNotFoundError:
        pass


def execute_command():
    try:
        save_values()
        executable_path = "Game/{app}/deadfrontier.exe"
        authentication_token = token_entry.get().replace('\"', '').replace('\n', '')
        command = [executable_path, authentication_token]
        subprocess.Popen(command)
        window.after(0, window.destroy)
    except Exception as e:
        window.after(0, lambda: messagebox.showerror("Erro", f"Ocorreu um erro ao executar:\n\n{str(e)}"))


def execute_command_thread():
    thread = threading.Thread(target=execute_command)
    thread.setDaemon(True)
    thread.start()


window = tk.Tk()
window.title("Dead Frontier 3D at Work")
window.resizable(False, False)

icon_file = "dficon.ico"
if os.path.exists(icon_file):
    window.iconbitmap(icon_file)

window_width = 320
window_height = 200
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2
window.geometry(f"{window_width}x{window_height}+{x}+{y}")

main_frame = ttk.Frame(window, padding=20)
main_frame.pack(expand=True, fill=tk.BOTH)

token_label = ttk.Label(main_frame, text="Authentication Token:")
token_label.pack(anchor=tk.W)
token_entry = ttk.Entry(main_frame)
token_entry.pack(fill=tk.X, pady=(0, 10))

execute_button = ttk.Button(main_frame, text="Login", command=execute_command_thread)
execute_button.pack(pady=(0, 10))

progress_var = tk.IntVar()
progress_bar = ttk.Progressbar(main_frame, variable=progress_var, maximum=100, mode='determinate')
progress_label_var = tk.StringVar()
progress_label = ttk.Label(main_frame, textvariable=progress_label_var)

load_values()
fetch_clipboard_content()

if autoLogin == "true":
    execute_command_thread()

window.mainloop()
