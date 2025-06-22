
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import time
import math
import threading
from datetime import datetime
from plyer import notification
import requests

GROQ_API_KEY = "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"  # 🔁 Replace this with your actual key
GROQ_MODEL = "llama3-70b-8192"  # Or another available model

# --------------------- MAIN APP WINDOW ---------------------
app = tk.Tk()
app.title("📘 Study Planner")
app.geometry("1000x600")
app.configure(bg="#121212")

# --------------------- TABS ---------------------
notebook = ttk.Notebook(app)
notebook.pack(expand=True, fill="both")

style = ttk.Style()
style.theme_use("clam")
style.configure("TNotebook", background="#121212", borderwidth=0)
style.configure("TNotebook.Tab", font=("Segoe UI", 10, "bold"), padding=[12, 8], background="#1e1e1e", foreground="white")
style.map("TNotebook.Tab", background=[("selected", "#00acc1")])

task_tab = tk.Frame(notebook, bg="#121212")
completed_tab = tk.Frame(notebook, bg="#121212")
timer_tab = tk.Frame(notebook, bg="#121212")
chat_tab = tk.Frame(notebook, bg="#121212")

notebook.add(task_tab, text="📝 Tasks")
notebook.add(completed_tab, text="✅ Completed")
notebook.add(timer_tab, text="⏰ Timer & Clock")
notebook.add(chat_tab, text="🧠 AI Chatbot")

# --------------------- TASKS TAB ---------------------
tasks_frame = tk.Frame(task_tab, bg="#121212")
tasks_frame.pack(pady=20)

task_entry = tk.Entry(tasks_frame, font=("Segoe UI", 12), width=40)
task_entry.grid(row=0, column=0, padx=10)

def mark_task_complete(task_text):
    now = datetime.now()
    date = now.strftime("%d %b %Y")
    time_str = now.strftime("%I:%M %p")
    completed_table.insert("", "end", values=(task_text, date, time_str))

def add_task():
    task_text = task_entry.get()
    if task_text:
        var = tk.IntVar()
        chk = tk.Checkbutton(tasks_list_frame, text=task_text, variable=var, font=("Segoe UI", 12),
                             bg="#121212", fg="white", selectcolor="#1e1e1e", activebackground="#1e1e1e",
                             command=lambda: [chk.destroy(), mark_task_complete(task_text)])
        chk.pack(anchor="w", pady=2)
        task_entry.delete(0, tk.END)

add_btn = tk.Button(tasks_frame, text="Add Task", command=add_task, bg="#2196f3", fg="white",
                    font=("Segoe UI", 10, "bold"), padx=10, pady=5)
add_btn.grid(row=0, column=1)

tasks_list_frame = tk.Frame(task_tab, bg="#121212")
tasks_list_frame.pack(pady=10)

# --------------------- COMPLETED TAB ---------------------
completed_header = tk.Label(completed_tab, text="✅ Completed Tasks", font=("Segoe UI", 18, "bold"),
                            bg="#121212", fg="#00e676")
completed_header.pack(pady=10)

table_frame = tk.Frame(completed_tab, bg="#121212")
table_frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

tree_scroll_y = tk.Scrollbar(table_frame)
tree_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

tree_scroll_x = tk.Scrollbar(table_frame, orient=tk.HORIZONTAL)
tree_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)

completed_table = ttk.Treeview(table_frame, yscrollcommand=tree_scroll_y.set, xscrollcommand=tree_scroll_x.set,
                               columns=("Task", "Date", "Time"), show="headings", selectmode="browse")
completed_table.pack(fill=tk.BOTH, expand=True)

tree_scroll_y.config(command=completed_table.yview)
tree_scroll_x.config(command=completed_table.xview)

style.configure("Treeview", background="#1e1e1e", foreground="white", rowheight=28, fieldbackground="#1e1e1e",
                font=("Segoe UI", 11))
style.configure("Treeview.Heading", font=("Segoe UI", 12, "bold"), background="#00acc1", foreground="white")

completed_table.heading("Task", text="Task")
completed_table.heading("Date", text="Date")
completed_table.heading("Time", text="Time")

completed_table.column("Task", anchor=tk.W, width=300)
completed_table.column("Date", anchor=tk.CENTER, width=100)
completed_table.column("Time", anchor=tk.CENTER, width=100)

# --------------------- TIMER & CLOCK TAB ---------------------
timer_running = False
start_time = 0

def run_stopwatch():
    global start_time, timer_running
    start_time = time.time()
    timer_running = True
    update_stopwatch()

def update_stopwatch():
    if timer_running:
        elapsed = int(time.time() - start_time)
        mins, secs = divmod(elapsed, 60)
        stopwatch_label.config(text=f"{mins:02}:{secs:02}")
        timer_tab.after(1000, update_stopwatch)

def stop_stopwatch():
    global timer_running
    timer_running = False

def start_timer(minutes):
    def countdown():
        global timer_running
        for i in range(minutes * 60, -1, -1):
            if not timer_running:
                break
            mins, secs = divmod(i, 60)
            stopwatch_label.config(text=f"{mins:02}:{secs:02}")
            time.sleep(1)
        if timer_running:
            notification.notify(title="Time's Up!", message="Take a 5-minute break!", timeout=5)
    global timer_running
    timer_running = True
    threading.Thread(target=countdown, daemon=True).start()

