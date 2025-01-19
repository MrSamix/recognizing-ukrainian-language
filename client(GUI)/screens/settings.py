import tkinter as tk
from tkinter import ttk
from list_of_microphones import set_array_microphones
from list_of_languages import return_list_of_avaibable_languages_native
from dotenv import load_dotenv, find_dotenv, set_key
import os

load_dotenv(find_dotenv())

if not load_dotenv(find_dotenv()):
    with open('.env', 'w') as env_file:
        env_file.write('UUID=\n')
        env_file.write('LAST_LANGUAGE=\n')
        env_file.write('LAST_MIC=\n')
        env_file.write('SERVER_IP=\n')
        env_file.write('SERVER_PORT=\n')
    load_dotenv(find_dotenv())

language = os.getenv('LAST_LANGUAGE')
if language is None:
    language = "Auto"
    set_key(find_dotenv(), 'LAST_LANGUAGE', language)

mic = os.getenv('LAST_MIC')
if mic is None:
    mic = set_array_microphones()[0]
    set_key(find_dotenv(), 'LAST_MIC', mic)

server_ip = os.getenv('SERVER_IP')
server_port = os.getenv('SERVER_PORT')

def check_valid_ip_port():
    if server_ip is None or server_port is None or server_ip == "" or server_port == "":
        return False
    return True


def settings():
    selector_window = tk.Toplevel()
    selector_window.resizable(False, False)
    selector_window.title("Налаштування")
    # selector_window.iconbitmap("settings.ico") # мініфріз на початку відкриття вікна

    # mic
    mic_label = tk.Label(selector_window, text="Оберiть мiкрофон:")
    mic_label.pack(pady=5)

    mic_list = ttk.Combobox(selector_window, values=set_array_microphones(), width=50, state="readonly")
    if mic in set_array_microphones():
        mic_list.current(set_array_microphones().index(mic))
    else:
        mic_list.current(0)
    mic_list.pack(pady=5, padx=10)

    # language
    language_label = tk.Label(selector_window, text="Оберіть мову розпiзнавання:")
    language_label.pack(pady=5)

    language_list = ttk.Combobox(selector_window, values=return_list_of_avaibable_languages_native(), width=50, state="readonly")
    if language in return_list_of_avaibable_languages_native():
        language_list.current(return_list_of_avaibable_languages_native().index(language))
    else:
        language_list.current(0)
    language_list.pack(pady=5, padx=10)

    ttk.Separator(selector_window, orient="horizontal").pack(fill="x")

    # ip settings
    ip_frame = tk.Frame(selector_window)
    ip_frame.pack(pady=5, padx=10, fill="x")

    ip_label = tk.Label(ip_frame, text="IP сервера:")
    ip_label.pack(side="left")

    ip_entry = ttk.Entry(ip_frame, width=50)
    ip_entry.insert(0, server_ip)
    ip_entry.pack(side="right", fill="x", expand=True)

    # port settings
    port_frame = tk.Frame(selector_window)
    port_frame.pack(pady=5, padx=10, fill="x")

    port_label = tk.Label(port_frame, text="Порт сервера:")
    port_label.pack(side="left")

    port_entry = ttk.Entry(port_frame, width=50)
    port_entry.insert(0, server_port)
    port_entry.pack(side="right", fill="x", expand=True)

    def apply_changes():
        global mic, language, server_ip, server_port
        mic = mic_list.get()
        language = language_list.get()
        server_ip = ip_entry.get()
        server_port = port_entry.get()
        set_key(find_dotenv(), 'LAST_MIC', mic)
        set_key(find_dotenv(), 'LAST_LANGUAGE', language)
        set_key(find_dotenv(), 'SERVER_IP', server_ip)
        set_key(find_dotenv(), 'SERVER_PORT', server_port)
        selector_window.destroy()

    def cancel_changes():
        selector_window.destroy()

    btn_frame = tk.Frame(selector_window)
    btn_frame.pack(pady=5)

    ok_button = ttk.Button(btn_frame, text="ОК", command=apply_changes)
    ok_button.pack(side="left", padx=5)

    cancel_button = ttk.Button(btn_frame, text="Відміна", command=cancel_changes)
    cancel_button.pack(side="left", padx=5)

    selector_window.update_idletasks()
    w = selector_window.winfo_reqwidth()
    h = selector_window.winfo_reqheight()
    x = (selector_window.winfo_screenwidth() // 2) - (w // 2)
    y = (selector_window.winfo_screenheight() // 2) - (h // 2) - 50
    selector_window.geometry(f"+{x}+{y}")
