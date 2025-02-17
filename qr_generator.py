import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, colorchooser
from PIL import Image, ImageTk, ImageDraw, ImageFont
import qrcode
import os
import time
import threading

__version__ = "1.3.0"

translations = {
    "ru": {
        "title": f"Генератор QR-кодов - QRGen v{__version__}",
        "input_label": "Введите текст:",
        "generate_button": "Сгенерировать QR-код",
        "save_button": "Сохранить QR-код",
        "clear_button": "Очистить",
        "generate_status": "QR-код успешно сгенерирован за {time:.2f} сек.",
        "save_status": "QR-код сохранен ({size} байт)",
        "error_empty_input": "Поле ввода не может быть пустым!",
        "history_title": "История QR-кодов",
        "customize_qr": "Настройки QR-кода",
        "dot_style": "Стиль точек",
        "bg_color": "Цвет фона",
        "dot_color": "Цвет точек",
        "upload_logo": "Загрузить логотип",
        "apply_customizations": "Применить настройки",
        "history_empty": "История пуста.",
        "error_correction": "Коррекция ошибок",
        "add_text": "Добавить текст",
        "text_label": "Текст:",
        "text_position": "Позиция текста:",
        "text_color": "Цвет текста:",
        "template_label": "Шаблоны",
        "template_social": "Социальные сети",
        "template_business": "Визитка",
    },
    "en": {
        "title": f"QR Code Generator - QRGen v{__version__}",
        "input_label": "Enter text:",
        "generate_button": "Generate QR Code",
        "save_button": "Save QR Code",
        "clear_button": "Clear",
        "generate_status": "QR Code successfully generated in {time:.2f} sec.",
        "save_status": "QR Code saved ({size} bytes)",
        "error_empty_input": "Input field cannot be empty!",
        "history_title": "QR Code History",
        "customize_qr": "Customize QR Code",
        "dot_style": "Dot Style",
        "bg_color": "Background Color",
        "dot_color": "Dot Color",
        "upload_logo": "Upload Logo",
        "apply_customizations": "Apply Customizations",
        "history_empty": "History is empty.",
        "error_correction": "Error Correction",
        "add_text": "Add Text",
        "text_label": "Text:",
        "text_position": "Text Position:",
        "text_color": "Text Color:",
        "template_label": "Templates",
        "template_social": "Social Media",
        "template_business": "Business Card",
    },
}

current_language = "ru"

class QRGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title(translations[current_language]["title"])
        self.root.resizable(True, True)
        self.qr_history = []
        self.qr_dot_style = "square"
        self.qr_back_color = "white"
        self.qr_fill_color = "black"
        self.qr_logo = None
        self.qr_error_correction = qrcode.constants.ERROR_CORRECT_H
        self.qr_text = ""
        self.qr_text_color = "black"
        self.qr_text_position = "bottom"
        self.setup_ui()

    def setup_ui(self):
        self.label = tk.Label(self.root, text=translations[current_language]["input_label"], font=("Arial", 12))
        self.label.pack(pady=5)

        self.entry = tk.Entry(self.root, width=50, font=("Arial", 12))
        self.entry.pack(pady=5)

        self.generate_button = tk.Button(self.root, text=translations[current_language]["generate_button"], font=("Arial", 12), command=self.generate_qr)
        self.generate_button.pack(pady=5)

        self.save_button = tk.Button(self.root, text=translations[current_language]["save_button"], font=("Arial", 12), command=self.save_qr)
        self.save_button.pack(pady=5)

        self.clear_button = tk.Button(self.root, text=translations[current_language]["clear_button"], font=("Arial", 12), command=self.clear_all)
        self.clear_button.pack(pady=5)

        self.qr_label = tk.Label(self.root)
        self.qr_label.pack(pady=5)

        self.status_label = tk.Label(self.root, text="", font=("Arial", 12))
        self.status_label.pack(pady=5)

        self.history_button = tk.Button(self.root, text=translations[current_language]["history_title"], font=("Arial", 12), command=self.view_history)
        self.history_button.pack(pady=5)

        self.customize_button = tk.Button(self.root, text=translations[current_language]["customize_qr"], font=("Arial", 12), command=self.customize_qr)
        self.customize_button.pack(pady=5)

        self.template_button = tk.Button(self.root, text=translations[current_language]["template_label"], font=("Arial", 12), command=self.apply_template)
        self.template_button.pack(pady=5)

        self.setup_menu()

    def setup_menu(self):
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Exit", command=self.root.quit)

        language_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Language", menu=language_menu)
        language_menu.add_command(label="Русский", command=lambda: self.change_language("ru"))
        language_menu.add_command(label="English", command=lambda: self.change_language("en"))

    def generate_qr(self):
        data = self.entry.get()
        if not data:
            messagebox.showerror("Ошибка", translations[current_language]["error_empty_input"])
            return

        self.status_label.config(text="Генерация QR-кода...")
        self.root.update_idletasks()

        def generate():
            start_time = time.time()

            qr = qrcode.QRCode(version=1, box_size=10, border=5, error_correction=self.qr_error_correction)
            qr.add_data(data)
            qr.make(fit=True)

            img = qr.make_image(fill_color=self.qr_fill_color, back_color=self.qr_back_color)

            if self.qr_logo:
                logo_size = int(img.size[0] / 4)
                logo = self.qr_logo.resize((logo_size, logo_size))
                img.paste(logo, (int(img.size[0] / 2 - logo_size / 2), int(img.size[1] / 2 - logo_size / 2)))

            if self.qr_text:
                draw = ImageDraw.Draw(img)
                font = ImageFont.load_default()
                text_position = (10, img.size[1] - 30) if self.qr_text_position == "bottom" else (10, 10)
                draw.text(text_position, self.qr_text, fill=self.qr_text_color, font=font)

            img_tk = ImageTk.PhotoImage(img)
            self.qr_label.config(image=img_tk)
            self.qr_label.image = img_tk

            end_time = time.time()
            time_taken = end_time - start_time
            self.status_label.config(text=translations[current_language]["generate_status"].format(time=time_taken))

            self.qr_history.append({"data": data, "time": time_taken})

        threading.Thread(target=generate).start()

    def save_qr(self):
        data = self.entry.get()
        if not data:
            messagebox.showerror("Ошибка", translations[current_language]["error_empty_input"])
            return

        qr = qrcode.QRCode(version=1, box_size=10, border=5, error_correction=self.qr_error_correction)
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color=self.qr_fill_color, back_color=self.qr_back_color)

        if self.qr_logo:
            logo_size = int(img.size[0] / 4)
            logo = self.qr_logo.resize((logo_size, logo_size))
            img.paste(logo, (int(img.size[0] / 2 - logo_size / 2), int(img.size[1] / 2 - logo_size / 2)))

        if self.qr_text:
            draw = ImageDraw.Draw(img)
            font = ImageFont.load_default()
            text_position = (10, img.size[1] - 30) if self.qr_text_position == "bottom" else (10, 10)
            draw.text(text_position, self.qr_text, fill=self.qr_text_color, font=font)

        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("SVG files", "*.svg")])
        if file_path:
            img.save(file_path)
            file_size = os.path.getsize(file_path)
            self.status_label.config(text=translations[current_language]["save_status"].format(size=file_size))

    def clear_all(self):
        self.entry.delete(0, tk.END)
        self.qr_label.config(image="")
        self.qr_label.image = None
        self.status_label.config(text="")

    def view_history(self):
        history_window = tk.Toplevel(self.root)
        history_window.title(translations[current_language]["history_title"])

        history_list = tk.Listbox(history_window, width=80, height=20)
        history_list.pack(pady=10)

        if not self.qr_history:
            history_list.insert(tk.END, translations[current_language]["history_empty"])
        else:
            for entry in self.qr_history:
                history_list.insert(tk.END, f"{entry['data']} - {entry['time']:.2f} sec")

    def customize_qr(self):
        customize_window = tk.Toplevel(self.root)
        customize_window.title(translations[current_language]["customize_qr"])

        # Dot style selection
        dot_style_var = tk.StringVar(value=self.qr_dot_style)
        dot_style_label = tk.Label(customize_window, text=translations[current_language]["dot_style"])
        dot_style_label.pack(pady=5)
        dot_style_menu = tk.OptionMenu(customize_window, dot_style_var, "square", "circle")
        dot_style_menu.pack(pady=5)

        # Background color selection
        bg_color_button = tk.Button(customize_window, text=translations[current_language]["bg_color"], command=self.select_bg_color)
        bg_color_button.pack(pady=5)

        # Dot color selection
        dot_color_button = tk.Button(customize_window, text=translations[current_language]["dot_color"], command=self.select_dot_color)
        dot_color_button.pack(pady=5)

        # Logo upload
        logo_button = tk.Button(customize_window, text=translations[current_language]["upload_logo"], command=self.upload_logo)
        logo_button.pack(pady=5)

        # Error correction level
        error_correction_label = tk.Label(customize_window, text=translations[current_language]["error_correction"])
        error_correction_label.pack(pady=5)
        error_correction_var = tk.StringVar(value="H")
        error_correction_menu = tk.OptionMenu(customize_window, error_correction_var, "L", "M", "Q", "H")
        error_correction_menu.pack(pady=5)

        # Add text
        text_label = tk.Label(customize_window, text=translations[current_language]["text_label"])
        text_label.pack(pady=5)
        self.text_entry = tk.Entry(customize_window, width=30)
        self.text_entry.pack(pady=5)

        text_color_button = tk.Button(customize_window, text=translations[current_language]["text_color"], command=self.select_text_color)
        text_color_button.pack(pady=5)

        text_position_var = tk.StringVar(value="bottom")
        text_position_label = tk.Label(customize_window, text=translations[current_language]["text_position"])
        text_position_label.pack(pady=5)
        text_position_menu = tk.OptionMenu(customize_window, text_position_var, "bottom", "top")
        text_position_menu.pack(pady=5)

        def apply_customizations():
            self.qr_dot_style = dot_style_var.get()
            self.qr_error_correction = getattr(qrcode.constants, f"ERROR_CORRECT_{error_correction_var.get()}")
            self.qr_text = self.text_entry.get()
            self.qr_text_position = text_position_var.get()
            customize_window.destroy()

        apply_button = tk.Button(customize_window, text=translations[current_language]["apply_customizations"], command=apply_customizations)
        apply_button.pack(pady=5)

    def select_bg_color(self):
        color = colorchooser.askcolor(title="Выберите цвет фона")[1]
        if color:
            self.qr_back_color = color

    def select_dot_color(self):
        color = colorchooser.askcolor(title="Выберите цвет точек")[1]
        if color:
            self.qr_fill_color = color

    def select_text_color(self):
        color = colorchooser.askcolor(title="Выберите цвет текста")[1]
        if color:
            self.qr_text_color = color

    def upload_logo(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")])
        if file_path:
            self.qr_logo = Image.open(file_path)
            messagebox.showinfo("Загрузка логотипа", "Логотип успешно загружен!")

    def apply_template(self):
        template_window = tk.Toplevel(self.root)
        template_window.title(translations[current_language]["template_label"])

        social_button = tk.Button(template_window, text=translations[current_language]["template_social"], command=lambda: self.use_template("https://example.com/social"))
        social_button.pack(pady=5)

        business_button = tk.Button(template_window, text=translations[current_language]["template_business"], command=lambda: self.use_template("https://example.com/business"))
        business_button.pack(pady=5)

    def use_template(self, template):
        self.entry.delete(0, tk.END)
        self.entry.insert(0, template)

    def change_language(self, lang_code):
        global current_language
        current_language = lang_code
        self.root.title(translations[current_language]["title"])
        self.label.config(text=translations[current_language]["input_label"])
        self.generate_button.config(text=translations[current_language]["generate_button"])
        self.save_button.config(text=translations[current_language]["save_button"])
        self.clear_button.config(text=translations[current_language]["clear_button"])
        self.status_label.config(text="")
        self.history_button.config(text=translations[current_language]["history_title"])
        self.customize_button.config(text=translations[current_language]["customize_qr"])
        self.template_button.config(text=translations[current_language]["template_label"])

def main():
    root = tk.Tk()
    app = QRGeneratorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()