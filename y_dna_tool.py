import tkinter as tk
from tkinter import scrolledtext, messagebox


def load_fasta(filename):
    sequence = []

    with open(filename, "r") as f:
        for line in f:
            if not line.startswith(">"):
                sequence.append(line.strip().upper())

    return "".join(sequence)


# שנה לשם הקובץ שלך
sequence = load_fasta("chrY.txt")


def check_position():
    try:
        pos = int(position_entry.get())

        if pos < 1 or pos > len(sequence):
            messagebox.showerror(
                "שגיאה",
                f"המיקום חייב להיות בין 1 ל-{len(sequence)}"
            )
            return

        base = sequence[pos - 1]

        result_label.config(
            text=f"במיקום {pos} נמצא: {base}"
        )

    except ValueError:
        messagebox.showerror(
            "שגיאה",
            "יש להזין מספר תקין"
        )


def show_window():
    try:
        pos = int(position_entry.get())

        if pos < 1 or pos > len(sequence):
            messagebox.showerror(
                "שגיאה",
                f"המיקום חייב להיות בין 1 ל-{len(sequence)}"
            )
            return

        start = max(1, pos - 500)
        end = min(len(sequence), pos + 499)

        left = sequence[start - 1:pos - 1]
        center = sequence[pos - 1]
        right = sequence[pos:end]

        text_box.delete("1.0", tk.END)
        text_box.insert(
            tk.END,
            left + "[" + center + "]" + right
        )

    except ValueError:
        messagebox.showerror(
            "שגיאה",
            "יש להזין מספר תקין"
        )


def find_sequence():
    query = sequence_entry.get().strip().upper()

    if not query:
        return

    pos = sequence.find(query)

    if pos == -1:
        result_label.config(text="הרצף לא נמצא")
        return

    start = pos + 1
    end = start + len(query) - 1

    result_label.config(
        text=f"הרצף נמצא במיקום {start} עד {end}"
    )


def find_all_sequences():
    query = sequence_entry.get().strip().upper()

    if not query:
        return

    text_box.delete("1.0", tk.END)

    count = 0
    search_start = 0

    while True:
        pos = sequence.find(query, search_start)

        if pos == -1:
            break

        start = pos + 1
        end = start + len(query) - 1

        text_box.insert(
            tk.END,
            f"{start} - {end}\n"
        )

        count += 1
        search_start = pos + 1

    if count == 0:
        text_box.insert(tk.END, "הרצף לא נמצא")
    else:
        text_box.insert(
            tk.END,
            f"\nסה\"כ מופעים: {count}"
        )


root = tk.Tk()
root.title("Chromosome Y Viewer")
root.geometry("1100x750")


title_label = tk.Label(
    root,
    text=f"Chromosome Y Viewer - GRCh38 - ({len(sequence):,} bases)",
    font=("Arial", 16)
)
title_label.pack(pady=10)


position_frame = tk.Frame(root)
position_frame.pack(pady=5)

tk.Label(
    position_frame,
    text="מיקום:"
).pack(side=tk.LEFT)

position_entry = tk.Entry(
    position_frame,
    width=20
)
position_entry.pack(side=tk.LEFT, padx=5)

tk.Button(
    position_frame,
    text="בדוק מיקום",
    command=check_position
).pack(side=tk.LEFT, padx=5)

tk.Button(
    position_frame,
    text="הצג 1000 בסיסים מסביב",
    command=show_window
).pack(side=tk.LEFT, padx=5)


search_frame = tk.Frame(root)
search_frame.pack(pady=10)

tk.Label(
    search_frame,
    text="רצף DNA:"
).pack(side=tk.LEFT)

sequence_entry = tk.Entry(
    search_frame,
    width=60
)
sequence_entry.pack(side=tk.LEFT, padx=5)

tk.Button(
    search_frame,
    text="חפש רצף",
    command=find_sequence
).pack(side=tk.LEFT, padx=5)

tk.Button(
    search_frame,
    text="מצא כל המופעים",
    command=find_all_sequences
).pack(side=tk.LEFT, padx=5)


result_label = tk.Label(
    root,
    text="",
    font=("Arial", 12)
)
result_label.pack(pady=10)


text_box = scrolledtext.ScrolledText(
    root,
    width=140,
    height=30,
    wrap=tk.WORD
)
text_box.pack(
    fill="both",
    expand=True,
    padx=10,
    pady=10
)


root.mainloop()
