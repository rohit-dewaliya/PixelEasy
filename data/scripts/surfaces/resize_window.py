import tkinter as tk
from tkinter import ttk, messagebox


def ask_width_height(size):
    def on_ok():
        try:
            w = int(width_var.get())
            h = int(height_var.get())
            result.extend([w, h])  # store values
            root.destroy()
        except ValueError:
            messagebox.showerror("Invalid input", "Please enter valid integers.")

    def on_cancel():
        root.destroy()

    result = []

    root = tk.Tk()
    root.title("Resize Canvas")
    root.geometry("280x150")
    root.configure(bg="#2b2b2b")

    icon_img = tk.PhotoImage(file="data/images/icon.png")
    root.iconphoto(True, icon_img)

    style = ttk.Style()
    style.theme_use("clam")

    # Button style
    style.configure(
        "Accent.TButton",
        font=("Segoe UI", 10, "bold"),
        padding=8,
        foreground="white",
        background="#4CAF50",
        borderwidth=0,
        focusthickness=3,
        focuscolor="none"
    )
    style.map(
        "Accent.TButton",
        background=[("active", "#45a049")]
    )

    style.configure(
        "Cancel.TButton",
        font=("Segoe UI", 10, "bold"),
        padding=8,
        foreground="white",
        background="#f44336",
        borderwidth=0
    )
    style.map(
        "Cancel.TButton",
        background=[("active", "#d32f2f")]
    )

    tk.Label(root, text="Width:", font=("Segoe UI", 10), bg="#2b2b2b", fg="white").grid(row=0, column=0, padx=10, pady=10, sticky="e")
    tk.Label(root, text="Height:", font=("Segoe UI", 10), bg="#2b2b2b", fg="white").grid(row=1, column=0, padx=10, pady=10, sticky="e")

    width_var = tk.StringVar(value=str(size[0]))
    height_var = tk.StringVar(value=str(size[1]))
    ttk.Entry(root, textvariable=width_var, font=("Segoe UI", 10)).grid(row=0, column=1, padx=10, pady=10)
    ttk.Entry(root, textvariable=height_var, font=("Segoe UI", 10)).grid(row=1, column=1, padx=10, pady=10)

    ttk.Button(root, text="OK", command=on_ok, style="Accent.TButton").grid(row=2, column=0, pady=15, padx=10, sticky="ew")
    ttk.Button(root, text="Cancel", command=on_cancel, style="Cancel.TButton").grid(row=2, column=1, pady=15, padx=10, sticky="ew")

    root.mainloop()
    return result if result else None