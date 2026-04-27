import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import json
import os

HISTORY_FILE = "history.json"

class PasswordGeneratorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Random Password Generator")
        self.geometry("500x400")

        # 1. Настройки
        self.length_var = tk.IntVar(value=12)
        self.include_digits = tk.BooleanVar(value=True)
        self.include_letters = tk.BooleanVar(value=True)
        self.include_symbols = tk.BooleanVar(value=True)

        # 2. Верхняя панель: настройки создания пароля
        settings_frame = ttk.LabelFrame(self, text="Настройки пароля")
        settings_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(settings_frame, text="Длина:").grid(row=0, column=0, sticky="w")
        self.length_scale = ttk.Scale(settings_frame, from_=6, to=32, variable=self.length_var, orient="horizontal")
        self.length_scale.grid(row=0, column=1, sticky="ew", padx=5)
        settings_frame.columnconfigure(1, weight=1)
        ttk.Label(settings_frame, textvariable=self.length_var, width=3).grid(row=0, column=2)

        ttk.Checkbutton(settings_frame, text="Буквы", variable=self.include_letters).grid(row=1, column=0, sticky="w")
        ttk.Checkbutton(settings_frame, text="Цифры", variable=self.include_digits).grid(row=1, column=1, sticky="w")
        ttk.Checkbutton(settings_frame, text="Спецсимволы", variable=self.include_symbols).grid(row=1, column=2, sticky="w")

        # 3. Кнопка генерации
        gen_btn = ttk.Button(self, text="Сгенерировать", command=self.generate_password)
        gen_btn.pack(pady=10)

        # 4. Результат и история
        self.result_var = tk.StringVar()
        ttk.Entry(self, textvariable=self.result_var, font=("Arial", 14)).pack(fill="x", padx=10)

        self.history = []
        self.history_table = ttk.Treeview(self, columns=("password", "options"), show="headings")
        self.history_table.heading("password", text="Пароль")
        self.history_table.heading("options", text="Параметры")
        self.history_table.pack(expand=True, fill="both", padx=10, pady=10)

        self.load_history()

    def generate_password(self):
        length = self.length_var.get()
        if length < 6 or length > 32:
            messagebox.showerror("Ошибка", "Длина пароля от 6 до 32 символов")
            return
        pool = ""
        options = []
        if self.include_letters.get():
            pool += string.ascii_letters
            options.append("буквы")
        if self.include_digits.get():
            pool += string.digits
            options.append("цифры")
        if self.include_symbols.get():
            pool += string.punctuation
            options.append("спецсимволы")
        if not pool:
            messagebox.showwarning("Ошибка", "Выберите хотя бы один тип символов.")
            return

        password = ''.join(random.choice(pool) for _ in range(length))
        self.result_var.set(password)
        self.add_to_history(password, ", ".join(options))

    def add_to_history(self, password, options):
        self.history.append({"password": password, "options": options})
        self.history_table.insert("", "end", values=(password, options))
        self.save_history()

    # --- История ---
    def save_history(self):
        try:
            with open(HISTORY_FILE, "w", encoding="utf-8") as f:
                json.dump(self.history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print("Ошибка при сохранении истории:", e)

    def load_history(self):
        if os.path.exists(HISTORY_FILE):
            try:
                with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                    self.history = json.load(f)
                for h in self.history:
                    self.history_table.insert("", "end", values=(h["password"], h["options"]))
            except Exception as e:
                print("Ошибка при загрузке истории:", e)
                self.history = []

if __name__ == "__main__":
    app = PasswordGeneratorApp()
    app.mainloop()