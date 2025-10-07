import tkinter as tk
from tkinter import filedialog, messagebox

def show_lab_report_scanner():
    win = tk.Toplevel()
    win.title("Smart Lab Report Scanner")
    tk.Label(win, text="Upload your lab report:").pack(pady=10)
    tk.Button(win, text="Upload Photo/PDF", command=lambda: upload_file(win)).pack()

def upload_file(parent):
    file_path = filedialog.askopenfilename(filetypes=[("Images/PDFs", "*.jpg *.jpeg *.png *.pdf")])
    if file_path:
        # Placeholder logic for now
        messagebox.showinfo("Coming Soon", "AI Lab report parsing will display extracted data here!")
    
