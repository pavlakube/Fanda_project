from flask import Flask, request, jsonify
import PyPDF2

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return 'No file part in the request', 400

    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400

    if file and allowed_file(file.filename):
        pdf = file.read()
        json_data = convert_pdf_to_json(pdf)
        return jsonify(json_data)

    return 'Invalid file format', 400

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'pdf'

def convert_pdf_to_json(pdf):
    pdf_reader = PyPDF2.PdfReader(pdf)

    json_data = []
    for page in pdf_reader.pages:
        json_data.append(page.extract_text())

    return json_data

if __name__ == '__main__':
    app.run()
