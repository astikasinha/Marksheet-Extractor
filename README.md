#  Marksheet Table Extractor from PDF

A smart PDF parsing tool designed to extract structured tabular data (such as student marks) from academic mark sheets and convert them into Excel files for easy analysis and storage.

---

##  Features

- Upload academic mark sheets in PDF format
- Automatically extracts subject-wise marks and grades
- Converts tabular data into `.xlsx` (Excel) format
- Supports multi-page PDFs
- Skips non-tabular text or malformed pages
- Built with Python, Flask, pdfplumber, and Pandas
- 10MB upload limit for efficiency and security

---

## How It Works

1. Upload a marksheet PDF via the web interface
2. The backend parses the file using `pdfplumber`
3. It detects subject rows using rule-based logic
4. Extracted tables are saved as `.xlsx` files
5. If multiple tables are found, they are zipped into `tables.zip`
6. Download starts automatically!

---

##  Technologies Used

| Tech           | Role                                |
|----------------|-------------------------------------|
| **Flask**      | Web server backend                  |
| **pdfplumber** | Text extraction from PDF            |
| **Pandas**     | Data processing and Excel export    |
| **HTML/CSS/JS**| Custom frontend with upload UI      |

---

## Screenshot


![image](https://github.com/user-attachments/assets/04366103-c317-4df2-82c6-e0f09e012f68)

![image](https://github.com/user-attachments/assets/6c02b017-cd12-46d9-90d8-0ad31d18d7bb)



