import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import skfuzzy as fuzz
import numpy as np


# Проверка кода
def check_code(user_code):
    try:
        # Создаём пространство для выполнения кода
        local_vars = {}
        exec(user_code, {"fuzz": fuzz, "np": np}, local_vars)

        # Проверяем результат выполнения
        if 'result' not in local_vars:
            raise ValueError("Переменная 'result' не определена.")
        if isinstance(local_vars['result'], np.ndarray):
            messagebox.showinfo("Результат", "Правильно! Вы успешно дополнили код.")
        else:
            raise ValueError("Результат имеет неправильный формат.")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка в коде: {str(e)}")


# Функция запуска тренажёра
def run_trainer():
    def submit_code():
        user_code = code_text.get("1.0", tk.END)
        check_code(user_code)

    # Создание окна
    root = tk.Tk()
    root.title("Учебный тренажёр по нечёткой логике")

    # Описание задачи
    task_label = ttk.Label(
        root,
        text="Задача: Дополните код для создания треугольной функции принадлежности.\n"
             "Функция должна быть задана для пространства universe = np.arange(0, 11, 1)."
    )
    task_label.pack(pady=10)

    # Поле для кода
    code_text = scrolledtext.ScrolledText(root, width=70, height=15)
    code_text.insert(
        "1.0",
        (
            "# Пространство\n"
            "universe = np.arange(0, 11, 1)\n\n"
            "# Дополните код для создания функции принадлежности\n"
            "membership_function = fuzz.trimf(universe, [0, 5, 10])\n"
            "\n"
            "# Создайте переменную result, чтобы она равнялась\n"
            "# результату применения функции принадлежности\n"
            "result = \n"
        )
    )
    code_text.pack(pady=10)

    # Кнопка для проверки
    submit_button = ttk.Button(root, text="Проверить код", command=submit_code)
    submit_button.pack(pady=10)

    root.mainloop()


if __name__ == "__main__":
    run_trainer()