import tkinter as tk
from tkinter import messagebox
import sqlite3

DB_PATH = 'careconnect.db'


def get_connection():
    return sqlite3.connect(DB_PATH)


def fetch_doctors():
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT doctorID, name, specialty FROM Doctor ORDER BY name")
        rows = cur.fetchall()
        conn.close()
        return rows
    except Exception as e:
        print('DB fetch error:', e)
        return []


def doctor_exists(name):
    """Return True if a doctor with the given name already exists (case-insensitive)."""
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM Doctor WHERE LOWER(name) = LOWER(?) LIMIT 1", (name,))
        found = cur.fetchone() is not None
        conn.close()
        return found
    except Exception:
        return False


def add_doctor(name, specialty):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO Doctor (name, specialty) VALUES (?, ?)", (name, specialty))
    conn.commit()
    conn.close()


def update_doctor(doctor_id, name, specialty):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE Doctor SET name = ?, specialty = ? WHERE doctorID = ?", (name, specialty, doctor_id))
    conn.commit()
    conn.close()


def delete_doctor(doctor_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM Doctor WHERE doctorID = ?", (doctor_id,))
    conn.commit()
    conn.close()


def show_doctor_finder_window(parent):
    win = tk.Toplevel(parent)
    win.title('Doctor Finder')
    win.geometry('500x400')

    header = tk.Label(win, text='Doctors', font=('Arial', 12, 'bold'))
    header.pack(pady=8)

    list_frame = tk.Frame(win)
    list_frame.pack(fill='both', expand=True, padx=8)

    tk.Label(list_frame, text='Name', font=('Arial', 10, 'bold')).grid(row=0, column=0, padx=6, pady=6, sticky='w')
    tk.Label(list_frame, text='Specialty', font=('Arial', 10, 'bold')).grid(row=0, column=1, padx=6, pady=6, sticky='w')
    tk.Label(list_frame, text='Actions', font=('Arial', 10, 'bold')).grid(row=0, column=2, padx=6, pady=6, sticky='w')

    rows_container = tk.Frame(list_frame)
    rows_container.grid(row=1, column=0, columnspan=3, sticky='nsew')

    list_frame.rowconfigure(1, weight=1)
    list_frame.columnconfigure(1, weight=1)

    def refresh_list():
        for child in rows_container.winfo_children():
            child.destroy()

        doctors = fetch_doctors()
        if not doctors:
            tk.Label(rows_container, text='No doctors found.', fg='gray').pack(pady=12)
            return

        for doc in doctors:
            doctor_id, name, specialty = doc
            row = tk.Frame(rows_container)
            row.pack(fill='x', pady=2)

            lbl_name = tk.Label(row, text=name, anchor='w', fg='blue', cursor='hand2')
            lbl_name.pack(side='left', fill='x', expand=True, padx=4)

            def on_show_details(did=doctor_id, n=name, s=specialty):
                messagebox.showinfo('Doctor details', f"Name: {n}\nSpecialty: {s or '<empty>'}\nID: {did}")

            # clicking the name opens a small details dialog
            lbl_name.bind('<Button-1>', lambda e, dfn=on_show_details: dfn())

            lbl_spec = tk.Label(row, text=specialty or '', width=20, anchor='w')
            lbl_spec.pack(side='left', padx=4)

            btn_frame = tk.Frame(row)
            btn_frame.pack(side='right')

            def on_edit(did=doctor_id):
                edit_doctor_dialog(did)

            def on_delete(did=doctor_id):
                if messagebox.askyesno('Delete', 'Delete this doctor?'):
                    delete_doctor(did)
                    refresh_list()

            tk.Button(btn_frame, text='Edit', command=on_edit).pack(side='left', padx=2)
            tk.Button(btn_frame, text='Delete', command=on_delete).pack(side='left', padx=2)

    def add_doctor_dialog():
        dialog = tk.Toplevel(win)
        dialog.title('Add Doctor')
        dialog.grab_set()

        tk.Label(dialog, text='Name:').grid(row=0, column=0, padx=6, pady=6, sticky='e')
        name_var = tk.StringVar()
        tk.Entry(dialog, textvariable=name_var, width=40).grid(row=0, column=1, padx=6, pady=6)

        tk.Label(dialog, text='Specialty:').grid(row=1, column=0, padx=6, pady=6, sticky='e')
        spec_var = tk.StringVar()
        tk.Entry(dialog, textvariable=spec_var, width=40).grid(row=1, column=1, padx=6, pady=6)

        def on_save():
            name = name_var.get().strip()
            spec = spec_var.get().strip()
            if not name:
                messagebox.showwarning('Missing name', "Please enter the doctor's name.")
                return
            if doctor_exists(name):
                messagebox.showwarning('Duplicate', 'A doctor with this name already exists.')
                return
            add_doctor(name, spec)
            dialog.destroy()
            refresh_list()

        tk.Button(dialog, text='Save', command=on_save).grid(row=2, column=0, columnspan=2, pady=8)

    def edit_doctor_dialog(doctor_id):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute('SELECT name, specialty FROM Doctor WHERE doctorID = ?', (doctor_id,))
        row = cur.fetchone()
        conn.close()
        if not row:
            messagebox.showerror('Not found', 'Doctor not found in database.')
            return

        dialog = tk.Toplevel(win)
        dialog.title('Edit Doctor')
        dialog.grab_set()

        tk.Label(dialog, text='Name:').grid(row=0, column=0, padx=6, pady=6, sticky='e')
        name_var = tk.StringVar(value=row[0])
        tk.Entry(dialog, textvariable=name_var, width=40).grid(row=0, column=1, padx=6, pady=6)

        tk.Label(dialog, text='Specialty:').grid(row=1, column=0, padx=6, pady=6, sticky='e')
        spec_var = tk.StringVar(value=row[1])
        tk.Entry(dialog, textvariable=spec_var, width=40).grid(row=1, column=1, padx=6, pady=6)

        def on_update():
            name = name_var.get().strip()
            spec = spec_var.get().strip()
            if not name:
                messagebox.showwarning('Missing name', "Please enter the doctor's name.")
                return
            # allow update if name unchanged or not colliding with another doctor
            if name.lower() != row[0].lower() and doctor_exists(name):
                messagebox.showwarning('Duplicate', 'A doctor with this name already exists.')
                return
            update_doctor(doctor_id, name, spec)
            dialog.destroy()
            refresh_list()

        tk.Button(dialog, text='Update', command=on_update).grid(row=2, column=0, columnspan=2, pady=8)

    btn_bar = tk.Frame(win)
    btn_bar.pack(pady=8)

    tk.Button(btn_bar, text='Add Doctor', command=add_doctor_dialog).pack()

    refresh_list()
