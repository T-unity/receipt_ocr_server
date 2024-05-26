import pytesseract
pytesseract.pytesseract.tesseract_cmd = '/opt/homebrew/bin/tesseract'

import pytesseract
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
import io
import re

# Set up logging
logging.basicConfig(filename='app.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s')

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

    # Log the image mode and size
    logging.debug(f"Image mode: {image.mode}, size: {image.size}")

    # Extract text from image using pytesseract
    text = pytesseract.image_to_string(image)

    # Log the extracted text
    logging.debug(f"Extracted text: {text}")

    # Extract date and amount from the text
    date, amount = extract_date_and_amount(text)

    # Log the extracted date and amount
    logging.debug(f"Extracted date: {date}, amount: {amount}")

    return jsonify({"date": date, "amount": amount})

if __name__ == '__main__':
    app.run(debug=True)