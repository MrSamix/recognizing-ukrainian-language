from tkinter import messagebox

def show_info():
    messagebox.showinfo("Інформація", "Ця програма була створена в рамках курсової роботи.\n\nВ цій програмі ви можете транскрибувати текст, для цього вам потрібно мати сервер транскрибації, мікрофон та інтернет з'єднання, якщо сервер не знаходиться на вашому комп'ютері.\n\nВАЖЛИВО! Перед початком повноційної роботи з програмою, переконайтеся, що вибрали правильний мікрофон для запису, мову розпізнавання, та вказали вірну IP адресу та Port серверу!\n\nДля початку запису натисніть на кнопку 'Запис', яка знаходиться по центру вікна або комбінацію клавіш \n'Ctrl + /' та починайте диктувати.\n\nДля закінчення запису натисніть на цю ж кнопку.\n\nДля виходу натисніть на хрестик в правому верхньому куті програми.")