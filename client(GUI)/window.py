import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from screens.settings import settings, check_valid_ip_port
from screens.info import show_info
from main import start_threads, stop_threads, starts_recording, stops_recording, initilizing
import keyboard as kb
import callback_handler

import time

is_recording = False
thread_record = None
thread_send = None

def start_recording():
    global is_recording, thread_record, thread_send
    label = tk.Label(main_frame, font=("Arial", 16), bg="#2E2E2E", fg="white")
    label.place(x=65, y=40)
    if not check_valid_ip_port():
        messagebox.showerror("Помилка", "IP або порт сервера не вказаний! Будь ласка, вкажіть їх у налаштуваннях.")
        return
    if not is_recording:
        mic_btn.config(bg="red", fg="white")
        is_recording = True
        initilizing()
        starts_recording()
        thread_record, thread_send = start_threads()
        label.config(text="Розпізнавання...")
    else:
        mic_btn.config(bg="#2E2E2E", fg="#00ADEF")
        stops_recording()
        stop_threads()
        label.config(text="Запис зупинено!")
        is_recording = False
        callback_handler.set_error_handling(False)


def start_recording_with_delay():
    if is_recording:
        start_recording()


def close_window():
    if is_recording:
        if messagebox.askokcancel("Йде запис", "Ви впевнені, що хочете вийти?"):
            stops_recording()
            stop_threads()
            animate_close()
    else:
        animate_close()

def animate_window(): # Анімація появи вікна
    global y
    if y > target_y:  # Якщо вікно ще не досягло кінцевої позиції
        y -= 10
        root.geometry(f"{width}x{height}+{x}+{y}")
        root.after(5, animate_window)  # Повторюємо через 5 мс
    else:
        root.geometry(f"{width}x{height}+{x}+{target_y}")  # Фіксуємо позицію

def animate_close(): # Анімація закриття вікна
    global y
    if y < screen_height:  # Якщо вікно ще не вийшло за межі екрану
        y += 10
        root.geometry(f"{width}x{height}+{x}+{y}")
        root.after(3, animate_close)  # Повторюємо через 3 мс
    else:
        root.destroy()  # Закриваємо вікно

# Створення головного вікна
root = tk.Tk()
root.title("Програма транскрибування мови")
root.overrideredirect(True)  # Видалити стандартну рамку вікна

style = ttk.Style(root)
style.theme_use('winnative')

width, height = 300, 200
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x = (screen_width - width) // 2  # Відцентрувати по горизонталі
y = screen_height  
target_y = screen_height - height - 50


root.geometry(f"{width}x{height}+{x}+{y}")
root.attributes("-topmost", True)
root.attributes("-alpha", 0.95)  # Прозорість вікна

main_frame = tk.Frame(root, bg="#2E2E2E", width=width, height=height, relief="raised", bd=0)
main_frame.place(x=0, y=0)


# Іконка "Закрити"
close_btn = tk.Button(main_frame, text="✖", font=("Arial", 12), bg="#2E2E2E", fg="white", borderwidth=0, command=close_window)
close_btn.place(x=260, y=10)

# Кнопка для мікрофона
mic_frame = tk.Frame(main_frame, bg="#2E2E2E", highlightbackground="#00ADEF", highlightthickness=2, width=80, height=80)
mic_frame.place(x=125, y=100) # byv 60
mic_btn = tk.Button(mic_frame, text="🎤", font=("Arial", 20), bg="#2E2E2E", fg="#00ADEF", borderwidth=0, command=start_recording)
mic_btn.pack(expand=True, fill="both")

# Кнопка "Інформація"
info_btn = tk.Button(main_frame, text="❓", font=("Arial", 14), bg="#2E2E2E", fg="white", borderwidth=0, command=show_info)
info_btn.place(x=230, y=120)

# Кнопка "Налаштування"
settings_btn = tk.Button(main_frame, text="⚙️", font=("Arial", 14), bg="#2E2E2E", fg="white", borderwidth=0, command=settings)
settings_btn.place(x=30, y=120)

# Анімація появи вікна
animate_window()

# Keyboard
kb.add_hotkey('Ctrl + /', lambda: start_recording())

# Встановлюємо функцію зворотного виклику для обробки помилок
callback_handler.set_error_callback(start_recording_with_delay)

root.mainloop()
