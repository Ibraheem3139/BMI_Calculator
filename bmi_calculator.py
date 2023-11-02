import tkinter as tk
from tkinter import ttk
import sqlite3
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Database Initialization
conn = sqlite3.connect("bmi_data.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS bmi_records (
    id INTEGER PRIMARY KEY,
    name TEXT,
    weight REAL,
    height REAL,
    bmi REAL,
    date DATE
)
""")
conn.commit()

# Function to calculate BMI
def calculate_bmi():
    name = name_entry.get()
    weight = float(weight_entry.get())
    height = float(height_entry.get())
    bmi = weight / (height ** 2)

    cursor.execute("INSERT INTO bmi_records (name, weight, height, bmi, date) VALUES (?, ?, ?, ?, date('now'))", (name, weight, height, bmi))
    conn.commit()

    bmi_label.config(text=f"Your BMI: {bmi:.2f}")
    update_history()

# Function to update the history list
def update_history():
    history_tree.delete(*history_tree.get_children())
    cursor.execute("SELECT name, bmi, date FROM bmi_records ORDER BY date DESC")
    for row in cursor.fetchall():
        history_tree.insert("", "end", values=row)

# Function to show BMI trend
def show_bmi_trend():
    cursor.execute("SELECT date, bmi FROM bmi_records ORDER BY date")
    data = cursor.fetchall()
    dates = [row[0] for row in data]
    bmis = [row[1] for row in data]

    plt.figure(figsize=(6, 4))
    plt.plot(dates, bmis, marker='o')
    plt.title("BMI Trend Over Time")
    plt.xlabel("Date")
    plt.ylabel("BMI")
    plt.xticks(rotation=45)

    # Clear the existing canvas (if any) in trend_frame
    for widget in trend_frame.winfo_children():
        widget.destroy()

    canvas = FigureCanvasTkAgg(plt.gcf(), master=trend_frame)
    canvas.get_tk_widget().grid(row=1, column=0, columnspan=2)

    canvas.draw()  # Redraw the canvas

# GUI setup
root = tk.Tk()
root.title("BMI Calculator")

# Set the window size and position to center it on the screen
window_width = 800  # Set your desired window width
window_height = 600  # Set your desired window height

# Calculate the screen width and height to center the window
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)

# Use the 'geometry' method to set the window size and position
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Input frame
input_frame = ttk.Frame(root)
input_frame.pack(padx=10, pady=10, anchor='w')

name_label = ttk.Label(input_frame, text="Name:")
name_label.grid(row=0, column=0, sticky='w')
name_entry = ttk.Entry(input_frame)
name_entry.grid(row=0, column=1)

weight_label = ttk.Label(input_frame, text="Weight (kg):")
weight_label.grid(row=1, column=0, sticky='w')
weight_entry = ttk.Entry(input_frame)
weight_entry.grid(row=1, column=1)

height_label = ttk.Label(input_frame, text="Height (m):")
height_label.grid(row=2, column=0, sticky='w')
height_entry = ttk.Entry(input_frame)
height_entry.grid(row=2, column=1)

calculate_button = ttk.Button(input_frame, text="Calculate BMI", command=calculate_bmi)
calculate_button.grid(row=3, columnspan=2)

bmi_label = ttk.Label(input_frame, text="")
bmi_label.grid(row=4, columnspan=2)

# History frame
history_frame = ttk.Frame(root)
history_frame.pack(padx=10, pady=10, anchor='w')

history_label = ttk.Label(history_frame, text="BMI History")
history_label.grid(row=0, column=0, columnspan=3)

history_tree = ttk.Treeview(history_frame, columns=("Name", "BMI", "Date"))
history_tree.heading("#1", text="Name")
history_tree.heading("#2", text="BMI")
history_tree.heading("#3", text="Date")
history_tree.column("#1", width=100)
history_tree.column("#2", width=100)
history_tree.column("#3", width=100)
history_tree.grid(row=1, column=0, columnspan=3)

update_history()

# Trend frame
trend_frame = ttk.Frame(root)
trend_frame.pack(padx=10, pady=10, anchor='w')

trend_label = ttk.Label(trend_frame, text="BMI Trend Over Time")
trend_label.grid(row=0, column=0, columnspan=2)

trend_button = ttk.Button(trend_frame, text="Show Trend", command=show_bmi_trend)
trend_button.grid(row=1, column=0, columnspan=2)

root.mainloop()
