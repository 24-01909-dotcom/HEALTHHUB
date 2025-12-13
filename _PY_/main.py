import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import json
import os
import mysql.connector

# ====================
# DATABASE CONNECTION
# ====================
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="healthhub"
    )


# ---------------- MAIN RECORDS ----------------

def fetch_main_records():
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM main_records ORDER BY id ASC")
    rows = cur.fetchall()
    conn.close()
    return rows


def insert_main_record(data):
    conn = get_connection()
    cur = conn.cursor()
    query = """
        INSERT INTO main_records (label, type, description, datetime, severity)
        VALUES (%s, %s, %s, %s, %s)
    """
    cur.execute(query, (
        data["label"], data["type"], data["description"],
        data["datetime"], data["severity"]
    ))
    conn.commit()
    conn.close()


def update_main_record(record_id, data):
    conn = get_connection()
    cur = conn.cursor()
    query = """
        UPDATE main_records
        SET label=%s, type=%s, description=%s, datetime=%s, severity=%s
        WHERE id=%s
    """
    cur.execute(query, (
        data["label"], data["type"], data["description"],
        data["datetime"], data["severity"], record_id
    ))
    conn.commit()
    conn.close()


def delete_main_record(record_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM main_records WHERE id=%s", (record_id,))
    conn.commit()
    conn.close()


# ---------------- WELLNESS RECORDS ----------------

def fetch_wellness_records():
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM wellness_records ORDER BY id ASC")
    rows = cur.fetchall()
    conn.close()
    return rows


def insert_wellness_record(data):
    conn = get_connection()
    cur = conn.cursor()
    query = """
        INSERT INTO wellness_records (label, category, frequency, description, datetime)
        VALUES (%s, %s, %s, %s, %s)
    """
    cur.execute(query, (
        data["label"], data["category"], data["frequency"],
        data["description"], data["datetime"]
    ))
    conn.commit()
    conn.close()


def update_wellness_record(record_id, data):
    conn = get_connection()
    cur = conn.cursor()
    query = """
        UPDATE wellness_records
        SET label=%s, category=%s, frequency=%s, description=%s, datetime=%s
        WHERE id=%s
    """
    cur.execute(query, (
        data["label"], data["category"], data["frequency"],
        data["description"], data["datetime"], record_id
    ))
    conn.commit()
    conn.close()


def delete_wellness_record(record_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM wellness_records WHERE id=%s", (record_id,))
    conn.commit()
    conn.close()


# ================
# GLOBAL STORAGE
# ================
records = []               # Main records (Symptoms / Medicine / Appointments)
wellness_records = []      # Wellness habits
selected_index = None
selected_source = None
quick_type = None
next_id = 1
next_wellness_id = 1

# =============
# COLOR THEME
# =============
BG_COLOR = "#1E1E2F"
FRAME_BG = "#2E2E3E"
BTN_COLOR = "#4C6EF5"
BTN_HOVER = "#5C7CFA"
LABEL_COLOR = "#E0E0E0"
ENTRY_BG = "#3C3C4E"
ENTRY_FG = "#FFFFFF"
TREE_BG = "#2E2E3E"
TREE_FG = "#E0E0E0"

# ===================
# JSON FILE STORAGE
# ===================
MAIN_FILE = "healthhub_records.json"
WELLNESS_FILE = "healthhub_wellness.json"


def save_all_data():
    """Automatically save all records to JSON."""
    with open(MAIN_FILE, "w") as f:
        json.dump(records, f, indent=4)

    with open(WELLNESS_FILE, "w") as f:
        json.dump(wellness_records, f, indent=4)


def load_all_data():
    """Load all data automatically when program starts."""
    global records, wellness_records, next_id, next_wellness_id

    if os.path.exists(MAIN_FILE):
        with open(MAIN_FILE, "r") as f:
            records = json.load(f)

    if os.path.exists(WELLNESS_FILE):
        with open(WELLNESS_FILE, "r") as f:
            wellness_records = json.load(f)

    # Fix ID counters
    next_id = (max([int(r["id"]) for r in records]) + 1) if records else 1
    next_wellness_id = (max([int(r["id"]) for r in wellness_records]) + 1) if wellness_records else 1


# =========================================
# DATABASE-LIKE FUNCTIONS (WITH AUTO-SAVE)
# =========================================
def fetch_all_records():
    merged = [("main", r) for r in records] + [("wellness", w) for w in wellness_records]
    merged.sort(key=lambda x: (0 if x[0] == "main" else 1, x[1]["id"]))
    return merged


def insert_record(data):
    global next_id
    data["id"] = next_id
    next_id += 1
    records.append(data)
    save_all_data()


def update_record(record_id, data):
    for r in records:
        if r["id"] == record_id:
            r.update(data)
            break
    save_all_data()


def delete_record_db(record_id):
    global records
    records = [r for r in records if r["id"] != record_id]
    save_all_data()


def insert_wellness_record(data):
    global next_wellness_id
    data["id"] = next_wellness_id
    next_wellness_id += 1
    wellness_records.append(data)
    save_all_data()


def update_wellness_record(record_id, data):
    for r in wellness_records:
        if r["id"] == record_id:
            r.update(data)
            break
    save_all_data()


def delete_wellness_record_db(record_id):
    global wellness_records
    wellness_records = [r for r in wellness_records if r["id"] != record_id]
    save_all_data()


# ===================
# MAIN APPLICATION
# ===================
class HealthHubApp(tk.Tk):
    def __init__(self):
        super().__init__()

        load_all_data()  # ← Load saved data automatically

        self.title("HealthHub: A Wellness Tracking System")
        self.geometry("980x620")
        self.configure(bg=BG_COLOR)
        self.current_frame = None
        self.switch_frame(StartScreen)

    def switch_frame(self, frame_class, **kwargs):
        global selected_index, selected_source, quick_type

        if frame_class not in (RecordForm, WellnessHabitsForm):
            selected_index = None
            selected_source = None
            quick_type = None

        new_frame = frame_class(self, **kwargs)
        if self.current_frame:
            self.current_frame.destroy()

        self.current_frame = new_frame
        self.current_frame.pack(fill="both", expand=True)


# ==================
# START SCREEN
# ==================
class StartScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=BG_COLOR)

        # Load background image
        image_path = "IMAGE/FRONT PAGE.png"
        if os.path.exists(image_path):
            self.bg_image = Image.open(image_path)
        else:
            self.bg_image = Image.new("RGB", (1280, 800), BG_COLOR)  # fallback

        self.bg_image = self.bg_image.resize((1280, 800), Image.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        # Canvas for background
        self.canvas = tk.Canvas(self, width=980, height=620)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")

        # Overlay text
        self.canvas.create_text(700, 200, text="HealthHub: A Wellness Tracking \nand Information System",
                                font=("Constantia", 55, "bold"), fill="black", justify="center")

        # Buttons
        start_btn = tk.Button(self, text="START", width=20, font=("Times New Roman", 15),
                            bg=BTN_COLOR, fg="white", justify="right", command=lambda: master.switch_frame(Dashboard))
        about_btn = tk.Button(self, text="ABOUT", width=20, font=("Times New Roman", 15),
                            bg=BTN_COLOR, fg="white", justify="right", command=lambda: master.switch_frame(AboutScreen))

        self.canvas.create_window(650, 400, window=start_btn)
        self.canvas.create_window(650, 460, window=about_btn)


# ==================
# ABOUT SCREEN
# ==================
class AboutScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=BG_COLOR)

        tk.Label(self, text="ABOUT", font=("Times New Roman", 30, "bold"),
                bg=BG_COLOR, fg=LABEL_COLOR).pack(pady=40)

        desc = (
            "HealthHub is a digital platform designed to track, monitor, \n"
            "and manage personal health and wellness. It serves as both an \n"
            "information repository and a tracking tool, helping users maintain a healthy \n"
            "lifestyle through organized data collection, analysis, and guidance."
        )

        tk.Label(self, text=desc, font=("Times New Roman", 20),
                bg=BG_COLOR, fg=LABEL_COLOR, justify="center").pack(pady=10)

        tk.Button(
            self, text="BACK", width=18, font=("Times New Roman", 15),
            bg=BTN_COLOR, fg="white",
            command=lambda: master.switch_frame(StartScreen)
        ).pack(side="bottom", pady=40)


# ==================
# DASHBOARD
# ==================
class Dashboard(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=BG_COLOR)

        tk.Label(self, text="Dashboard - HealthHub",
                font=("Times New Roman", 26, "bold"),
                bg=BG_COLOR, fg=LABEL_COLOR).pack(pady=10)

        container = tk.Frame(self, bg=BG_COLOR)
        container.pack(fill="both", expand=True, padx=10, pady=10)

        # ==== LEFT PANEL ====
        left = tk.Frame(container, bg=FRAME_BG, bd=2, relief="solid", padx=20, pady=20)
        left.pack(side="left", fill="y")

        tk.Label(left, text="VIEW", font=("Times New Roman", 15, "bold"),
                bg=FRAME_BG, fg=LABEL_COLOR).pack(pady=30)

        tk.Button(left, text="View All", font=("Courier New", 9), width=19, bg=BTN_COLOR, fg="white",
                command=self.load_records).pack(pady=4)

        tk.Button(left, text="View Symptoms", font=("Courier New", 9), width=19, bg=BTN_COLOR, fg="white",
                command=lambda: self.filter_main_type("Symptoms")).pack(pady=4)

        tk.Button(left, text="View Medicine", font=("Courier New", 9), width=19, bg=BTN_COLOR, fg="white",
                command=lambda: self.filter_main_type("Medicine")).pack(pady=4)

        tk.Button(left, text="View Appointment", font=("Courier New", 9),  width=19, bg=BTN_COLOR, fg="white",
                command=lambda: self.filter_main_type("Appointment")).pack(pady=4)

        tk.Button(left, text="View Wellness Only", font=("Courier New", 9), width=19, bg=BTN_COLOR, fg="white",
                command=lambda: self.load_records(True)).pack(pady=4)

        tk.Button(left, text="Saved Info", font=("Courier New", 9), width=19, bg=BTN_COLOR, fg="white",
                command=lambda: master.switch_frame(SavedInfoScreen)).pack(pady=20)

        # === ACTIONS ===
        tk.Label(left, text="ACTIONS", font=("Times New Roman", 15, "bold"),
                bg=FRAME_BG, fg=LABEL_COLOR).pack(pady=20)

        tk.Button(left, text="Edit Selected", font=("Courier New", 9), width=19, bg=BTN_COLOR, fg="white",
                command=self.edit_selected).pack(pady=4)

        tk.Button(left, text="Delete Selected", font=("Courier New", 9), width=19, bg=BTN_COLOR, fg="white",
                command=self.delete_selected).pack(pady=4)

        # ==== CENTER TABLE ====
        center = tk.Frame(container, bd=2, relief="solid", bg=FRAME_BG)
        center.pack(side="left", expand=True, fill="both", padx=10)

        columns = ("ID No.", "Label", "Type", "Description", "Date/Time", "Severity/Freq")
        widths = [60, 120, 120, 250, 120, 100]
        self.tree = ttk.Treeview(center, columns=columns, show="headings")

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background=TREE_BG, foreground=TREE_FG,
                        fieldbackground=TREE_BG, rowheight=28)
        style.map("Treeview", background=[('selected', BTN_COLOR)])

        for col, w in zip(columns, widths):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=w, anchor="center")

        self.tree.pack(fill="both", expand=True)
        self.load_records()

        # ==== RIGHT QUICK ADD ====
        right = tk.Frame(container, bg=FRAME_BG, bd=2, relief="solid", padx=10, pady=10)
        right.pack(side="right", fill="y")

        tk.Label(right, text="QUICK ADD", font=("Times New Roman", 15, "bold"),
                bg=FRAME_BG, fg=LABEL_COLOR).pack(pady=30)

        tk.Button(right, text="Add Symptoms", font=("Courier New", 9), width=19, bg=BTN_COLOR, fg="white",
                command=lambda: self.quick_add("Symptoms")).pack(pady=5)

        tk.Button(right, text="Add Medicine", font=("Courier New", 9), width=19, bg=BTN_COLOR, fg="white",
                command=lambda: self.quick_add("Medicine")).pack(pady=5)

        tk.Button(right, text="Add Appointment", font=("Courier New", 9), width=19, bg=BTN_COLOR, fg="white",
                command=lambda: self.quick_add("Appointment")).pack(pady=5)

        tk.Button(right, text="Add Wellness Habit", font=("Courier New", 9), width=19, bg=BTN_COLOR, fg="white",
                command=lambda: self.quick_add("WELLNESS_FORM")).pack(pady=5)

        tk.Button(right, text="Back", font=("Courier New", 9), width=19, bg=BTN_COLOR, fg="white",
                command=lambda: master.switch_frame(StartScreen)).pack(pady=20)

    # ------------------------------------------------
    def quick_add(self, type_name):
        global quick_type
        quick_type = type_name
        if type_name == "WELLNESS_FORM":
            self.master.switch_frame(WellnessHabitsForm)
        else:
            self.master.switch_frame(RecordForm)

    def load_records(self, wellness_only=False):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for source, row in fetch_all_records():
            if wellness_only and source != "wellness":
                continue

            if source == "main":
                self.tree.insert("", "end", iid=f"main_{row['id']}", values=(
                    row["id"], row["label"], row["type"], row["description"],
                    row["datetime"], row["severity"]
                ))
            else:
                self.tree.insert("", "end", iid=f"well_{row['id']}", values=(
                    row["id"], row["label"], f"Wellness ({row['category']})",
                    row["description"], row["datetime"], row["frequency"]
                ))

    def filter_main_type(self, category):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for source, row in fetch_all_records():
            if source == "main" and row["type"].lower() == category.lower():
                self.tree.insert("", "end", iid=f"main_{row['id']}", values=(
                    row["id"], row["label"], row["type"], row["description"],
                    row["datetime"], row["severity"]
                ))

    def edit_selected(self):
        global selected_index, selected_source

        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select a record to edit.")
            return

        iid = selected[0]
        selected_index = int(iid.split("_")[1])
        selected_source = "main" if iid.startswith("main_") else "wellness"

        if selected_source == "main":
            self.master.switch_frame(RecordForm)
        else:
            self.master.switch_frame(WellnessHabitsForm)

    def delete_selected(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select a record to delete.")
            return

        iid = selected[0]

        if iid.startswith("main_"):
            delete_record_db(int(iid.split("_")[1]))
        else:
            delete_wellness_record_db(int(iid.split("_")[1]))

        self.load_records()


# ==========================
# SAVED INFO SCREEN
# ==========================
class SavedInfoScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=BG_COLOR)

        tk.Button(
            self, text="←", font=("Arial", 20, "bold"),
            bg=BG_COLOR, fg="white", bd=0,
            command=lambda: master.switch_frame(Dashboard)
        ).pack(anchor="nw", padx=10, pady=10)

        tk.Label(
            self, text="SAVED INFO",
            font=("Times New Roman", 30, "bold"),
            bg=BG_COLOR, fg="white"
        ).pack(pady=5)

        outer = tk.Frame(self, bg=FRAME_BG, bd=3, relief="solid")
        outer.pack(fill="both", expand=True, padx=20, pady=20)

        table_frame = tk.Frame(outer, bg=FRAME_BG)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        columns = ("ID No.", "Name", "Type", "Description", "Date/Time", "Severity/Freq")
        widths = [60, 120, 140, 250, 140, 100]
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background=TREE_BG, foreground=TREE_FG,
                        fieldbackground=TREE_BG, rowheight=30)

        for col, w in zip(columns, widths):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=w, anchor="center")

        self.tree.pack(fill="both", expand=True)
        self.load_saved_info()

    def load_saved_info(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for source, row in fetch_all_records():
            if source == "main":
                self.tree.insert("", "end", values=(
                    row["id"], row["label"], row["type"], row["description"],
                    row["datetime"], row["severity"]
                ))
            else:
                self.tree.insert("", "end", values=(
                    row["id"], row["label"], f"Wellness ({row['category']})",
                    row["description"], row["datetime"], row["frequency"]
                ))


# ======================
# RECORD FORM
# ======================
class RecordForm(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=BG_COLOR)

        global selected_index, selected_source, quick_type

        tk.Label(self, text="HealthHub Form", font=("Times New Roman", 22, "bold"),
                bg=BG_COLOR, fg=LABEL_COLOR).pack(pady=15)

        form = tk.Frame(self, bg=FRAME_BG, bd=2, relief="solid", padx=60, pady=18)
        form.pack()

        self.entry_name = self.create_entry(form, "Label:")
        self.entry_type = self.create_entry(form, "Type:")

        # ======================================
        # MULTI-LINE DESCRIPTION BOX (UPDATED)
        # ======================================
        tk.Label(form, text="Description:", bg=FRAME_BG, fg=LABEL_COLOR).pack(anchor="w")
        self.entry_desc = tk.Text(form, width=30, height=3, bg=ENTRY_BG, fg=ENTRY_FG,
                                insertbackground=ENTRY_FG)
        self.entry_desc.pack()
        self.entry_desc.insert("1.0", " ")

        self.entry_datetime = self.create_entry(form, "Date/Time:")

        # Wellness Category
        tk.Label(form, text="Category (For Wellness Only):",
                bg=FRAME_BG, fg=LABEL_COLOR).pack(anchor="w", pady=(10, 0))
        categories = ["Exercise", "Nutrition", "Sleep", "Self-Care", "Mental Wellness", "Hygiene"]
        self.entry_category = ttk.Combobox(form, values=categories, width=37, state="readonly")
        self.entry_category.pack()
        self.entry_category.set(categories[0])

        tk.Label(form, text="Frequency (For Wellness Only):",
                bg=FRAME_BG, fg=LABEL_COLOR).pack(anchor="w", pady=(10, 0))
        self.entry_frequency = ttk.Combobox(
            form, values=["Daily", "Weekly", "Routine", "Sometimes"],
            width=37, state="readonly"
        )
        self.entry_frequency.pack()
        self.entry_frequency.set("Daily")

        # Severity
        tk.Label(form, text="Severity (For Main Records):",
                bg=FRAME_BG, fg=LABEL_COLOR).pack(anchor="w", pady=(10, 0))
        self.entry_severity = ttk.Combobox(
            form, values=["Mild", "Moderate", "Critical"],
            width=37, state="readonly"
        )
        self.entry_severity.pack()
        self.entry_severity.set("Mild")

        # Buttons
        btns = tk.Frame(self, bg=BG_COLOR)
        btns.pack(side="right", padx=60, pady=20)

        tk.Button(btns, text="SAVE", font=("Courier New", 9), width=19,
                bg=BTN_COLOR, fg="white",
                command=self.save_record).pack(pady=5)

        tk.Button(btns, text="CANCEL", font=("Courier New", 9), width=19,
                bg=BTN_COLOR, fg="white",
                command=lambda: master.switch_frame(Dashboard)).pack(pady=5)

        if selected_index is not None and selected_source == "main":
            tk.Button(btns, text="DELETE", font=("Courier New", 9), width=19,
                    bg="red", fg="white",
                    command=self.delete_record).pack(pady=5)

        tk.Button(btns, text="BACK", font=("Courier New", 9), width=19,
                bg=BTN_COLOR, fg="white",
                command=lambda: master.switch_frame(Dashboard)).pack(pady=5)

        self.entry_type.bind("<KeyRelease>", lambda e: self.toggle_wellness_mode())
        self.entry_type.bind("<FocusOut>", lambda e: self.toggle_wellness_mode())

        # Load editing data
        if selected_index is not None and selected_source == "main":
            self.load_edit_data_main()

        if quick_type and quick_type != "WELLNESS_FORM":
            self.entry_type.delete(0, tk.END)
            self.entry_type.insert(0, quick_type)

        if quick_type == "WELLNESS_FORM":
            self.entry_type.delete(0, tk.END)
            self.entry_type.insert(0, "Wellness Habits")

        self.toggle_wellness_mode()

    # -------------------------------------------------------
    def create_entry(self, parent, txt):
        tk.Label(parent, text=txt, bg=FRAME_BG, fg=LABEL_COLOR).pack(anchor="w")
        entry = tk.Entry(parent, width=40, bg=ENTRY_BG, fg=ENTRY_FG, insertbackground=ENTRY_FG)
        entry.pack()
        return entry

    # -------------------------------------------------------
    def toggle_wellness_mode(self):
        is_wellness = self.entry_type.get().strip().lower().startswith("wellness")

        self.entry_category.configure(state="readonly" if is_wellness else "disabled")
        self.entry_frequency.configure(state="readonly" if is_wellness else "disabled")
        self.entry_severity.configure(state="disabled" if is_wellness else "readonly")

    # -------------------------------------------------------
    def load_edit_data_main(self):
        for rec in records:
            if rec["id"] == selected_index:
                self.entry_name.insert(0, rec["label"])
                self.entry_type.insert(0, rec["type"])
                self.entry_desc.insert("1.0", rec["description"])
                self.entry_datetime.insert(0, rec["datetime"])
                self.entry_severity.set(rec["severity"])
                break

    # -------------------------------------------------------
    def save_record(self):
        global selected_source, selected_index

        typ = self.entry_type.get().strip().lower()
        is_wellness = typ.startswith("wellness")

        if is_wellness:
            data = {
                "label": self.entry_name.get().strip(),
                "category": self.entry_category.get(),
                "frequency": self.entry_frequency.get(),
                "description": self.entry_desc.get("1.0", "end-1c").strip(),
                "datetime": self.entry_datetime.get().strip()
            }

            if selected_index is not None and selected_source == "wellness":
                update_wellness_record(selected_index, data)
            else:
                insert_wellness_record(data)

        else:
            data = {
                "label": self.entry_name.get().strip(),
                "type": self.entry_type.get().strip(),
                "description": self.entry_desc.get("1.0", "end-1c").strip(),
                "datetime": self.entry_datetime.get().strip(),
                "severity": self.entry_severity.get()
            }

            if selected_index is not None and selected_source == "main":
                update_record(selected_index, data)
            else:
                insert_record(data)

        self.master.switch_frame(Dashboard)

    # -------------------------------------------------------
    def delete_record(self):
        delete_record_db(selected_index)
        self.master.switch_frame(Dashboard)


# ======================
# WELLNESS HABITS FORM
# ======================
class WellnessHabitsForm(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=BG_COLOR)

        global selected_index, selected_source, quick_type

        tk.Label(self, text="Wellness Habits Form",
                font=("Times New Roman", 22, "bold"),
                bg=BG_COLOR, fg=LABEL_COLOR).pack(pady=15)

        form = tk.Frame(self, bg=FRAME_BG, bd=2, relief="solid",
                        padx=60, pady=18)
        form.pack()

        self.entry_name = self.create_entry(form, "Label:")

        tk.Label(form, text="Category:", bg=FRAME_BG, fg=LABEL_COLOR).pack(anchor="w")
        categories = ["Exercise", "Nutrition", "Sleep", "Self-Care", "Mental Wellness", "Hygiene"]
        self.entry_category = ttk.Combobox(form, values=categories, state="readonly", width=37)
        self.entry_category.pack()

        tk.Label(form, text="Frequency:", bg=FRAME_BG, fg=LABEL_COLOR).pack(anchor="w")
        self.entry_frequency = ttk.Combobox(
            form, values=["Daily", "Weekly", "Routine", "Sometimes"],
            state="readonly", width=37
        )
        self.entry_frequency.pack()

        # ======================================
        # MULTI-LINE DESCRIPTION BOX
        # ======================================
        tk.Label(form, text="Description:", bg=FRAME_BG, fg=LABEL_COLOR).pack(anchor="w")
        self.entry_desc = tk.Text(form, width=30, height=3,
                                bg=ENTRY_BG, fg=ENTRY_FG, insertbackground=ENTRY_FG)
        self.entry_desc.pack()
        self.entry_desc.insert("1.0", "")

        self.entry_datetime = self.create_entry(form, "Date/Time:")

        btns = tk.Frame(self, bg=BG_COLOR)
        btns.pack(side="right", padx=60)

        tk.Button(btns, text="SAVE", font=("Courier New", 9), width=19,
                bg=BTN_COLOR, fg="white",
                command=self.save_record).pack(pady=5)

        tk.Button(btns, text="CANCEL", font=("Courier New", 9), width=19,
                bg=BTN_COLOR, fg="white",
                command=lambda: master.switch_frame(Dashboard)).pack(pady=5)

        if selected_index is not None and selected_source == "wellness":
            tk.Button(btns, text="DELETE", font=("Courier New", 9), width=19,
                    bg="red", fg="white",
                    command=self.delete_record).pack(pady=5)

        tk.Button(btns, text="BACK", font=("Courier New", 9), width=19,
                bg=BTN_COLOR, fg="white",
                command=lambda: master.switch_frame(Dashboard)).pack(pady=5)

        if selected_index is not None and selected_source == "wellness":
            self.load_edit_data_wellness()
        elif quick_type == "WELLNESS_FORM":
            self.entry_name.insert(0, "Wellness Habit")

    # -----------------------------------------
    def create_entry(self, parent, text):
        tk.Label(parent, text=text, bg=FRAME_BG, fg=LABEL_COLOR).pack(anchor="w")
        e = tk.Entry(parent, width=40, bg=ENTRY_BG, fg=ENTRY_FG, insertbackground=ENTRY_FG)
        e.pack()
        return e

    # -----------------------------------------
    def load_edit_data_wellness(self):
        for rec in wellness_records:
            if rec["id"] == selected_index:
                self.entry_name.insert(0, rec["label"])
                self.entry_category.set(rec["category"])
                self.entry_frequency.set(rec["frequency"])
                self.entry_desc.insert("1.0", rec["description"])
                self.entry_datetime.insert(0, rec["datetime"])
                break

    # -----------------------------------------
    def save_record(self):
        data = {
            "label": self.entry_name.get().strip(),
            "category": self.entry_category.get(),
            "frequency": self.entry_frequency.get(),
            "description": self.entry_desc.get("1.0", "end-1c").strip(),
            "datetime": self.entry_datetime.get().strip()
        }

        if selected_index is not None and selected_source == "wellness":
            update_wellness_record(selected_index, data)
        else:
            insert_wellness_record(data)

        self.master.switch_frame(Dashboard)

    # -----------------------------------------
    def delete_record(self):
        delete_wellness_record_db(selected_index)
        self.master.switch_frame(Dashboard)


# ---------------------------
# RUN APP
# ---------------------------
if __name__ == "__main__":
    app = HealthHubApp()
    app.mainloop()
