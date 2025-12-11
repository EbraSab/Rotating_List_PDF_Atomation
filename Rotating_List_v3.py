"""
Quran Parts PDF Generator - v3 (English/Arabic Toggle)
Creates daily PDF schedules for 30 people rotating through Quran Juz' assignments.
Toggle USE_ARABIC = True/False at the top for language choice.
"""

import os
from datetime import datetime, timedelta
from fpdf import FPDF
import customtkinter as ctk
from tkinter import messagebox, colorchooser
import tkinter as tk

# ========================================
# TOGGLE LANGUAGE SUPPORT HERE
USE_ARABIC = False  # Set True for Arabic names/headers (requires extra pip installs)

# ========================================
# CONFIGURATION
FONT_PATH = r"C:\Windows\Fonts\arial.ttf"  # Change to MAJALLA.TTF for Arabic
START_DATE = datetime(2025, 8, 16)
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
folder_name = "Parts"  # Changed from Arabic "اجزاء"
folder_path = os.path.join(desktop_path, folder_name)
os.makedirs(folder_path, exist_ok=True)
names_file = os.path.join(folder_path, "names.txt")

# Language content
if USE_ARABIC:
    # Requires: pip install arabic-reshaper python-bidi
    import arabic_reshaper
    from bidi.algorithm import get_display
    
    HEADERS = ["رقم الجزء", "الاسم", "رقم الجزء", "الاسم"]
    DAYS_ARABIC = {
        "Monday": "الاثنين", "Tuesday": "الثلاثاء", "Wednesday": "الأربعاء",
        "Thursday": "الخميس", "Friday": "الجمعة", "Saturday": "السبت", "Sunday": "الأحد"
    }
    DEFAULT_NAMES = [
        "عبدالله", "فاطمة", "أحمد", "مريم", "عمر", "زينب", "خالد", "نور", "يوسف", "سارة",
        "إبراهيم", "عائشة", "محمود", "ليلى", "حسن", "رقية", "علي", "سمية", "مصطفى", "هدى",
        "بشرى", "سلمى", "عبدالرحمن", "أسماء", "طارق", "نادية", "فيصل", "منى", "سعيد", "جميلة"
    ]

    
    def reshape_arabic(text):
        reshaped = arabic_reshaper.reshape(text)
        return get_display(reshaped)
else:
    HEADERS = ["Part #", "Name", "Part #", "Name"]
    DAYS_ARABIC = {}
    DEFAULT_NAMES = [
        "Nathan", "Michael", "Taylor", "Jessica", "Alex", "Sarah", "David", "Emily", 
        "James", "Olivia", "Sarah", "David", "Michael", "Andrew", "Henry", 
        "Bella", "Rachel", "Samuel", "Oliver", "Mia", "Riley", "Isaac", 
        "Noah James", "Sophia", "Russell", "Nora", "Susan", "Noah Andrew", "Amy", "Oscar"
    ]
    def reshape_arabic(text):
        return text

