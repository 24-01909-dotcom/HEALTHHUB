# HEALTHHUB

Here’s a detailed README for your **HealthHub** project, modeled after the format you provided for the Task Manager, but adapted for your JSON-based Tkinter app:

---

# HealthHub: A Wellness Tracking and Information System

This repository provides a Tkinter-based desktop application that demonstrates how to manage personal health and wellness records using a lightweight JSON storage system and a fully featured CRUD workflow.

Use this README to understand the project structure, how data flows through the app, and how to safely extend or modify the code.

---

## 1. What You Get Out of the Box

* **Tkinter UI** with multiple screens: Start, About, Dashboard, Saved Info, Record Form, and Wellness Habits Form.
* **CRUD functionality** for both main records (Symptoms, Medicine, Appointments) and wellness habits.
* **JSON storage** using `healthhub_records.json` and `healthhub_wellness.json` with automatic save/load.
* **Reusable data layer functions** for fetching, inserting, updating, and deleting records.
* **Quick-add feature** for adding records or wellness habits directly from the dashboard.
* **Multi-screen navigation** with `switch_frame` method.
* **Dynamic form behavior** for wellness vs main records.

---

## 2. Quick Start

1. **Install Python** 3.11+ (Tkinter and Pillow required for GUI and images):

   ```bash
   pip install Pillow
   ```

2. **Prepare image assets**:

   Place `FRONT PAGE.png` inside an `IMAGE` folder in the project root.

3. **Launch the app**:

   ```bash
   python healthhub.py
   ```

4. **First interaction**:

   * Start the app from the *Start* screen.
   * Explore the *Dashboard*, view records, and add new entries using *Quick Add*.
   * Save your data automatically—no database setup needed.

---

## 3. Repository Map

```
healthhub/
├── IMAGE/                      # Folder for background images
├── healthhub.py                # Main app file (Tkinter + JSON CRUD)
├── healthhub_records.json      # Auto-created main records storage
├── healthhub_wellness.json     # Auto-created wellness records storage
└── README.md                   # You are here
```

---

## 4. How the Pieces Fit Together

1. `healthhub.py` contains the full application.
2. **Data Layer Functions**:

   * `fetch_all_records()`: Retrieve all records in sorted order.
   * `insert_record(data)`, `update_record(record_id, data)`, `delete_record_db(record_id)`: CRUD operations for main records.
   * `insert_wellness_record(data)`, `update_wellness_record(record_id, data)`, `delete_wellness_record_db(record_id)`: CRUD for wellness habits.
   * Auto-save occurs after every insert/update/delete.
3. **Main Application (`HealthHubApp`)**:

   * Loads saved JSON data on startup.
   * Manages screen navigation with `switch_frame`.
4. **Screens**:

   * `StartScreen`: App landing page with *Start* and *About* buttons.
   * `AboutScreen`: Describes the purpose of HealthHub.
   * `Dashboard`: Central screen with table view, filters, and quick-add actions.
   * `SavedInfoScreen`: Read-only table of all saved records.
   * `RecordForm`: Form for main records (Symptoms, Medicine, Appointments).
   * `WellnessHabitsForm`: Form for wellness habits (Exercise, Nutrition, Sleep, etc.).
5. **State Management**:

   * Global variables: `selected_index`, `selected_source`, `quick_type`.
   * ID counters: `next_id` for main records, `next_wellness_id` for wellness records.

---

## 5. Screen-by-Screen Guide

* **StartScreen**: Background image + app title. Buttons navigate to Dashboard or About.
* **AboutScreen**: Static text describing HealthHub, with a back button.
* **Dashboard**:

  * Left panel: Filters and navigation.
  * Center panel: `ttk.Treeview` showing all records.
  * Right panel: Quick-add buttons for main records and wellness habits.
* **SavedInfoScreen**: Table of all records with detailed columns.
* **RecordForm / WellnessHabitsForm**:

  * Dynamic forms that adjust fields depending on the type (main vs wellness).
  * Supports edit, delete, and save operations.

