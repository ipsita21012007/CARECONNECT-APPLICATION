import tkinter as tk
from tkinter import messagebox
from doctor_finder import show_doctor_finder_window
from lab_report_scanner import show_lab_report_scanner
from health_qr_id import show_qr_id_window
root = tk.Tk()
root.title("CareConnect")

qr_btn = tk.Button(root, text="My Health QR ID", command=show_qr_id_window)
qr_btn.pack(pady=6)

lab_report_btn = tk.Button(root, text="Lab Report Scanner", command=show_lab_report_scanner)
lab_report_btn.pack(pady=6)

def doctor_finder_action():

    show_doctor_finder_window(root)  

doctor_finder_btn = tk.Button(root, text="Doctor Finder", command=doctor_finder_action)
doctor_finder_btn.pack(pady=6)


root.mainloop()