# ========================================
# HELPERS
def load_names():
    if os.path.exists(names_file):
        with open(names_file, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    return DEFAULT_NAMES.copy()

def save_names(names_list):
    with open(names_file, "w", encoding="utf-8") as f:
        for name in names_list:
            f.write(name + "\n")

def days_since_start(start_date, current_date):
    delta = current_date.date() - start_date.date()
    return delta.days if delta.days >= 0 else 0

def rotate_list(lst, n):
    n = n % len(lst)
    return lst[-n:] + lst[:-n]

def hex_to_rgb(hex_color):
    hex_color = (hex_color or "#000000").lstrip("#")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def get_day_name(date):
    day_english = date.strftime("%A")
    return DAYS_ARABIC.get(day_english, day_english)

# ========================================
# PDF GENERATION
class PDF(FPDF):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_font('Arial', '', FONT_PATH, uni=True)
        self.add_font('Arial', 'B', FONT_PATH, uni=True)

def generate_pdf(names, day_num, date, filename, colors):
    pdf = PDF()
    pdf.set_margins(5, 5, 5)
    pdf.add_page()
    
    # Header with date and day name
    pdf.set_font("Arial", 'B', 38)
    header_text = f"{date.strftime('%Y/%m/%d')} {get_day_name(date)}"
    pdf.cell(0, 15, reshape_arabic(header_text), ln=1, align='C')
    pdf.ln(5)
    
    # Table setup
    col_name_w, col_num_w, row_h = 75, 20, 15
    
    # Header row
    header_fill_rgb = hex_to_rgb(colors.get("header_fill"))
    header_text_rgb = hex_to_rgb(colors.get("header_text"))
    border_rgb = hex_to_rgb(colors.get("borders"))
    
    pdf.set_draw_color(*border_rgb)
    pdf.set_fill_color(*header_fill_rgb)
    pdf.set_text_color(*header_text_rgb)
    pdf.set_line_width(1.2)
    pdf.set_font("Arial", 'B', 16)
    
    for header in HEADERS:
        pdf.cell(col_num_w if "رقم" in header or "Part" in header else col_name_w, 
                row_h, reshape_arabic(header), border=1, align='C', fill=True)
    pdf.ln()
    
    # Data rows
    row1_rgb = hex_to_rgb(colors.get("row_bg1"))
    row2_rgb = hex_to_rgb(colors.get("row_bg2"))
    text_rgb = hex_to_rgb(colors.get("text"))
    numbers_rgb = hex_to_rgb(colors.get("numbers"))
    names_bg_rgb = hex_to_rgb(colors.get("names_bg"))
    
    pdf.set_draw_color(*border_rgb)
    pdf.set_line_width(1.2)
    
    half = len(names) // 2
    numbers_left, numbers_right = list(range(1, 16)), list(range(16, 31))
    right_names, left_names = names[half:], names[:half]
    
    for i in range(half):
        row_fill = row1_rgb if i % 2 == 0 else row2_rgb
        
        # Right column number
        pdf.set_fill_color(*row_fill)
        pdf.set_text_color(*numbers_rgb)
        pdf.set_font("Arial", 'B', 28)
        pdf.cell(col_num_w, row_h, str(numbers_right[i]), border=1, align='C', fill=True)
        
        # Right column name
        pdf.set_fill_color(*names_bg_rgb)
        pdf.set_text_color(*text_rgb)
        pdf.cell(col_name_w, row_h, reshape_arabic(right_names[i]), border=1, align='C', fill=True)
        
        # Left column number
        pdf.set_fill_color(*row_fill)
        pdf.set_text_color(*numbers_rgb)
        pdf.cell(col_num_w, row_h, str(numbers_left[i]), border=1, align='C', fill=True)
        
        # Left column name
        pdf.set_fill_color(*names_bg_rgb)
        pdf.set_text_color(*text_rgb)
        pdf.cell(col_name_w, row_h, reshape_arabic(left_names[i]), border=1, align='C', fill=True)
        
        pdf.ln()
    
    pdf.output(filename)

# ========================================
# MODERN GUI
class PartsApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("green")
        
        self.title(f"📄 Quran Parts PDF Generator - {'Arabic' if USE_ARABIC else 'English'} Mode")
        self.geometry("950x750")
        
        today_str = datetime.now().strftime("%Y/%m/%d")
        
        # Title
        title = ctk.CTkLabel(self, text="📅 Parts PDF Scheduler", font=ctk.CTkFont(size=28, weight="bold"))
        title.grid(row=0, column=0, columnspan=2, pady=20)
        
        # Status label showing language mode
        lang_status = ctk.CTkLabel(self, text=f"Language: {'Arabic' if USE_ARABIC else 'English'}", 
                                  font=ctk.CTkFont(size=14), text_color="orange" if USE_ARABIC else "green")
        lang_status.grid(row=0, column=2, padx=20)
        
        # Date Frame
        date_frame = ctk.CTkFrame(self, corner_radius=15)
        date_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        
        for i, label in enumerate(["Start Date (YYYY/MM/DD):", "End Date (YYYY/MM/DD):", "Preview Date:"]):
            ctk.CTkLabel(date_frame, text=label).grid(row=i, column=0, padx=5, pady=5, sticky="e")
        
        self.start_date_entry = ctk.CTkEntry(date_frame, width=150)
        self.start_date_entry.insert(0, today_str)
        self.start_date_entry.grid(row=0, column=1, padx=5, pady=5)
        
        self.end_date_entry = ctk.CTkEntry(date_frame, width=150)
        self.end_date_entry.insert(0, today_str)
        self.end_date_entry.grid(row=1, column=1, padx=5, pady=5)
        
        self.preview_date_entry = ctk.CTkEntry(date_frame, width=150)
        self.preview_date_entry.insert(0, today_str)
        self.preview_date_entry.grid(row=2, column=1, padx=5, pady=5)
        self.preview_date_entry.bind("<KeyRelease>", self.update_names_order)
        
        ctk.CTkButton(date_frame, text="Update Preview", command=self.update_names_order)\
          .grid(row=3, column=0, columnspan=2, pady=10)
        
        # Names Frame
        names_frame = ctk.CTkFrame(self, corner_radius=15)
        names_frame.grid(row=1, column=1, rowspan=2, sticky="nsew", padx=10, pady=10)
        
        self.names_header = ctk.CTkLabel(names_frame, text="Edit names below:", 
                                        font=ctk.CTkFont(size=16, weight="bold"))
        self.names_header.pack(pady=8)
        
        self.original_names = load_names()
        self.left_entries = []
        self.right_entries = []
        
        cols_frame = ctk.CTkFrame(names_frame)
        cols_frame.pack(fill="both", expand=True, padx=6, pady=6)
        
        # Right column (16-30)
        right_col = ctk.CTkFrame(cols_frame)
        right_col.pack(side="left", fill="both", expand=True, padx=(5, 10))
        ctk.CTkLabel(right_col, text="Parts 16-30", font=ctk.CTkFont(size=14, weight="bold")).pack()
        
        # Left column (1-15)
        left_col = ctk.CTkFrame(cols_frame)
        left_col.pack(side="left", fill="both", expand=True, padx=(10, 5))
        ctk.CTkLabel(left_col, text="Parts 1-15", font=ctk.CTkFont(size=14, weight="bold")).pack()
        
        # Create name entry fields
        for i in range(15):
            # Left column (1-15)
            l_row = ctk.CTkFrame(left_col)
            l_row.pack(fill="x", pady=2)
            ctk.CTkLabel(l_row, text=str(i+1), width=30).pack(side="left")
            ent_l = ctk.CTkEntry(l_row)
            ent_l.pack(side="left", fill="x", expand=True, padx=4)
            ent_l.bind("<KeyRelease>", self.auto_save_names)
            self.left_entries.append(ent_l)
            
            # Right column (16-30)
            r_row = ctk.CTkFrame(right_col)
            r_row.pack(fill="x", pady=2)
            ctk.CTkLabel(r_row, text=str(i+16), width=30).pack(side="left")
            ent_r = ctk.CTkEntry(r_row)
            ent_r.pack(side="left", fill="x", expand=True, padx=4)
            ent_r.bind("<KeyRelease>", self.auto_save_names)
            self.right_entries.append(ent_r)
        
        self.update_names_order()
        
        # Color Frame
        color_frame = ctk.CTkFrame(self, corner_radius=10)
        color_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        
        ctk.CTkLabel(color_frame, text="🎨 Customize PDF Colors", 
                    font=ctk.CTkFont(size=16, weight="bold"))\
          .grid(row=0, column=0, columnspan=3, pady=(10, 15))
        
        color_defs = [
            ("header_fill", "Header Fill", "#000000"),
            ("header_text", "Header Text", "#FFFFFF"),
            ("row_bg1", "Row 1 Background", "#ababab"),
            ("row_bg2", "Row 2 Background", "#FFFFFF"),
            ("names_bg", "Names Background", "#000000"),
            ("text", "Text Color", "#FFFFFF"),
            ("numbers", "Numbers Color", "#ff0000"),
            ("borders", "Borders Color", "#00af50"),
        ]
        
        self.color_vars = {}
        for i, (key, label, default) in enumerate(color_defs):
            ctk.CTkLabel(color_frame, text=f"{label}:", 
                        font=ctk.CTkFont(size=12))\
              .grid(row=i+1, column=0, sticky="e", padx=8, pady=5)
            
            color_var = tk.StringVar(value=default)
            self.color_vars[key] = color_var
            
            color_entry = ctk.CTkEntry(color_frame, textvariable=color_var, width=100)
            color_entry.grid(row=i+1, column=1, padx=5, pady=5)
            
            btn = ctk.CTkButton(
                color_frame,
                text="🎨",
                width=40,
                fg_color=default,
                hover_color="#666",
                command=lambda var=color_var, b=None: None
            )
            btn.grid(row=i + 1, column=2, padx=5, pady=5)

            # fix closure capture to use correct button
            btn.configure(command=lambda var=color_var, button=btn: self.choose_color(var, button))
        
        # Generate Button
        btn_frame = ctk.CTkFrame(self)
        btn_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=15, sticky="ew")
        
        ctk.CTkButton(btn_frame, text="🚀 Generate PDFs", font=ctk.CTkFont(size=20, weight="bold"),
                     height=50, command=self.generate_pdfs)\
          .pack(pady=15, padx=20, fill="x")
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
    
    def update_names_order(self, event=None):
        try:
            preview_date = datetime.strptime(self.preview_date_entry.get().strip(), "%Y/%m/%d")
            day_num = days_since_start(START_DATE, preview_date)
            rotated_names = rotate_list(self.original_names, day_num)
            self.names_header.configure(text=f"Preview for {preview_date.strftime('%Y/%m/%d')} (Day {day_num}):")
            
            for entry in self.left_entries + self.right_entries:
                entry.delete(0, "end")
            for i in range(15):
                if i < len(rotated_names):
                    self.left_entries[i].insert(0, rotated_names[i])
                if i + 15 < len(rotated_names):
                    self.right_entries[i].insert(0, rotated_names[i + 15])
        except:
            self.names_header.configure(text="Invalid date - showing original order:")
            for i, entry in enumerate(self.left_entries + self.right_entries):
                if i < len(self.original_names):
                    entry.delete(0, "end")
                    entry.insert(0, self.original_names[i])
    
    def auto_save_names(self, event=None):
        try:
            preview_date = datetime.strptime(self.preview_date_entry.get().strip(), "%Y/%m/%d")
            day_num = days_since_start(START_DATE, preview_date)
            rotated = [e.get().strip() for e in self.left_entries + self.right_entries]
            if len(rotated) == 30:
                reverse_rotation = -day_num % 30
                original = rotate_list(rotated, reverse_rotation)
                self.original_names = original
                save_names(original)
        except:
            pass
    
    def choose_color(self, color_var, button):
        color_code = colorchooser.askcolor(title="Choose Color")[1]
        if color_code:
            color_var.set(color_code)
            try:
                button.configure(fg_color=color_code)
            except:
                pass
    
    def generate_pdfs(self):
        try:
            start_date = datetime.strptime(self.start_date_entry.get().strip(), "%Y/%m/%d")
            end_date = datetime.strptime(self.end_date_entry.get().strip(), "%Y/%m/%d")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid dates (YYYY/MM/DD)")
            return
        
        if start_date > end_date:
            messagebox.showerror("Error", "Start date must be before end date")
            return
        
        if len(self.original_names) != 30 or any(not n.strip() for n in self.original_names):
            messagebox.showerror("Error", "Please fill all 30 names")
            return
        
        colors = {k: v.get() for k, v in self.color_vars.items()}
        current = start_date
        generated = 0
        
        while current <= end_date:
            day_num = days_since_start(START_DATE, current)
            rotated = rotate_list(self.original_names, day_num)
            filename = os.path.join(folder_path, f"{current.strftime('%m-%d')}.pdf")
            generate_pdf(rotated, day_num, current, filename, colors)
            current += timedelta(days=1)
            generated += 1
        
        messagebox.showinfo("Success", 
                           f"✅ Generated {generated} PDFs in:\n{folder_path}")

if __name__ == "__main__":
    print("📄 Quran Parts PDF Generator")
    print(f"Language mode: {'Arabic' if USE_ARABIC else 'English'}")
    if USE_ARABIC:
        print("💡 Install Arabic support: pip install arabic-reshaper python-bidi")
    print(f"Output folder: {folder_path}")
    app = PartsApp()
    app.mainloop()
