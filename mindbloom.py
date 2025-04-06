import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from PIL import Image, ImageTk
import random
import json
import os

# --------------------- JSON Persistence ---------------------
DATA_FILE = "users.json"

def show_points_table():
    table_window = tk.Toplevel(root)
    table_window.title("🏆 Points Table")
    table_window.geometry("300x400")
    table_window.configure(bg="#F0F8FF")

    title = tk.Label(table_window, text="🌟 Users Points Table", font=("Helvetica", 14, "bold"), bg="#F0F8FF")
    title.pack(pady=10)

    for username, data in users_data.items():
        entry = f"{username}: {data.get('score', 0)} pts"
        label = tk.Label(table_window, text=entry, font=("Helvetica", 12), bg="#F0F8FF")
        label.pack(pady=2)


def load_user_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_user_data():
    with open(DATA_FILE, "w") as f:
        json.dump(users_data, f, indent=4)

users_data = load_user_data()

# --------------------- GUI Setup ---------------------
root = tk.Tk()
root.title("🌸 MindBloom - Interactive Self-Care Game 🌸")
root.geometry("480x700")
root.configure(bg="#FAF8F0")

# Ask for username
user_name = simpledialog.askstring("Welcome!", "🌼 What's your name?")
if not user_name:
    user_name = "Guest"

if user_name not in users_data:
    users_data[user_name] = {
        "score": 0,
        "plant_stage": 0
    }

# --------------------- Load Images ---------------------
plant_images = []
for i in range(5):
    img = Image.open(f"plant_{i}.png").resize((200, 200))
    plant_images.append(ImageTk.PhotoImage(img))

# Game variables for current user
score = users_data[user_name]["score"]
plant_stage = users_data[user_name]["plant_stage"]
unlocked_vouchers = []
milestones = [10, 20, 30]

# Actions
actions = [
     "💧 Drank water", "🏃‍♀️ Exercise", "📓 Journaling", "🌞 Sunshine",
    "🧘‍♂️ Meditated", "🍏 Ate healthy", "🎵 Music", "🛌 Slept well"
]

# --------------------- GUI Layout ---------------------
title_frame = tk.Frame(root, bg="#D8EFD3", pady=10)
title_frame.pack(fill="x")

tk.Label(
    title_frame, text="🌸 MindBloom 🌸",
    font=("Helvetica", 22, "bold"),
    bg="#D8EFD3", fg="#2E5339"
).pack()

tk.Label(
    title_frame, text=f"Welcome, {user_name}!",
    font=("Helvetica", 14), bg="#D8EFD3"
).pack()
tk.Button(root, text="🚪 Exit Game", bg="tomato", fg="white", command=root.destroy).pack(pady=10)
tk.Button(root, text="📊 Show Points Table", bg="#4CAF50", fg="white", font=("Helvetica", 12),
          command=show_points_table).pack(pady=10)

# Plant Display
plant_frame = tk.Frame(root, bg="#FAF8F0")
plant_frame.pack()
plant_label = tk.Label(plant_frame, image=plant_images[plant_stage], bg="#FAF8F0")
plant_label.pack(pady=10)

# Progress Bar
tk.Label(root, text="🌱 Growth Progress", font=("Helvetica", 12), bg="#FAF8F0").pack()
progress = ttk.Progressbar(root, length=350, maximum=30)
progress['value'] = score
progress.pack(pady=5)

# Score Label
status_label = tk.Label(root, text=f"💚 Wellness Score: {score}", font=("Helvetica", 13), bg="#FAF8F0")
status_label.pack(pady=10)

# --------------------- Game Functions ---------------------
def show_points_table():
    table_window = tk.Toplevel(root)
    table_window.title("🏆 Points Table")
    table_window.geometry("300x400")
    table_window.configure(bg="#F0F8FF")

    title = tk.Label(table_window, text="🌟 Users Points Table", font=("Helvetica", 14, "bold"), bg="#F0F8FF")
    title.pack(pady=10)

    for username, data in users_data.items():
        entry = f"{username}: {data.get('score', 0)} pts"
        label = tk.Label(table_window, text=entry, font=("Helvetica", 12), bg="#F0F8FF")
        label.pack(pady=2)

