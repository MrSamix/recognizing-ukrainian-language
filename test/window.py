import tkinter as tk
from tkinter import messagebox

is_recording = False

def start_recording():
    global is_recording
    if not is_recording:
        mic_btn.config(bg="red", fg="white")
        messagebox.showinfo("Запис", "Запис з мікрофона розпочато!")
        is_recording = True
    else:
        mic_btn.config(bg="#2E2E2E", fg="#00ADEF")
        is_recording = False
        messagebox.showinfo("Запис", "Запис з мікрофона завершено!")
    """Функція для початку запису з мікрофона."""

def show_info():
    """Функція для відображення інформації."""
    messagebox.showinfo("Інформація", "Це тестова інформація!")

def show_settings():
    """Функція для відображення налаштувань мікрофона."""
    messagebox.showinfo("Налаштування", "Тут буде список мікрофонів.")

def close_window():
    """Запускає анімацію зникнення вниз."""
    animate_close()

def animate_window():
    """Анімація появи вікна знизу."""
    global y
    if y > target_y:  # Якщо вікно ще не досягло кінцевої позиції
        y -= 10
        root.geometry(f"{width}x{height}+{x}+{y}")
        root.after(5, animate_window)  # Повторюємо через 10 мс
    else:
        root.geometry(f"{width}x{height}+{x}+{target_y}")  # Фіксуємо позицію

def animate_close():
    """Анімація закриття вікна вниз."""
    global y
    if y < screen_height:  # Якщо вікно ще не вийшло за межі екрану
        y += 10
        root.geometry(f"{width}x{height}+{x}+{y}")
        root.after(3, animate_close)  # Повторюємо через 10 мс
    else:
        root.destroy()  # Закриваємо вікно

# Створення головного вікна
root = tk.Tk()
root.title("Мікрофон")
root.overrideredirect(True)  # Видалити стандартну рамку вікна

# Параметри вікна
width, height = 300, 200
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x = (screen_width - width) // 2  # Відцентрувати по горизонталі
y = screen_height  # Початкова позиція (поза екраном)
target_y = screen_height - height - 50  # Кінцева позиція

# Встановлення початкового розміру та позиції вікна
root.geometry(f"{width}x{height}+{x}+{y}")
root.attributes("-topmost", True)  # Завжди зверху
root.attributes("-alpha", 0.95)  # Прозорість вікна

# Головна рамка з закругленими краями
main_frame = tk.Frame(root, bg="#2E2E2E", width=width, height=height, relief="raised", bd=0)
main_frame.place(x=0, y=0)

# Іконка "Закрити"
close_btn = tk.Button(main_frame, text="✖", font=("Arial", 12), bg="#2E2E2E", fg="white", borderwidth=0, command=close_window)
close_btn.place(x=260, y=10)

# Кнопка для мікрофона (посередині, обведена колом)
mic_frame = tk.Frame(main_frame, bg="#2E2E2E", highlightbackground="#00ADEF", highlightthickness=2, width=80, height=80)
mic_frame.place(x=125, y=60)
mic_btn = tk.Button(mic_frame, text="🎤", font=("Arial", 20), bg="#2E2E2E", fg="#00ADEF", borderwidth=0, command=start_recording)
mic_btn.pack(expand=True, fill="both")

# Кнопка "Інформація" (праворуч)
info_btn = tk.Button(main_frame, text="❓", font=("Arial", 14), bg="#2E2E2E", fg="white", borderwidth=0, command=show_info)
info_btn.place(x=230, y=120)

# Кнопка "Налаштування" (ліворуч)
settings_btn = tk.Button(main_frame, text="⚙️", font=("Arial", 14), bg="#2E2E2E", fg="white", borderwidth=0, command=show_settings)
settings_btn.place(x=30, y=120)

# Запускаємо анімацію появи вікна
animate_window()

# Запускаємо головний цикл
root.mainloop()
