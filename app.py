import pytesseract
pytesseract.pytesseract.tesseract_cmd = '/opt/homebrew/bin/tesseract'

from flask import Flask, request, jsonify
from flask_cors import CORS
import pytesseract
from PIL import Image
import io
import re

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

def extract_date_and_amount(text):
    date_pattern = re.compile(r'\d{4}/\d{2}/\d{2}|\d{2}/\d{2}/\d{4}')
    amount_pattern = re.compile(r'\d+\.\d{2}')

    date_match = date_pattern.search(text)
    amount_match = amount_pattern.search(text)

    date = date_match.group() if date_match else 'Not found'
    amount = amount_match.group() if amount_match else 'Not found'
    return date, amount

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    image = Image.open(io.BytesIO(file.read()))
    text = pytesseract.image_to_string(image)
    date, amount = extract_date_and_amount(text)

    return jsonify({"date": date, "amount": amount})

if __name__ == '__main__':
    app.run(debug=True)