def save_current_user():
    users_data[user_name]["score"] = score
    users_data[user_name]["plant_stage"] = plant_stage
    save_user_data()

def log_action(action_text):
    global score, plant_stage
    score += 1
    status_label.config(text=f"💚 Wellness Score: {score}")
    progress['value'] = score

    if score % 5 == 0 and plant_stage < len(plant_images) - 1:
        plant_stage += 1
        plant_label.config(image=plant_images[plant_stage])

    if score % 4 == 0:
        play_mini_game()

    if score in milestones and score not in unlocked_vouchers:
        unlocked_vouchers.append(score)
        messagebox.showinfo("🎁 Achievement!", f"Voucher Unlocked at {score} points!")

    save_current_user()

def update_ui():
    global score, plant_stage
    score = users_data[user_name]['score']
    status_label.config(text=f"💚 Wellness Score: {score}")
    progress['value'] = score
    plant_stage = min(score // 5, len(plant_images) - 1)
    plant_label.config(image=plant_images[plant_stage])

def save_user_data():
    with open("users.json", "w") as f:
        json.dump(users_data, f, indent=4)


def play_mini_game():
    wordle_window = tk.Toplevel(root)
    wordle_window.title("🟩 Wordle Mini-Game 🟨")
    wordle_window.geometry("420x450")
    wordle_window.configure(bg="#FFFBEF")

    word_list = ["plant", "happy", "shine", "light", "green", "smile", "water"]
    target_word = random.choice(word_list)
    attempts = []

    tk.Label(wordle_window, text="Guess the 5-letter word!", font=("Helvetica", 14), bg="#FFFBEF").pack(pady=10)

    entry = tk.Entry(wordle_window, font=("Helvetica", 16), justify="center")
    entry.pack(pady=10)

    feedback_frame = tk.Frame(wordle_window, bg="#FFFBEF")
    feedback_frame.pack()

    def check_word():
        guess = entry.get().lower()
        entry.delete(0, tk.END)

        if len(guess) != 5 or not guess.isalpha():
            messagebox.showwarning("Invalid", "Please enter a valid 5-letter word.")
            return

        row = tk.Frame(feedback_frame, bg="#FFFBEF")
        for i in range(5):
            letter = guess[i].upper()
            correct_letter = target_word[i]

            if letter.lower() == correct_letter:
                bg_color = "#9CCC65"  # Green
            elif letter.lower() in target_word:
                bg_color = "#FFF176"  # Yellow
            else:
                bg_color = "#E0E0E0"  # Gray

            lbl = tk.Label(row, text=letter, width=4, height=2, font=("Helvetica", 16, "bold"), bg=bg_color)
            lbl.pack(side="left", padx=2)
        row.pack(pady=3)

        attempts.append(guess)

        if guess == target_word:
            messagebox.showinfo("🎉 Congrats!", "You guessed it right! +3 bonus points!")
            # Add 3 extra points to current user
            users_data[user_name]['score'] += 3
            save_user_data()
            update_ui()
            wordle_window.destroy()

        elif len(attempts) >= 6:
            messagebox.showinfo("🔚 Game Over", f"The word was: {target_word}")
            wordle_window.destroy()

    submit_btn = tk.Button(wordle_window, text="Submit", command=check_word)
    submit_btn.pack(pady=10)


def add_bonus_points():
    global score
    score += 3
    progress['value'] = score
    status_label.config(text=f"💚 Wellness Score: {score}")
    save_current_user()

# --------------------- Action Buttons ---------------------
tk.Label(root, text="✅ Choose your self-care action:", font=("Helvetica", 12), bg="#FAF8F0").pack(pady=10)

action_frame = tk.Frame(root, bg="#FAF8F0")
action_frame.pack()

for i, act in enumerate(actions):
    row = i // 2
    col = i % 2
    btn = tk.Button(action_frame, text=act, width=20, font=("Helvetica", 10), command=lambda a=act: log_action(a))
    btn.grid(row=row, column=col, padx=10, pady=5)
# --------------------- Controls ---------------------

root.mainloop()
