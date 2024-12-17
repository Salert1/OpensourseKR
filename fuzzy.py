import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import skfuzzy as fuzz
import numpy as np

# Список задач
TASKS = [
    {
        "description": (
            "Задача 1: Дополните код для создания треугольной функции принадлежности.\n"
            "Функция должна быть задана для пространства universe = np.arange(0, 11, 1)."
        ),
        "theory": (
            "Теория:\n"
            "Функции принадлежности в нечёткой логике описывают степень принадлежности элементов множества.\n"
            "Треугольная функция принадлежности задаётся тремя параметрами [a, b, c], где:\n"
            "  - a: начало\n"
            "  - b: вершина\n"
            "  - c: конец треугольника.\n"
            "\nПример: fuzz.trimf(universe, [0, 5, 10]) создаёт треугольник с вершиной в 5."
        ),
        "template": (
            "# Пространство\n"
            "universe = np.arange(0, 11, 1)\n\n"
            "# Дополните код для создания функции принадлежности\n"
            "membership_function = fuzz.trimf(universe, [0, 5, 10])\n\n"
            "# Создайте переменную result, чтобы она равнялась\n"
            "# результату применения функции принадлежности\n"
            "result = \n"
        ),
        "validation": lambda local_vars: isinstance(local_vars.get('result'), np.ndarray)
    }
]
current_task = TASKS[0]

# Проверка кода
def check_code(user_code, validation_func):
    try:
        # Создаём пространство для выполнения кода
        local_vars = {}
        exec(user_code, {"fuzz": fuzz, "np": np}, local_vars)

        # Проверяем результат выполнения через функцию проверки
        if not validation_func(local_vars):
            raise ValueError("Результат имеет неправильный формат или значение.")

        messagebox.showinfo("Результат", "Правильно! Вы успешно дополнили код.")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка в коде: {str(e)}")


# Функция для сохранения кода в файл
def save_code(code):
    file_path = filedialog.asksaveasfilename(defaultextension=".py", filetypes=[("Python Files", "*.py")])
    if file_path:
        with open(file_path, "w") as file:
            file.write(code)
        messagebox.showinfo("Сохранение", "Код успешно сохранён.")


# Функция запуска тренажёра
def run_trainer():
    global TASKS


    def submit_code():
        user_code = code_text.get("1.0", tk.END)
        check_code(user_code, current_task["validation"])

    def reset_code():
        code_text.delete("1.0", tk.END)
        code_text.insert("1.0", current_task["template"])

    def save_current_code():
        user_code = code_text.get("1.0", tk.END)
        save_code(user_code)

    # Создание окна
    root = tk.Tk()
    root.title("Учебный тренажёр по нечёткой логике")

    # Список задач




    # Теория
    theory_label = ttk.Label(root, text="Теория:", font=("Arial", 14, "bold"))
    theory_label.pack(pady=5)
    theory_text = scrolledtext.ScrolledText(root, width=70, height=10, state="disabled", wrap=tk.WORD)
    theory_text.pack(pady=5)
    theory_text.configure(state="normal")
    theory_text.insert("1.0", TASKS[0]["theory"])
    theory_text.configure(state="disabled")

    # Описание задачи
    task_label = ttk.Label(root, text="Задача:", font=("Arial", 14, "bold"))
    task_label.pack(pady=5)
    task_text = ttk.Label(root, text=TASKS[0]["description"], wraplength=500)
    task_text.pack(pady=5)

    # Поле для кода
    code_label = ttk.Label(root, text="Ваш код:", font=("Arial", 14, "bold"))
    code_label.pack(pady=5)
    code_text = scrolledtext.ScrolledText(root, width=70, height=15)
    code_text.insert("1.0", TASKS[0]["template"])
    code_text.pack(pady=10)

    # Кнопки управления
    button_frame = ttk.Frame(root)
    button_frame.pack(pady=10)

    submit_button = ttk.Button(button_frame, text="Проверить код", command=submit_code)
    submit_button.grid(row=0, column=0, padx=5)

    reset_button = ttk.Button(button_frame, text="Сбросить код", command=reset_code)
    reset_button.grid(row=0, column=1, padx=5)

    save_button = ttk.Button(button_frame, text="Сохранить код", command=save_current_code)
    save_button.grid(row=0, column=2, padx=5)

    root.mainloop()

if __name__ == "__main__":
    run_trainer()

