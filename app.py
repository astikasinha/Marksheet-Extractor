from flask import Flask, request, jsonify, send_file
import pandas as pd
import pdfplumber
import os
import zipfile
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10 MB limit

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return "✅ Backend is running!"

@app.route('/upload', methods=['POST'])
def upload_file():
    print("Received POST request to /upload")

    if 'file' not in request.files:
        print("No file part in request")
        return jsonify({"error": "No file part in request."}), 400

    file = request.files['file']

    if file.filename == '':
        print("No selected file")
        return jsonify({"error": "No selected file."}), 400

    if not file.filename.endswith('.pdf'):
        print("Invalid file type")
        return jsonify({"error": "Invalid file type. Please upload a PDF."}), 400

    filename = secure_filename(file.filename)
    pdf_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(pdf_path)
    print(f"Saved file to {pdf_path}")

    try:
        tables = []
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages, start=1):
                table = page.extract_table()
                if table:
                    df = pd.DataFrame(table[1:], columns=table[0])
                    tables.append((page_num, df))

        os.remove(pdf_path)

        if not tables:
            return jsonify({"error": "No tables found in the PDF."}), 400

        output_files = []
        for i, (page_num, table) in enumerate(tables):
            output_file = f"table_page_{page_num}.xlsx"
            table.to_excel(output_file, index=False)
            output_files.append(output_file)

        if len(output_files) == 1:
            return_data = send_file(output_files[0], as_attachment=True)
            os.remove(output_files[0])
            return return_data
        else:
            zip_filename = 'tables.zip'
            with zipfile.ZipFile(zip_filename, 'w') as zipf:
                for f in output_files:
                    zipf.write(f)
                    os.remove(f)
            return_data = send_file(zip_filename, as_attachment=True)
            os.remove(zip_filename)
            return return_data

    except Exception as e:
        print("Error during processing:", str(e))
        if os.path.exists(pdf_path):
            os.remove(pdf_path)
        return jsonify({"error": f"Error processing PDF: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
