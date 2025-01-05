# import tkinter as tk

# # Функція для закриття вікна
# def close_window():
#     root.destroy()

# # Створення головного вікна
# root = tk.Tk()

# # Вимикаємо рамки та стандартні кнопки
# root.overrideredirect(True)

# # Встановлюємо розмір і розташування вікна
# root.geometry("300x100+500+300")  # 300x100 - розмір, 500+300 - позиція на екрані

# # Додаємо текст до вікна
# label = tk.Label(root, text="Це вікно зникне через 3 секунди", font=("Arial", 12))
# label.pack(expand=True)

# # Налаштовуємо таймер на 3 секунди
# root.after(3000, close_window)

# # Запускаємо цикл програми
# root.mainloop()




import tkinter as tk

def show_window():
    """Анімація появи вікна знизу."""
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    window_width = 300
    window_height = 100

    # Початкова позиція вікна (знизу екрана, поза видимістю)
    x = (screen_width - window_width) // 2
    y = screen_height

    # Встановлюємо розмір і початкову позицію
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # Анімація підйому вікна
    def animate_up():
        nonlocal y
        if y > screen_height - window_height - 60:  # Зупинити анімацію на потрібній позиції
            y -= 10
            root.geometry(f"{window_width}x{window_height}+{x}+{y}")
            root.after(10, animate_up)
        else:
            # Таймер на автоматичне закриття через 3 секунди
            root.after(3000, animate_down)

    animate_up()

def animate_down():
    """Анімація зникнення вікна вниз."""
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    window_width = 300
    window_height = 100

    x = (screen_width - window_width) // 2
    y = screen_height - window_height - 50  # Поточна позиція вікна

    # Анімація з'їжджання вниз
    def move_down():
        nonlocal y
        if y < screen_height:  # Зупинити анімацію, коли вікно повністю зникне
            y += 10
            root.geometry(f"{window_width}x{window_height}+{x}+{y}")
            root.after(10, move_down)
        else:
            close_window()  # Закрити вікно після анімації

    move_down()

def close_window():
    """Закриття вікна."""
    root.destroy()

# Створення головного вікна
root = tk.Tk()

# Вимикаємо рамки вікна
root.overrideredirect(True)

# Додаємо текст до вікна
label = tk.Label(root, text="Це вікно з'являється та зникає плавно!", font=("Arial", 12))
label.pack(expand=True)

# Запускаємо анімацію
show_window()

# Запускаємо головний цикл
root.mainloop()
