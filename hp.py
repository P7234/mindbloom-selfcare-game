import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from PIL import Image, ImageTk
import random

# Root window
root = tk.Tk()
root.title("🌸 MindBloom - Interactive Self-Care Game 🌸")
root.geometry("500x720")
root.configure(bg="#FAF8F0")

# Ask for user name
user_name = simpledialog.askstring("Welcome!", "🌼 What's your name?")
if not user_name:
    user_name = "Guest"

# Load plant images
plant_images = []
for i in range(5):
    img = Image.open(f"plant_{i}.png").resize((200, 200))
    photo = ImageTk.PhotoImage(img)
    plant_images.append(photo)

# Game variables
plant_stage = 0
score = 0
unlocked_vouchers = []
milestones = [10, 20, 30]
actions = [
    "💧 Drank water", "🏃‍♀️ Did exercise", "📓 Wrote journal",
    "🌞 Got sunshine", "🧘‍♂️ Meditated", "🍏 Ate healthy", "🎵 Listened to music"
]

# Top UI Section
title_frame = tk.Frame(root, bg="#D8EFD3", pady=10)
title_frame.pack(fill="x")

title_label = tk.Label(title_frame, text=f"🌸 MindBloom 🌸", font=("Helvetica", 22, "bold"), bg="#D8EFD3", fg="#2E5339")
title_label.pack()

welcome_label = tk.Label(title_frame, text=f"Welcome, {user_name}!", font=("Helvetica", 14), bg="#D8EFD3")
welcome_label.pack()

# Plant Display
plant_frame = tk.Frame(root, bg="#FAF8F0", pady=10)
plant_frame.pack()
plant_label = tk.Label(plant_frame, image=plant_images[plant_stage], bg="#FAF8F0")
plant_label.pack(pady=10)

# Progress Bar
progress_label = tk.Label(root, text="🌱 Growth Progress", font=("Helvetica", 12), bg="#FAF8F0")
progress_label.pack(pady=5)
progress = ttk.Progressbar(root, length=350, maximum=30)
progress.pack(pady=5)

# Status
status_label = tk.Label(root, text=f"💚 Wellness Score: {score}", font=("Helvetica", 13), bg="#FAF8F0", pady=5)
status_label.pack()

# Word List for Wordle Game
word_list = ["apple", "grape", "lemon", "mango", "melon", "peach", "berry", "chili", "olive"]

# Functions
def log_action(action_text):
    global score, plant_stage

    score += 1
    progress['value'] = score
    status_label.config(text=f"💚 Wellness Score: {score}")

    # Plant Growth
    if score % 5 == 0 and plant_stage < len(plant_images) - 1:
        plant_stage += 1
        plant_label.config(image=plant_images[plant_stage])

    # Launch Wordle mini-game every 4 actions
    if score % 4 == 0:
        play_wordle_game()

    # Show achievement vouchers
    if score in milestones and score not in unlocked_vouchers:
        unlocked_vouchers.append(score)
        show_achievement(score)

def show_achievement(score):
    messagebox.showinfo("🎁 Achievement Unlocked!", f"Great job, {user_name}!\nYou've earned a voucher at {score} points!")

def play_wordle_game():
    game = tk.Toplevel(root)
    game.title("🔤 Wordle Mini-Game")
    game.geometry("350x400")
    game.configure(bg="#FFFBEF")

    target_word = random.choice(word_list)
    attempts = []

    label_info = tk.Label(game, text="Guess the 5-letter word!", font=("Helvetica", 12), bg="#FFFBEF")
    label_info.pack(pady=10)

    entry = tk.Entry(game, font=("Helvetica", 14), justify="center")
    entry.pack(pady=10)

    result_frame = tk.Frame(game, bg="#FFFBEF")
    result_frame.pack()

    def check_guess():
        guess = entry.get().lower()
        if len(guess) != 5 or not guess.isalpha():
            messagebox.showerror("Invalid", "Please enter a valid 5-letter word.")
            return
        entry.delete(0, 'end')

        row = tk.Frame(result_frame, bg="#FFFBEF")
        row.pack(pady=2)

        for i in range(5):
            char = guess[i].upper()
            color = "#D3D3D3"  # default grey
            if char.lower() == target_word[i]:
                color = "#90EE90"  # green for correct position
            elif char.lower() in target_word:
                color = "#FFD700"  # yellow for correct letter wrong position

            box = tk.Label(row, text=char, width=4, font=("Helvetica", 16, "bold"), bg=color, borderwidth=2, relief="ridge")
            box.pack(side="left", padx=2)

        attempts.append(guess)

        if guess == target_word:
            messagebox.showinfo("🎉 You Won!", f"Awesome! You guessed the word: {target_word.upper()}")
            game.destroy()
        elif len(attempts) == 6:
            messagebox.showinfo("😓 Out of tries", f"The correct word was: {target_word.upper()}")
            game.destroy()

    btn_guess = tk.Button(game, text="Check", font=("Helvetica", 12), bg="lightblue", command=check_guess)
    btn_guess.pack(pady=5)

# Action Buttons
tk.Label(root, text="✅ Choose your self-care action:", font=("Helvetica", 12), bg="#FAF8F0").pack(pady=10)

action_frame = tk.Frame(root, bg="#FAF8F0")
action_frame.pack()

for act in actions:
    tk.Button(action_frame, text=act, width=35, font=("Helvetica", 10), command=lambda a=act: log_action(a)).pack(pady=3)

# Exit Button
tk.Button(root, text="🚪 Exit Game", bg="tomato", fg="white", font=("Helvetica", 12), command=root.destroy).pack(pady=20)

# Start GUI
root.mainloop()
