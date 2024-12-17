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
correct = [0]
index_task = 0


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
        correct[index_task] = 1
        mark_task_complete()
        update_completed_tasks_label()
    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка в коде: {str(e)}")


# Функция для сохранения кода в файл
def save_code(code):
    file_path = filedialog.asksaveasfilename(defaultextension=".py", filetypes=[("Python Files", "*.py")])
    if file_path:
        with open(file_path, "w") as file:
            file.write(code)
        messagebox.showinfo("Сохранение", "Код успешно сохранён.")



# Функция для загрузки кода из файла
def load_code():
    file_path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py")])
    if file_path:
        with open(file_path, "r") as file:
            return file.read()
    return None

# Функция для загрузки задач из файла
def load_tasks_from_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        corr = 0
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                lines = file.readlines()
                tasks = []
                current_task = {}
                for line in lines:
                    line = line.strip()
                    if line.startswith("#TASK_DESCRIPTION:"):
                        current_task["description"] = line.replace("#TASK_DESCRIPTION:", "").strip()
                    elif line.startswith("#TASK_THEORY:"):
                        current_task["theory"] = line.replace("#TASK_THEORY:", "").strip()
                    elif line.startswith("#TASK_TEMPLATE:"):
                        current_task["template"] = line.replace("#TASK_TEMPLATE:", "").strip()
                    elif line.startswith("#END_TASK"):
                        current_task["validation"] = lambda local_vars: isinstance(local_vars.get('result'), np.ndarray)
                        tasks.append(current_task)
                        current_task = {}
                    corr += 1
                    if corr == 4:
                        correct.append(0)
                        corr = 0
                return tasks
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при загрузке задач: {str(e)}")
    return []

def exi():
    exit()
def mark_task_complete():
    global completed_label
    completed_label.configure(text="Статус: Выполнено", foreground="green")
def update_completed_tasks_label():
    global completed_tasks_label
    completed_tasks_label.configure(text=f"Выполнено заданий: {correct.count(1)}")

# Функция запуска тренажёра
def run_trainer():
    global TASKS

    def change_task(task_index):
        current_task = TASKS[task_index]
        global  index_task
        index_task = task_index
        if correct[index_task] == 0:
            completed_label.configure(text="Статус: Не выполнено", foreground="red")
        else:
            completed_label.configure(text="Статус: Выполнено", foreground="green")
        reset_code()
        theory_text.configure(state="normal")
        theory_text.delete("1.0", tk.END)
        theory_text.insert("1.0", current_task["theory"])
        theory_text.configure(state="disabled")
        task_text.configure(text=current_task["description"])
        code_text.delete("1.0", tk.END)
        code_text.insert("1.0", current_task["template"])

    def submit_code():
        user_code = code_text.get("1.0", tk.END)
        check_code(user_code, current_task["validation"])

    def reset_code():
        code_text.delete("1.0", tk.END)
        code_text.insert("1.0", current_task["template"])

    def save_current_code():
        user_code = code_text.get("1.0", tk.END)
        save_code(user_code)

    def load_saved_code():
        loaded_code = load_code()
        if loaded_code:
            code_text.delete("1.0", tk.END)
            code_text.insert("1.0", loaded_code)



    def load_tasks():
        # nonlocal TASKS
        new_tasks = load_tasks_from_file()
        if new_tasks:
            for i in new_tasks:
                TASKS.append(i)
            task_selector["values"] = [f"Задача {i + 1}" for i in range(len(TASKS))]
            task_selector.current(0)
            change_task(0)



    # Создание окна
    root = tk.Tk()
    root.title("Учебный тренажёр по нечёткой логике")
    # Список задач
    task_selector_label = ttk.Label(root, text="Выберите задачу:", font=("Arial", 12))
    task_selector_label.pack(pady=5)
    task_selector = ttk.Combobox(root, values=[f"Задача {i + 1}" for i in range(len(TASKS))])
    task_selector.current(0)
    task_selector.pack(pady=5)
    task_selector.bind("<<ComboboxSelected>>", lambda e: change_task(task_selector.current()))
    load_tasks_button = ttk.Button(root, text="Загрузить задачи из файла", command=load_tasks)
    load_tasks_button.pack(pady=5)
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
    # Статус выполнения задания
    global completed_label
    completed_label = ttk.Label(root, text="Статус: Не выполнено", foreground="red", font=("Arial", 12))
    completed_label.pack(pady=5)
    # Поле для кода
    code_label = ttk.Label(root, text="Ваш код:", font=("Arial", 14, "bold"))
    code_label.pack(pady=5)
    code_text = scrolledtext.ScrolledText(root, width=70, height=15)
    code_text.insert("1.0", TASKS[0]["template"])
    code_text.pack(pady=10)
    # количество выполненных заданий
    global completed_tasks_label
    completed_tasks_label = ttk.Label(root, text=f"Выполнено заданий: {correct.count(1)}", font=("Arial", 12))
    completed_tasks_label.pack(pady=5)
    # Кнопки управления
    button_frame = ttk.Frame(root)
    button_frame.pack(pady=10)
    submit_button = ttk.Button(button_frame, text="Проверить код", command=submit_code)
    submit_button.grid(row=0, column=0, padx=5)
    reset_button = ttk.Button(button_frame, text="Сбросить код", command=reset_code)
    reset_button.grid(row=0, column=1, padx=5)
    save_button = ttk.Button(button_frame, text="Сохранить код", command=save_current_code)
    save_button.grid(row=0, column=2, padx=5)
    load_button = ttk.Button(button_frame, text="Загрузить код", command=load_saved_code)
    load_button.grid(row=0, column=3, padx=5)
    load_button = ttk.Button(button_frame, text="Выход", command=exi)
    load_button.grid(row=0, column=4, padx=5)
    root.mainloop()
# Функция отображения готовности задания
def mark_task_complete():
    global completed_label
    completed_label.configure(text="Статус: Выполнено", foreground="green")
def update_completed_tasks_label():
    global completed_tasks_label
    completed_tasks_label.configure(text=f"Выполнено заданий: {correct.count(1)}")


if __name__ == "__main__":
    run_trainer()