stopwatch_label = tk.Label(timer_tab, text="00:00", font=("Consolas", 40, "bold"), bg="#121212", fg="#00e5ff")
stopwatch_label.pack(pady=(20, 10))

btn_frame = tk.Frame(timer_tab, bg="#121212")
btn_frame.pack(pady=10)

style_btn = {"width": 15, "font": ("Segoe UI", 11, "bold"), "padx": 8, "pady": 6, "bd": 0}

tk.Button(btn_frame, text="⏱️ Stopwatch", command=run_stopwatch, bg="#43a047", fg="white", **style_btn).grid(row=0, column=0, padx=6)
tk.Button(btn_frame, text="⛔ Stop", command=stop_stopwatch, bg="#e53935", fg="white", **style_btn).grid(row=0, column=1, padx=6)
tk.Button(btn_frame, text="⏲️ Timer (5m)", command=lambda: start_timer(5), bg="#1e88e5", fg="white", **style_btn).grid(row=0, column=2, padx=6)
tk.Button(btn_frame, text="📖 Start Study (25m)", command=lambda: start_timer(25), bg="#8e24aa", fg="white", **style_btn).grid(row=0, column=3, padx=6)

canvas_frame = tk.Frame(timer_tab, bg="#121212")
canvas_frame.pack(pady=20)

canvas = tk.Canvas(canvas_frame, width=220, height=220, bg="#1c1c1c", highlightthickness=0)
canvas.pack()

def draw_clock():
    canvas.delete("all")
    now = datetime.now()
    canvas.create_oval(10, 10, 210, 210, outline="#bbbbbb", width=2)
    for i in range(12):
        angle = math.pi / 6 * i
        x = 110 + 90 * math.sin(angle)
        y = 110 - 90 * math.cos(angle)
        canvas.create_text(x, y, text=str(i if i > 0 else 12), fill="white", font=("Segoe UI", 10, "bold"))

    hour = now.hour % 12
    minute = now.minute
    second = now.second

    hour_angle = math.pi / 6 * hour + math.pi / 360 * minute
    canvas.create_line(110, 110, 110 + 40 * math.sin(hour_angle), 110 - 40 * math.cos(hour_angle), fill="white", width=5)

    minute_angle = math.pi / 30 * minute
    canvas.create_line(110, 110, 110 + 60 * math.sin(minute_angle), 110 - 60 * math.cos(minute_angle), fill="white", width=3)

    second_angle = math.pi / 30 * second
    canvas.create_line(110, 110, 110 + 70 * math.sin(second_angle), 110 - 70 * math.cos(second_angle), fill="#00e676", width=2)

    timer_tab.after(1000, draw_clock)

draw_clock()

# --------------------- AI CHATBOT TAB ---------------------
chat_header = tk.Label(chat_tab, text="🤖 AI Study Assistant", font=("Segoe UI", 20, "bold"),
                       bg="#121212", fg="#00bcd4")
chat_header.pack(pady=10)

chat_frame = tk.Frame(chat_tab, bg="#121212")
chat_frame.pack(pady=10)

chat_display = scrolledtext.ScrolledText(chat_frame, width=80, height=20, bg="#1c1c1c", fg="white",
                                         font=("Consolas", 11), wrap=tk.WORD, relief=tk.FLAT, bd=2)
chat_display.pack(pady=5)

input_frame = tk.Frame(chat_tab, bg="#121212")
input_frame.pack(pady=10)

chat_entry = tk.Entry(input_frame, width=60, font=("Segoe UI", 12), bg="#eeeeee", relief=tk.FLAT)
chat_entry.grid(row=0, column=0, ipady=6, padx=5)

def ask_groq(prompt):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "messages": [
            {"role": "system", "content": "You are a helpful study assistant for a 14-year-old student."},
            {"role": "user", "content": prompt}
        ],
        "model": GROQ_MODEL,
        "temperature": 0.7
    }

    response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=data)

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        raise Exception(f"Groq API error: {response.status_code} - {response.text}")


def send_query():
    query = chat_entry.get()
    if not query:
        return
    chat_display.insert(tk.END, f"\n🧑 You: {query}\n", "user")
    chat_display.see(tk.END)
    chat_entry.delete(0, tk.END)
    threading.Thread(target=ask_ai, args=(query,), daemon=True).start()

def ask_ai(prompt):
    try:
        response = ask_groq(prompt)
        chat_display.insert(tk.END, f"\n🤖 AI: {response.strip()}\n", "bot")
        chat_display.see(tk.END)
    except Exception as e:
        chat_display.insert(tk.END, f"\n[Error] {str(e)}\n", "error")
        chat_display.see(tk.END)

ask_btn = tk.Button(input_frame, text="🧠 Ask", command=send_query, font=("Segoe UI", 11, "bold"),
                    bg="#2196f3", fg="white", activebackground="#1976d2", bd=0, padx=12, pady=4)
ask_btn.grid(row=0, column=1, padx=5)

chat_display.tag_config("user", foreground="#90caf9")
chat_display.tag_config("bot", foreground="#81c784")
chat_display.tag_config("error", foreground="#e57373")

app.mainloop()
