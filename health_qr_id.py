import tkinter as tk
from tkinter import messagebox
import qrcode
from PIL import ImageTk, Image


def show_qr_id_window(parent=None):
    """Open a window that lets the user enter their health details and generate a QR code.

    parent: optional tkinter parent (keeps compatibility with how main.py calls it)
    """
    qr_win = tk.Toplevel(parent) if parent else tk.Toplevel()
    qr_win.title("My Health QR ID")

    header = tk.Label(qr_win, text="Your Health QR Code (show to doctor):", font=("Arial", 12, "bold"))
    header.pack(pady=8)

    form_frame = tk.Frame(qr_win)
    form_frame.pack(padx=10, pady=6)

    # Form fields
    tk.Label(form_frame, text="Name:").grid(row=0, column=0, sticky="e", padx=4, pady=4)
    name_var = tk.StringVar()
    name_entry = tk.Entry(form_frame, textvariable=name_var, width=30)
    name_entry.grid(row=0, column=1, pady=4)

    tk.Label(form_frame, text="Blood Type:").grid(row=1, column=0, sticky="e", padx=4, pady=4)
    blood_var = tk.StringVar()
    blood_entry = tk.Entry(form_frame, textvariable=blood_var, width=30)
    blood_entry.grid(row=1, column=1, pady=4)

    tk.Label(form_frame, text="Allergies:").grid(row=2, column=0, sticky="e", padx=4, pady=4)
    allergies_var = tk.StringVar()
    allergies_entry = tk.Entry(form_frame, textvariable=allergies_var, width=30)
    allergies_entry.grid(row=2, column=1, pady=4)

    tk.Label(form_frame, text="Emergency Contact:").grid(row=3, column=0, sticky="e", padx=4, pady=4)
    emergency_var = tk.StringVar()
    emergency_entry = tk.Entry(form_frame, textvariable=emergency_var, width=30)
    emergency_entry.grid(row=3, column=1, pady=4)

    # Container for QR display
    display_frame = tk.Frame(qr_win)
    display_frame.pack(pady=8)

    panel = tk.Label(display_frame)
    panel.pack()

    # Helper to generate and show QR
    def generate_qr():
        name = name_var.get().strip()
        blood = blood_var.get().strip()
        allergies = allergies_var.get().strip()
        emergency = emergency_var.get().strip()

        if not name:
            messagebox.showwarning("Missing name", "Please enter your name before generating the QR code.")
            return

        # Build the text payload for the QR code
        parts = [f"Name: {name}"]
        if blood:
            parts.append(f"Blood Type: {blood}")
        if allergies:
            parts.append(f"Allergies: {allergies}")
        if emergency:
            parts.append(f"Emergency: {emergency}")

        payload = "\n".join(parts)

        try:
            img = qrcode.make(payload)
            # keep a saved copy (optional) so users can find it later
            img.save("health_qr.png")
            # prepare image for tkinter
            img = img.convert("RGB")
            img = img.resize((200, 200))
            qr_img = ImageTk.PhotoImage(img)
            panel.configure(image=qr_img)
            panel.image = qr_img
        except Exception as e:
            messagebox.showerror("QR Error", f"Failed to generate QR code: {e}")

    btn_frame = tk.Frame(qr_win)
    btn_frame.pack(pady=6)

    gen_btn = tk.Button(btn_frame, text="Generate QR", command=generate_qr)
    gen_btn.grid(row=0, column=0, padx=6)

    def show_details():
        # Show a small preview of what will be encoded
        name = name_var.get().strip()
        blood = blood_var.get().strip()
        allergies = allergies_var.get().strip()
        emergency = emergency_var.get().strip()
        parts = [f"Name: {name or '<empty>'}", f"Blood Type: {blood or '<empty>'}", f"Allergies: {allergies or '<empty>'}", f"Emergency: {emergency or '<empty>'}"]
        messagebox.showinfo("QR Payload Preview", "\n".join(parts))

    preview_btn = tk.Button(btn_frame, text="Preview Details", command=show_details)
    preview_btn.grid(row=0, column=1, padx=6)

    # Focus on the name field for quick data entry
    name_entry.focus_set()

