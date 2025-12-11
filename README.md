<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# Quran Parts PDF Generator

This tool creates beautiful PDF schedules for assigning 30 people to daily Quran recitation parts (called "Juz'"). It automatically rotates names daily starting from a set date, so everyone gets a fair turn. Perfect for mosques, study groups, or family Quran schedules!

## ✨ Key Features

- **Automatic Rotation**: Names rotate daily based on days since start date (Aug 16, 2025)
- **Dual Column Layout**: Shows Juz' 1-15 (right side) and 16-30 (left side) in one table
- **Date Range Generation**: Create PDFs for multiple days at once
- **Full Customization**: Edit names, pick any colors, preview any date
- **Persistent Names**: Names auto-save to `names.txt` so you never lose your list
- **Professional PDFs**: Date headers with weekdays, alternating row colors
- **Arabic Support Toggle**: Optional Arabic text rendering (right-to-left)


## 🌐 Arabic Mode - When to Use It

**Enable Arabic support when:**

- Using Arabic names (نهال, محمد, طيبة, etc.)
- Need proper right-to-left text display
- Headers like "رقم الجزء | الاسم" instead of "Part \# | Name"

**Install extra dependencies:**

```bash
pip install arabic-reshaper python-bidi
```

**Toggle in code:** Set `USE_ARABIC = True` at the top of any version

## 📱 How It Works

```
1. Enter start date → Names rotate based on days since Aug 16, 2025
2. Preview any date → See exact name order for that day
3. Edit names → Changes save automatically
4. Pick colors → Every element customizable
5. Generate → PDFs save to Desktop/Parts folder as MM-DD.pdf
```


## 🛠️ Versions Comparison

| Version | Interface | Colors | Arabic Support | Extras |
| :-- | :-- | :-- | :-- | :-- |
| **v1** | Command line | Fixed | Optional | Basic rotation [v1.py](v1.py) |
| **v2** | Tkinter GUI | Fully customizable | Optional | Date range, name editing [v2.py](v2.py) |
| **v3** | Modern CustomTkinter | Color wheel picker | Optional | Weekday headers [v3.py](v3.py) |

## 🚀 Quick Start (v3 - Recommended)

1. **Basic install** (English only):
```bash
pip install fpdf2 customtkinter
```

2. **Full install** (English + Arabic):
```bash
pip install fpdf2 customtkinter arabic-reshaper python-bidi
```

3. **Run**:
```bash
python v3.py
```

4. **Enable Arabic** (in any version):
```python
# At the top of the file
USE_ARABIC = True  # Set False for English only
```

5. **Default names** (mix Arabic/English - editable):
```
English: ["Nathan", "Michael", "Taylor", "Jessica", "Alex", ...]
Arabic:  ["نهال", "محمد", "طيبة", "تسنيم", "الاء", ...]
```


## 🎨 Customization

- **Dates**: Set start/end dates (YYYY/MM/DD format)
- **Colors**: 8 customizable elements (headers, row backgrounds, numbers, borders)
- **Language**: English or Arabic headers/names (toggle `USE_ARABIC`)
- **Font**: Windows fonts (MAJALLA.TTF for Arabic, Arial for English)
- **Output**: Desktop/Parts folder with daily PDFs


## 📁 Files Structure

```
Parts/
├── 08-16.pdf          # Daily PDFs (MM-DD format)
├── names.txt          # Your custom name list (auto-saved)
├── v1.py              # Basic CLI (English/Arabic toggle)
├── v2.py              # Tkinter GUI (English/Arabic toggle)  
└── v3.py              # Modern CustomTkinter (English/Arabic toggle)
```


## 💡 Example Output

**English Mode:**

```
2025/08/16 Friday
Part # | Name     | Part # | Name
16     | Sophia   | 1      | Nathan
17     | Russell  | 2      | Michael
```

**Arabic Mode:**

```
2025/08/16 الجمعة
رقم الجزء | الاسم    | رقم الجزء | الاسم
16        | شيماء   | 1         | نهال
17        | رسل     | 2         | محمد
```


## 🔧 Requirements

**Core:** `fpdf2`, `customtkinter`
**Arabic (optional):** `arabic-reshaper`, `python-bidi`

## 🙌 Contributing

1. Fork the repo
2. Toggle `USE_ARABIC` for your language needs
3. Add fonts, export formats, or improvements
4. Submit pull request!

**Easy scheduling for any language - English or Arabic!**

