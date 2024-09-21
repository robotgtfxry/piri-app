from flask import Flask, send_file, jsonify
import qrcode
import io
import uuid
from datetime import datetime, timedelta

app = Flask(__name__)

# Funkcja generowania unikalnego tekstu (np. ID użytkownika)
def generate_unique_text():
    user_id = str(uuid.uuid4())
    expiration_time = datetime.now() + timedelta(minutes=2)  # Tekst ważny 2 minuty
    return f"UserID: {user_id}, ExpireAt: {expiration_time.strftime('%Y-%m-%d %H:%M:%S')}"

# Funkcja generowania kodu QR z tekstu
def generate_qr_code(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    img = qr.make_image(fill='black', back_color='white')
    
    # Zapisz obraz do pamięci (strumień IO)
    img_io = io.BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)
    
    return img_io

# Endpoint do generowania i zwracania kodu QR
@app.route('/generate_qr', methods=['GET'])
def generate_qr():
    # Generowanie unikalnego tekstu
    unique_text = generate_unique_text()
    
    # Generowanie obrazu kodu QR
    img_io = generate_qr_code(unique_text)
    
    # Zwrócenie kodu QR jako pliku PNG
    return send_file(img_io, mimetype='image/png')

# Start serwera
if __name__ == '__main__':
    app.run(debug=True)
