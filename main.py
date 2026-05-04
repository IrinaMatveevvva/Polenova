import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
from datetime import datetime

HISTORY_FILE = 'tasks_history.json'

class RandomTaskGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Task Generator")
        self.root.geometry("650x500")

        # Предопределенный список задач
        self.all_tasks = [
            {"task": "Прочитать статью по криптографии", "type": "Учёба"},
            {"task": "Сделать 20 приседаний", "type": "Спорт"},
            {"task": "Написать отчет по практике", "type": "Работа"},
            {"task": "Изучить новый алгоритм шифрования", "type": "Учёба"},
            {"task": "Размять шею и спину", "type": "Спорт"},
            {"task": "Проверить электронную почту", "type": "Работа"}
        ]
        
        self.history = self.load_history()
        self.setup_ui()

    def setup_ui(self):
        # --- Панель генерации задач ---
        frame_gen = ttk.LabelFrame(self.root, text="Генератор", padding=10)
        frame_gen.pack(padx=10, pady=10, fill="x")

        ttk.Label(frame_gen, text="Выберите тип:").grid(row=0, column=0, padx=5, pady=5)
        self.combo_type = ttk.Combobox(frame_gen, values=["Все", "Учёба", "Спорт", "Работа"], state="readonly")
        self.combo_type.set("Все")
        self.combo_type.grid(row=0, column=1, padx=5, pady=5)

        self.btn_generate = ttk.Button(frame_gen, text="Сгенерировать задачу", command=self.generate_task)
        self.btn_generate.grid(row=0, column=2, padx=15, pady=5)

        # Вывод сгенерированной задачи
        self.lbl_result = ttk.Label(self.root, text="Нажмите кнопку, чтобы получить задачу", font=("Arial", 12, "bold"))
        self.lbl_result.pack(pady=10)

        # --- Панель добавления новых задач ---
        frame_add = ttk.LabelFrame(self.root, text="Добавить новую задачу", padding=10)
        frame_add.pack(padx=10, pady=5, fill="x")

        ttk.Label(frame_add, text="Название:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_new_task = ttk.Entry(frame_add, width=30)
        self.entry_new_task.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame_add, text="Тип:").grid(row=0, column=2, padx=5, pady=5)
        self.combo_new_type = ttk.Combobox(frame_add, values=["Учёба", "Спорт", "Работа"], state="readonly")
        self.combo_new_type.set("Учёба")
        self.combo_new_type.grid(row=0, column=3, padx=5, pady=5)

        self.btn_add_task = ttk.Button(frame_add, text="Добавить", command=self.add_task)
        self.btn_add_task.grid(row=0, column=4, padx=10, pady=5)

        # --- История ---
        frame_hist = ttk.LabelFrame(self.root, text="История сгенерированных задач", padding=10)
        frame_hist.pack(padx=10, pady=10, fill="both", expand=True)

        self.tree = ttk.Treeview(frame_hist, columns=("date", "task", "type"), show="headings")
        self.tree.heading("date", text="Дата и время")
        self.tree.heading("task", text="Задача")
        self.tree.heading("type", text="Тип")
        
        self.tree.column("date", width=120, anchor="center")
        self.tree.column("type", width=80, anchor="center")
        
        self.tree.pack(fill="both", expand=True)
        self.refresh_table()

    def generate_task(self):
        selected_type = self.combo_type.get()
        
        if selected_type == "Все":
            available_tasks = self.all_tasks
        else:
            available_tasks = [t for t in self.all_tasks if t["type"] == selected_type]

        if not available_tasks:
            messagebox.showwarning("Внимание", "Нет задач для выбранного типа!")
            return

        chosen_task = random.choice(available_tasks)
        self.lbl_result.config(text=f"{chosen_task['type']}: {chosen_task['task']}")

        # Добавление в историю
        new_entry = {
            "date": datetime.now().strftime("%d.%m.%Y %H:%M"),
            "task": chosen_task["task"],
            "type": chosen_task["type"]
        }
        self.history.append(new_entry)
        self.save_history()
        self.refresh_table()

    def add_task(self):
        new_task_text = self.entry_new_task.get().strip()
        new_task_type = self.combo_new_type.get()

        if not new_task_text:
            messagebox.showwarning("Ошибка ввода", "Поле новой задачи не должно быть пустым!")
            return

        self.all_tasks.append({"task": new_task_text, "type": new_task_type})
        messagebox.showinfo("Успех", f"Задача '{new_task_text}' успешно добавлена!")
        self.entry_new_task.delete(0, tk.END)

    def load_history(self):
        try:
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_history(self):
        with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.history, f, ensure_ascii=False, indent=2)

    def refresh_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for h in reversed(self.history):
            self.tree.insert("", "end", values=(h['date'], h['task'], h['type']))


if __name__ == "__main__":
    root = tk.Tk()
    app = RandomTaskGenerator(root)
    root.mainloop()