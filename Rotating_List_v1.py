"""
Quran Parts PDF Generator - v1 (CLI Version with English/Arabic Toggle)
Creates daily PDF schedules for 30 people rotating through Quran Juz' assignments.
Toggle USE_ARABIC = True/False at the top for language choice.
"""

from fpdf import FPDF
import os
from datetime import datetime
# ========================================
# TOGGLE LANGUAGE SUPPORT HERE
USE_ARABIC = False  # Set True for Arabic names/headers (requires extra pip installs)

# ========================================
# CONFIGURATION
FONT_PATH = r"C:\Windows\Fonts\arial.ttf"  # Change to MAJALLA.TTF for Arabic
START_DATE = datetime(2025, 8, 16)

desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
date_str = datetime.now().strftime("%m-%d")
pdf_filename = f"{date_str}.pdf"
pdf_path = os.path.join(desktop_path, pdf_filename)

# Language content
if USE_ARABIC:
    # Requires: pip install arabic-reshaper python-bidi
    try:
        import arabic_reshaper
        from bidi.algorithm import get_display
        
        HEADERS = ["رقم الجزء", "الاسم", "رقم الجزء", "الاسم"]
        DAYS_ARABIC = {
            "Monday": "الاثنين", "Tuesday": "الثلاثاء", "Wednesday": "الأربعاء",
            "Thursday": "الخميس", "Friday": "الجمعة", "Saturday": "السبت", "Sunday": "الأحد"
        }
        NAMES = [
            "نهال", "محمد", "طيبة", "تسنيم", "الاء", "صباح", "يوم", "هدى", "نجلة", "سوسن",
            "صباح", "يوم", "محمد", "احمد", "حمودي", "بيداء", "رشا", "سعد", "علي", "مها",
            "ريم", "ابراهيم", "نور اسامة", "شيماء", "رسل", "نبا", "سعاد", "نور احمد", "امي", "أسامة"
        ]
        
        def reshape_arabic(text):
            reshaped = arabic_reshaper.reshape(text)
            return get_display(reshaped)
            
        def get_day_name(date):
            day_english = date.strftime("%A")
            return DAYS_ARABIC.get(day_english, day_english)
            
    except ImportError:
        print("⚠️ Arabic libraries not found. Install: pip install arabic-reshaper python-bidi")
        USE_ARABIC = False
        HEADERS = ["Part #", "Name", "Part #", "Name"]
        NAMES = [
            "Nathan", "Michael", "Taylor", "Jessica", "Alex", "Sarah", "David", "Emily", 
            "James", "Olivia", "Sarah", "David", "Michael", "Andrew", "Henry", 
            "Bella", "Rachel", "Samuel", "Oliver", "Mia", "Riley", "Isaac", 
            "Noah James", "Sophia", "Russell", "Nora", "Susan", "Noah Andrew", "Amy", "Oscar"
        ]
        def reshape_arabic(text):
            return text
        def get_day_name(date):
            return date.strftime("%A")
else:
    HEADERS = ["Part #", "Name", "Part #", "Name"]
    NAMES = [
        "Nathan", "Michael", "Taylor", "Jessica", "Alex", "Sarah", "David", "Emily", 
        "James", "Olivia", "Sarah", "David", "Michael", "Andrew", "Henry", 
        "Bella", "Rachel", "Samuel", "Oliver", "Mia", "Riley", "Isaac", 
        "Noah James", "Sophia", "Russell", "Nora", "Susan", "Noah Andrew", "Amy", "Oscar"
    ]
    def reshape_arabic(text):
        return text
    def get_day_name(date):
        return date.strftime("%A")

# ========================================
# CORE LOGIC
def days_since_start(start_date):
    today = datetime.now()
    delta = today.date() - start_date.date()
    return delta.days if delta.days >= 0 else 0

def rotate_list(lst, n):
    n = n % len(lst)
    return lst[-n:] + lst[:-n]

# ========================================
# PDF CLASS
class PDF(FPDF):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_font('Arial', '', FONT_PATH, uni=True)
        self.add_font('Arial', 'B', FONT_PATH, uni=True)

    def header(self):
        self.set_font('Arial', 'B', 25)

def generate_pdf(names, day_num, date, filename):
    pdf = PDF()
    pdf.set_margins(5, 5, 5)
    pdf.add_page()

    # Title with date and day name
    pdf.set_font("Arial", 'B', 35)
    header_text = f"{date.strftime('%Y/%m/%d')} {get_day_name(date)}"
    pdf.cell(0, 15, reshape_arabic(header_text), ln=1, align='C')
    pdf.ln(5)

    col_name_w = 75
    col_num_w = 20
    row_h = 15

    # Header formatting
    pdf.set_fill_color(0, 51, 102)  # dark blue
    pdf.set_text_color(255, 255, 255)  # white
    pdf.set_line_width(0.5)

    pdf.set_font("Arial", 'B', 16)
    for header in HEADERS:
        pdf.cell(col_num_w if "Part" in header or "رقم" in header else col_name_w, 
                row_h, reshape_arabic(header), border=1, align='C', fill=True)
    pdf.ln()

    # Colors
    light_blue = (173, 216, 230)  # light blue
    white = (255, 255, 255)
    red_color = (204, 0, 0)
    green_border = (0, 128, 0)
    pdf.set_draw_color(*green_border)

    half = len(names) // 2
    numbers_left = list(range(1, 16))
    numbers_right = list(range(16, 31))
    right_names = names[half:]
    left_names = names[:half]

    for i in range(half):
        # Alternate row fill color
        row_fill = light_blue if i % 2 == 0 else white

        # Right side number (bold red)
        pdf.set_fill_color(*row_fill)
        pdf.set_text_color(*red_color)
        pdf.set_font("Arial", 'B', 25)
        pdf.cell(col_num_w, row_h, str(numbers_right[i]), border=1, align='C', fill=True)

        # Right side name (bold black)
        pdf.set_fill_color(*row_fill)
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Arial", 'B', 25)
        pdf.cell(col_name_w, row_h, reshape_arabic(right_names[i]), border=1, align='C', fill=True)

        # Left side number (bold red)
        pdf.set_fill_color(*row_fill)
        pdf.set_text_color(*red_color)
        pdf.set_font("Arial", 'B', 25)
        pdf.cell(col_num_w, row_h, str(numbers_left[i]), border=1, align='C', fill=True)

        # Left side name (bold black)
        pdf.set_fill_color(*row_fill)
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Arial", 'B', 25)
        pdf.cell(col_name_w, row_h, reshape_arabic(left_names[i]), border=1, align='C', fill=True)

        pdf.ln()

    pdf.output(filename)

# ========================================
# MAIN
def main():
    print("📄 Quran Parts PDF Generator v1 (CLI)")
    print(f"Language mode: {'Arabic' if USE_ARABIC else 'English'}")
    if USE_ARABIC:
        print("💡 Arabic support enabled (arabic-reshaper + python-bidi installed)")
    
    day_num = days_since_start(START_DATE)
    print(f"Today is day {day_num} since start date ({START_DATE.strftime('%Y/%m/%d')})")
    
    rotated_names = rotate_list(NAMES, day_num)
    print(f"Generating PDF for today: {pdf_filename}")
    print(f"Output: {pdf_path}")
    
    generate_pdf(rotated_names, day_num, datetime.now(), pdf_path)
    print("✅ PDF generated successfully on Desktop!")
    print("\nPreview of today's assignment:")
    print("Parts 1-15:", rotated_names[:15])
    print("Parts 16-30:", rotated_names[15:])

if __name__ == "__main__":
    main()
