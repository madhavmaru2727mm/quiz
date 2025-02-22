import tkinter as tk
from tkinter import ttk, messagebox
import random
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Math Quiz")
        self.root.geometry("800x600")
        self.root.configure(bg="#2E3440")  # Dark background for color grading

        # Variables
        self.difficulty_vars = {
            "Easy": tk.BooleanVar(value=False),
            "Medium": tk.BooleanVar(value=False),
            "Hard": tk.BooleanVar(value=False)
        }
        self.num_questions = tk.IntVar(value=10)
        self.enable_time = tk.BooleanVar(value=False)
        self.time_per_question = tk.IntVar(value=10)
        self.question_types = {
            "Addition": tk.BooleanVar(value=False),
            "Subtraction": tk.BooleanVar(value=False),
            "Multiplication": tk.BooleanVar(value=False),
            "Division": tk.BooleanVar(value=False)
        }

        self.questions = []
        self.current_question = 0
        self.correct_answers = 0
        self.incorrect_answers = 0
        self.unattempted = 0
        self.start_time = 0
        self.time_consumed = []

        self.create_first_panel()

    def create_first_panel(self):
        self.first_panel = tk.Frame(self.root, bg="#2E3440")
        self.first_panel.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Title
        title_label = tk.Label(self.first_panel, text="Math Quiz", bg="#2E3440", fg="#D8DEE9", font=("Arial", 24, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Difficulty Selection (Checkboxes)
        tk.Label(self.first_panel, text="Select Difficulty:", bg="#2E3440", fg="#D8DEE9", font=("Arial", 14)).grid(row=1, column=0, sticky="w", pady=5)
        for i, (difficulty, var) in enumerate(self.difficulty_vars.items()):
            ttk.Checkbutton(self.first_panel, text=difficulty, variable=var, style="Dark.TCheckbutton").grid(row=2, column=i, sticky="w", padx=5)

        # Number of Questions
        tk.Label(self.first_panel, text="Number of Questions:", bg="#2E3440", fg="#D8DEE9", font=("Arial", 14)).grid(row=3, column=0, sticky="w", pady=5)
        ttk.Entry(self.first_panel, textvariable=self.num_questions, style="Dark.TEntry").grid(row=3, column=1, sticky="ew", padx=5)

        # Enable Time Limit
        tk.Label(self.first_panel, text="Enable Time Limit:", bg="#2E3440", fg="#D8DEE9", font=("Arial", 14)).grid(row=4, column=0, sticky="w", pady=5)
        ttk.Checkbutton(self.first_panel, variable=self.enable_time, style="Dark.TCheckbutton").grid(row=4, column=1, sticky="w", padx=5)

        # Time per Question
        tk.Label(self.first_panel, text="Time per Question (seconds):", bg="#2E3440", fg="#D8DEE9", font=("Arial", 14)).grid(row=5, column=0, sticky="w", pady=5)
        ttk.Entry(self.first_panel, textvariable=self.time_per_question, style="Dark.TEntry").grid(row=5, column=1, sticky="ew", padx=5)

        # Question Types (Checkboxes)
        tk.Label(self.first_panel, text="Select Question Types:", bg="#2E3440", fg="#D8DEE9", font=("Arial", 14)).grid(row=6, column=0, sticky="w", pady=5)
        question_types_frame = tk.Frame(self.first_panel, bg="#2E3440")
        question_types_frame.grid(row=7, column=0, columnspan=2, sticky="w")

        ttk.Checkbutton(question_types_frame, text="Addition", variable=self.question_types["Addition"], style="Dark.TCheckbutton").grid(row=0, column=0, sticky="w", padx=5)
        ttk.Checkbutton(question_types_frame, text="Subtraction", variable=self.question_types["Subtraction"], style="Dark.TCheckbutton").grid(row=0, column=1, sticky="w", padx=5)
        ttk.Checkbutton(question_types_frame, text="Multiplication", variable=self.question_types["Multiplication"], style="Dark.TCheckbutton").grid(row=1, column=0, sticky="w", padx=5)
        ttk.Checkbutton(question_types_frame, text="Division", variable=self.question_types["Division"], style="Dark.TCheckbutton").grid(row=1, column=1, sticky="w", padx=5)

        # Start Quiz Button
        ttk.Button(self.first_panel, text="Start Quiz", command=self.start_quiz, style="Dark.TButton").grid(row=8, column=0, columnspan=2, pady=20)

        # Configure grid weights for responsive design
        for i in range(9):
            self.first_panel.grid_rowconfigure(i, weight=1)
        for j in range(2):
            self.first_panel.grid_columnconfigure(j, weight=1)

    def start_quiz(self):
        # Validate selections
        if not any(var.get() for var in self.difficulty_vars.values()):
            messagebox.showwarning("Warning", "Please select at least one difficulty level.")
            return
        if not any(var.get() for var in self.question_types.values()):
            messagebox.showwarning("Warning", "Please select at least one question type.")
            return

        self.questions = self.generate_questions()
        self.current_question = 0
        self.correct_answers = 0
        self.incorrect_answers = 0
        self.unattempted = 0
        self.time_consumed = []

        self.first_panel.destroy()
        self.create_quiz_panel()

    def generate_questions(self):
        questions = []
        for _ in range(self.num_questions.get()):
            # Select a random difficulty level
            selected_difficulty = random.choice([k for k, v in self.difficulty_vars.items() if v.get()])
            # Select a random question type
            q_type = random.choice([k for k, v in self.question_types.items() if v.get()])

            if q_type == "Addition":
                if selected_difficulty == "Easy":
                    a = random.randint(1, 50)
                    b = random.randint(1, 50)
                elif selected_difficulty == "Medium":
                    a = random.randint(50, 100)
                    b = random.randint(50, 100)
                else:  # Hard
                    a = random.randint(100, 200)
                    b = random.randint(100, 200)
                question = f"{a} + {b} = ?"
                answer = a + b
            elif q_type == "Subtraction":
                if selected_difficulty == "Easy":
                    a = random.randint(1, 50)
                    b = random.randint(1, a)
                elif selected_difficulty == "Medium":
                    a = random.randint(50, 100)
                    b = random.randint(1, a)
                else:  # Hard
                    a = random.randint(100, 200)
                    b = random.randint(1, a)
                question = f"{a} - {b} = ?"
                answer = a - b
            elif q_type == "Multiplication":
                if selected_difficulty == "Easy":
                    a = random.randint(1, 10)
                    b = random.randint(1, 10)
                elif selected_difficulty == "Medium":
                    a = random.randint(10, 20)
                    b = random.randint(10, 20)
                else:  # Hard
                    a = random.randint(20, 30)
                    b = random.randint(20, 30)
                question = f"{a} * {b} = ?"
                answer = a * b
            elif q_type == "Division":
                if selected_difficulty == "Easy":
                    a = random.randint(1, 50)
                    b = random.randint(1, a)
                    while a % b != 0:
                        b = random.randint(1, a)
                elif selected_difficulty == "Medium":
                    a = random.randint(50, 100)
                    b = random.randint(1, a)
                    while a % b != 0:
                        b = random.randint(1, a)
                else:  # Hard
                    a = random.randint(100, 200)
                    b = random.randint(1, a)
                    while a % b != 0:
                        b = random.randint(1, a)
                question = f"{a} / {b} = ?"
                answer = a // b
            questions.append((question, answer))
        return questions

    def create_quiz_panel(self):
        self.quiz_panel = tk.Frame(self.root, bg="#2E3440")
        self.quiz_panel.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        self.question_label = tk.Label(self.quiz_panel, text="", bg="#2E3440", fg="#D8DEE9", font=("Arial", 18))
        self.question_label.pack(pady=20)

        self.answer_entry = ttk.Entry(self.quiz_panel, font=("Arial", 14), style="Dark.TEntry")
        self.answer_entry.pack(pady=20)
        self.answer_entry.bind("<Return>", lambda event: self.next_question())  # Submit on Enter key

        self.timer_label = tk.Label(self.quiz_panel, text="", bg="#2E3440", fg="#D8DEE9", font=("Arial", 14))
        self.timer_label.pack(pady=10)

        self.next_button = ttk.Button(self.quiz_panel, text="Next", command=self.next_question, style="Dark.TButton")
        self.next_button.pack(pady=20)

        self.start_time = time.time()
        self.update_timer()
        self.show_question()

    def show_question(self):
        if self.current_question < len(self.questions):
            self.question_label.config(text=self.questions[self.current_question][0])
            self.answer_entry.delete(0, tk.END)
            self.start_time = time.time()
        else:
            self.show_stats()

    def next_question(self):
        user_answer = self.answer_entry.get()
        if user_answer:
            correct_answer = self.questions[self.current_question][1]
            if int(user_answer) == correct_answer:
                self.correct_answers += 1
            else:
                self.incorrect_answers += 1
            self.time_consumed.append(time.time() - self.start_time)
        else:
            self.unattempted += 1
            self.time_consumed.append(0)

        self.current_question += 1
        self.show_question()

    def update_timer(self):
        if self.enable_time.get() and self.current_question < len(self.questions):
            elapsed_time = time.time() - self.start_time
            remaining_time = max(0, self.time_per_question.get() - int(elapsed_time))
            self.timer_label.config(text=f"Time Left: {remaining_time} seconds")
            if remaining_time == 0:
                self.next_question()
            self.root.after(1000, self.update_timer)

    def show_stats(self):
        self.quiz_panel.destroy()
        self.create_stats_panel()

    def create_stats_panel(self):
        self.stats_panel = tk.Frame(self.root, bg="#2E3440")
        self.stats_panel.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        tk.Label(self.stats_panel, text="Quiz Statistics", bg="#2E3440", fg="#D8DEE9", font=("Arial", 24, "bold")).pack(pady=20)

        stats_text = f"Total Questions: {len(self.questions)}\n" \
                     f"Correct Answers: {self.correct_answers}\n" \
                     f"Incorrect Answers: {self.incorrect_answers}\n" \
                     f"Unattempted: {self.unattempted}"
        tk.Label(self.stats_panel, text=stats_text, bg="#2E3440", fg="#D8DEE9", font=("Arial", 14)).pack(pady=20)

        # Bar Chart
        fig, ax = plt.subplots()
        ax.bar(["Correct", "Incorrect", "Unattempted"], [self.correct_answers, self.incorrect_answers, self.unattempted], color=["#4CAF50", "#F44336", "#FFC107"])
        ax.set_ylabel("Number of Questions")
        ax.set_title("Quiz Results")

        canvas = FigureCanvasTkAgg(fig, master=self.stats_panel)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=20)

        # Restart Quiz Button
        ttk.Button(self.stats_panel, text="Restart Quiz", command=self.restart_quiz, style="Dark.TButton").pack(pady=20)

    def restart_quiz(self):
        self.stats_panel.destroy()
        self.create_first_panel()

if __name__ == "__main__":
    root = tk.Tk()
    style = ttk.Style()
    style.configure("Dark.TCheckbutton", background="#2E3440", foreground="#D8DEE9")
    style.configure("Dark.TEntry", fieldbackground="#3B4252", foreground="#D8DEE9")
    style.configure("Dark.TButton", background="#4C566A", foreground="#D8DEE9", font=("Arial", 12))
    app = QuizApp(root)
    root.mainloop()