---

## 6. Data Layer Details

* **Files**:

  * `healthhub_records.json` for main records.
  * `healthhub_wellness.json` for wellness habits.

* **Structure of records**:

  **Main records:**

  ```json
  {
    "id": 1,
    "label": "Headache",
    "type": "Symptoms",
    "description": "Mild headache",
    "datetime": "2025-12-12 08:00",
    "severity": "Mild"
  }
  ```

  **Wellness records:**

  ```json
  {
    "id": 1,
    "label": "Morning Jog",
    "category": "Exercise",
    "frequency": "Daily",
    "description": "30-minute jog",
    "datetime": "2025-12-12 06:30"
  }
  ```

* **Auto-save:** Every insert, update, or delete automatically updates JSON files.

---

## 7. CRUD Operations

All CRUD actions are handled through functions in the data layer:

* **Fetch all records:** `fetch_all_records()`
* **Insert record:** `insert_record(data)` / `insert_wellness_record(data)`
* **Update record:** `update_record(record_id, data)` / `update_wellness_record(record_id, data)`
* **Delete record:** `delete_record_db(record_id)` / `delete_wellness_record_db(record_id)`

Screens like `Dashboard`, `RecordForm`, and `WellnessHabitsForm` call these functions to reflect changes in the UI and save to disk.

---

## 8. Working With the Code

* **Add a new screen:** Subclass `tk.Frame`, implement the UI and button callbacks, and switch frames via `self.master.switch_frame(NewScreen)`.
* **Add a new record type:** Extend `fetch_all_records()` or add new JSON files with similar CRUD helpers.
* **Modify styling:** Update constants like `BG_COLOR`, `BTN_COLOR`, `ENTRY_BG`, etc.
* **Image assets:** Replace `FRONT PAGE.png` for custom splash screens.

---

## 9. Tkinter Notes

* **Treeview:** Used for tabular display with selection binding.
* **Text widgets:** For multi-line descriptions.
* **Combobox:** For categories, frequency, and severity selections.
* **Button commands:** Trigger CRUD operations or screen navigation.
* **Dynamic form fields:** Adjust enabled/disabled state based on record type.

---

## 10. Widget Reference

| Widget         | Purpose                          | Example                                    |
| -------------- | -------------------------------- | ------------------------------------------ |
| `tk.Label`     | Display headings or field labels | `tk.Label(self, text="Label:")`            |
| `tk.Entry`     | Single-line input                | `self.entry_name = tk.Entry(...)`          |
| `tk.Text`      | Multi-line input                 | `self.entry_desc = tk.Text(...)`           |
| `ttk.Combobox` | Dropdown selection               | `self.entry_severity = ttk.Combobox(...)`  |
| `tk.Button`    | Trigger actions                  | `tk.Button(..., command=self.save_record)` |
| `ttk.Treeview` | Display tabular records          | `self.tree = ttk.Treeview(...)`            |
| `tk.Frame`     | Container for widgets            | `form = tk.Frame(self)`                    |
| `messagebox`   | Alerts/confirmations             | `messagebox.showwarning(...)`              |

---

## 11. Workflow Overview

1. **StartScreen → Dashboard**

   * Users start the app and navigate to the dashboard.

2. **Dashboard → Quick Add / Edit Form**

   * Select “Quick Add” or existing record → RecordForm or WellnessHabitsForm.

3. **Form → Save / Delete → Dashboard**

   * Save updates JSON file and refresh dashboard.
   * Delete removes record and updates dashboard immediately.

4. **Dashboard → Saved Info Screen**

   * Provides a read-only overview of all saved records.

---

Trace the flow starting at `healthhub.py` to understand how GUI actions trigger JSON-based CRUD operations. This provides a full picture of the HealthHub architecture and how screens, forms, and records interact seamlessly.

---

### Information Table

| | Name | Role |
|----------|----------|----------|
|<img src="images/Micha.jpg" width="120">| Panaligan, Michaela C. |

