import tkinter as tk
import random
import time
from tkinter import messagebox, ttk

class MathQuiz:
    def __init__(self, root):
        self.root = root
        self.root.title("🧠 Mental Math Quiz 🎯")
        self.root.geometry("600x500")
        self.root.config(bg="#282c36")

        self.score = 0
        self.total_questions = 0
        self.current_question = 0
        self.history = []
        self.types_selected = []
        self.time_per_question = None
        self.max_questions = None
        self.time_left = None
        self.correct_answer = None

        self.create_main_menu()

    def create_main_menu(self):
        """Creates the quiz settings panel where the user selects options."""
        self.clear_window()
        tk.Label(self.root, text="🎯 Select Quiz Options 🏆", font=("Arial", 18, "bold"), bg="#282c36", fg="white").pack(pady=10)

        self.types_selected = []  

        self.addition_var = tk.BooleanVar()
        self.subtraction_var = tk.BooleanVar()
        self.multiplication_var = tk.BooleanVar()
        self.division_var = tk.BooleanVar()

        tk.Checkbutton(self.root, text="➕ Addition", variable=self.addition_var, bg="#282c36", fg="white", selectcolor="black").pack()
        tk.Checkbutton(self.root, text="➖ Subtraction", variable=self.subtraction_var, bg="#282c36", fg="white", selectcolor="black").pack()
        tk.Checkbutton(self.root, text="✖ Multiplication", variable=self.multiplication_var, bg="#282c36", fg="white", selectcolor="black").pack()
        tk.Checkbutton(self.root, text="➗ Division", variable=self.division_var, bg="#282c36", fg="white", selectcolor="black").pack()

        tk.Label(self.root, text="⏳ Time per question (seconds):", bg="#282c36", fg="white", font=("Arial", 12)).pack(pady=5)
        self.time_per_question_entry = tk.Entry(self.root, font=("Arial", 12))
        self.time_per_question_entry.pack()
        self.time_per_question_entry.insert(0, "10")  

        tk.Label(self.root, text="🔢 Total number of questions:", bg="#282c36", fg="white", font=("Arial", 12)).pack(pady=5)
        self.max_questions_entry = tk.Entry(self.root, font=("Arial", 12))
        self.max_questions_entry.pack()
        self.max_questions_entry.insert(0, "10")  

        tk.Button(self.root, text="🚀 Start Quiz", command=self.start_quiz, bg="green", fg="white", font=("Arial", 14)).pack(pady=15)

    def start_quiz(self):
        """Starts the quiz with the selected options."""
        self.types_selected = []
        if self.addition_var.get():
            self.types_selected.append("addition")
        if self.subtraction_var.get():
            self.types_selected.append("subtraction")
        if self.multiplication_var.get():
            self.types_selected.append("multiplication")
        if self.division_var.get():
            self.types_selected.append("division")

        if not self.types_selected:
            messagebox.showerror("Error", "❌ Select at least one question type!")
            return

        try:
            self.time_per_question = int(self.time_per_question_entry.get())
            self.max_questions = int(self.max_questions_entry.get())
        except ValueError:
            messagebox.showerror("Error", "⚠️ Enter valid numbers!")
            return

        self.score = 0
        self.total_questions = 0
        self.current_question = 0
        self.history = []

        self.ask_question()

    def ask_question(self):
        """Generates and displays a new question."""
        if self.current_question >= self.max_questions:
            self.end_quiz()
            return

        self.clear_window()
        self.current_question += 1
        question, self.correct_answer = self.generate_question()

        tk.Label(self.root, text=f"📌 Question {self.current_question}/{self.max_questions}", font=("Arial", 16), bg="#282c36", fg="yellow").pack(pady=5)
        tk.Label(self.root, text=question, font=("Arial", 22, "bold"), bg="#282c36", fg="white").pack(pady=10)

        self.answer_entry = tk.Entry(self.root, font=("Arial", 16))
        self.answer_entry.pack(pady=5)
        self.answer_entry.focus()

        tk.Button(self.root, text="✅ Submit", command=self.check_answer, bg="blue", fg="white", font=("Arial", 14)).pack(pady=10)
        tk.Button(self.root, text="❌ End Quiz", command=self.end_quiz, bg="red", fg="white", font=("Arial", 12)).pack(pady=5)

        self.time_left = self.time_per_question
        self.time_label = tk.Label(self.root, text=f"⏳ Time Left: {self.time_left} sec", font=("Arial", 12), bg="#282c36", fg="white")
        self.time_label.pack()

        self.time_bar = ttk.Progressbar(self.root, orient="horizontal", length=300, mode="determinate")
        self.time_bar.pack(pady=5)

        self.update_timer()

    def update_timer(self):
        """Updates the countdown timer and progress bar."""
        if self.time_left > 0:
            self.time_left -= 1
            self.time_label.config(text=f"⏳ Time Left: {self.time_left} sec")
            self.time_bar['value'] = (self.time_left / self.time_per_question) * 100
            self.root.after(1000, self.update_timer)
        else:
            self.check_answer(auto_fail=True)

    def generate_question(self):
        """Generates a random math question based on selected types."""
        num1 = random.randint(1, 20)
        num2 = random.randint(1, 20)
        q_type = random.choice(self.types_selected)

        if q_type == "addition":
            return f"{num1} + {num2} =", num1 + num2
        elif q_type == "subtraction":
            if random.choice([True, False]):  
                num1, num2 = num2, num1
            return f"{num1} - {num2} =", num1 - num2
        elif q_type == "multiplication":
            return f"{num1} × {num2} =", num1 * num2
        elif q_type == "division":
            num1 = num1 * num2  
            return f"{num1} ÷ {num2} =", num1 // num2

    def check_answer(self, auto_fail=False):
        """Checks the user's answer and updates the score."""
        if auto_fail:
            self.history.append((self.current_question, "❌ No Answer", self.correct_answer, False))
            self.ask_question()
            return

        user_answer = self.answer_entry.get().strip()
        try:
            user_answer = int(user_answer)
        except ValueError:
            messagebox.showerror("Error", "⚠️ Enter a valid number!")
            return

        is_correct = user_answer == self.correct_answer
        self.score += 1 if is_correct else 0
        self.history.append((self.current_question, user_answer, self.correct_answer, is_correct))

        self.ask_question()

    def end_quiz(self):
        """Displays the quiz results with a summary of correct and incorrect answers."""
        self.clear_window()
        tk.Label(self.root, text="🏆 Quiz Summary 🏆", font=("Arial", 18, "bold"), bg="#282c36", fg="white").pack(pady=10)
        tk.Label(self.root, text=f"🎯 Score: {self.score}/{self.max_questions}", font=("Arial", 16), bg="#282c36", fg="yellow").pack()

        for q_num, user_ans, correct_ans, is_correct in self.history:
            color = "green" if is_correct else "red"
            tk.Label(self.root, text=f"Q{q_num}: Your Ans: {user_ans} | Correct: {correct_ans}", fg=color, bg="#282c36", font=("Arial", 12)).pack()

        tk.Button(self.root, text="🔄 Restart", command=self.create_main_menu, bg="blue", fg="white", font=("Arial", 14)).pack(pady=10)
        tk.Button(self.root, text="❌ Exit", command=self.root.quit, bg="red", fg="white", font=("Arial", 14)).pack()

    def clear_window(self):
        """Removes all widgets from the window."""
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = MathQuiz(root)
    root.mainloop()
