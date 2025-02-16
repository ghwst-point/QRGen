import tkinter as tk
import qrcode
from PIL import ImageTk, Image
from tkinter import filedialog
import time
import os

__version__ = "1.1.0" # Версия приложения

# Словарь для хранения текстовых элементов интерфейса
translations = {
    "ru": {
        "title": f"Генератор QR-кодов - QRGen v{__version__}",
        "input_label": "Введите текст:",
        "generate_button": "Сгенерировать QR-код",
        "save_button": "Сохранить QR-код",
        "clear_button": "Очистить",
        "generate_status": "QR-код успешно сгенерирован за {time:.2f} сек.",
        "save_status": "QR-код сохранен ({size} байт)",
        "about_title": "О программе",
        "about_message": f"Генератор QR-кодов - QRGen v{__version__}\nАвтор: [Ваше имя]\n[Описание программы]"
    },
    "en": {
        "title": f"QR Code Generator - QRGen v{__version__}",
        "input_label": "Enter text:",
        "generate_button": "Generate QR Code",
        "save_button": "Save QR Code",
        "clear_button": "Clear",
        "generate_status": "QR Code successfully generated in {time:.2f} sec.",
        "save_status": "QR Code saved ({size} bytes)",
        "about_title": "About",
        "about_message": f"QR Code Generator - QRGen v{__version__}\nAuthor: [Your name]\n[Program description]"
    },
}

current_language = "ru" # язык по умолчанию

def update_ui():
    """Обновляет текст интерфейса на основе выбранного языка."""
    lang = translations[current_language]
    root.title(lang["title"])
    label.config(text=lang["input_label"])
    generate_button.config(text=lang["generate_button"])
    save_button.config(text=lang["save_button"])
    clear_button.config(text=lang["clear_button"])

def generate_qr():
    """Генерирует QR-код из введенного текста."""
    data = entry.get()
    if data:
        start_time = time.time()
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        img_tk = ImageTk.PhotoImage(img)
        qr_label.config(image=img_tk)
        qr_label.image = img_tk

        end_time = time.time()
        time_taken = end_time - start_time
        status_label.config(text=translations[current_language]["generate_status"].format(time=time_taken))
        entry.delete(0, tk.END)

def save_qr():
    """Сохраняет QR-код в файл."""
    data = entry.get()
    if data:
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if file_path:
            img.save(file_path)
            file_size = os.path.getsize(file_path)
            status_label.config(text=translations[current_language]["save_status"].format(size=file_size))
            entry.delete(0, tk.END)

def clear_all():
    """Очищает поле ввода и метку QR-кода."""
    entry.delete(0, tk.END)
    qr_label.config(image="")
    qr_label.image = None
    status_label.config(text="")

def change_language(lang):
    """Изменяет язык интерфейса."""
    global current_language
    current_language = lang
    update_ui()

def show_about():
    """Показывает окно 'About'."""
    lang = translations[current_language]
    about_window = tk.Toplevel(root)
    about_window.title(lang["about_title"])
    about_label = tk.Label(about_window, text=lang["about_message"], padx=20, pady=20)
    about_label.pack()

# Создаем главное окно
root = tk.Tk()
update_ui() # Устанавливаем язык интерфейса при запуске

# Добавляем иконку
try:
    root.iconbitmap("icon.ico")
except tk.TclError:
    pass

# Создаем метку для ввода текста
label = tk.Label(root, font=("Arial", 12))
label.pack(pady=5)

# Создаем поле ввода текста
entry = tk.Entry(root, width=50, font=("Arial", 12))
entry.pack(pady=5)

# Создаем кнопки
generate_button = tk.Button(root, font=("Arial", 12), command=generate_qr)
generate_button.pack(pady=5)

save_button = tk.Button(root, font=("Arial", 12), command=save_qr)
save_button.pack(pady=5)

clear_button = tk.Button(root, font=("Arial", 12), command=clear_all)
clear_button.pack(pady=5)

# Создаем метку для отображения QR-кода
qr_label = tk.Label(root)
qr_label.pack(pady=5)

# Создаем метку для статуса
status_label = tk.Label(root, text="", font=("Arial", 12))
status_label.pack(pady=5)

# Создаем меню
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# Меню "File"
file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Exit", command=root.quit)

# Меню "Language"
language_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Language", menu=language_menu)
language_menu.add_command(label="Русский", command=lambda: change_language("ru"))
language_menu.add_command(label="English", command=lambda: change_language("en"))

# Меню "About"
about_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="About", menu=about_menu)
about_menu.add_command(label="About", command=show_about)

# Запускаем главный цикл обработки событий
root.mainloop()