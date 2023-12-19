import tkinter as tk
import time
import random

start_time = 0


def generate_random_text():
    words = ["apple", "banana", "cherry", "dog", "elephant", "python", "programming", "keyboard", "monitor", "mouse"]
    return " ".join(random.choices(words, k=20))  # Random sentence with 30 words


def start_test():
    global start_time
    start_time = time.time()
    entry.focus_set()
    start_button['state'] = 'disabled'
    entry.bind("<KeyRelease>", check_input)


def check_input(event):
    global start_time
    typed_text = current_input.get()

    if typed_text == text_to_type:
        elapsed_time = time.time() - start_time
        words_per_minute = int((len(text_to_type) / 5) / (elapsed_time / 60))

        result_label.config(text=f"Words per minute: {words_per_minute}")
        entry.unbind("<KeyRelease>")
        start_button['state'] = 'normal'
    elif text_to_type.startswith(typed_text):
        text_label.config(text=text_to_type[len(typed_text):])
    else:
        current_input.set(typed_text[:-1])  # Remove the last character


if __name__ == "__main__":
    root = tk.Tk()
    root.title("WPM Tester")

    text_to_type = generate_random_text()
    current_input = tk.StringVar()

    instruction_label = tk.Label(root, text="Type the following:")
    instruction_label.pack(pady=10)

    text_label = tk.Label(root, text=text_to_type, font=("Helvetica", 12))
    text_label.pack()

    entry = tk.Entry(root, textvariable=current_input, font=("Helvetica", 12))
    entry.pack(pady=10)

    start_button = tk.Button(root, text="Start Test", command=start_test)
    start_button.pack()

    result_label = tk.Label(root, text="")
    result_label.pack(pady=10)

    root.mainloop()
