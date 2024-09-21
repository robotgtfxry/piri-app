from flask import Flask, request, jsonify, send_file
import qrcode
import io
import uuid
from datetime import datetime, timedelta

app = Flask(__name__)

# Funkcja generowania unikalnego tekstu (np. ID użytkownika)
def generate_unique_text():
    user_id = str(uuid.uuid4())
    expiration_time = datetime.now() + timedelta(minutes=2)  # Tekst ważny przez 2 minuty
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

# Funkcja do sprawdzania, czy kod QR wygasł
def is_code_expired(expiration_time_str):
    expiration_time = datetime.strptime(expiration_time_str, '%Y-%m-%d %H:%M:%S')
    return datetime.now() > expiration_time

# Endpoint do walidacji kodu QR
@app.route('/validate_qr', methods=['POST'])
def validate_qr():
    # Pobranie danych z żądania (zakodowanych w QR)
    data = request.json.get('data')
    
    # Podziel dane na części (np. "UserID: xxx, ExpireAt: yyy")
    try:
        parts = dict(item.split(": ") for item in data.split(", "))
        user_id = parts["UserID"]
        expire_at = parts["ExpireAt"]
    except:
        return jsonify({"status": "error", "message": "Invalid QR code format"}), 400
    
    # Sprawdzenie, czy kod wygasł
    if is_code_expired(expire_at):
        return jsonify({"status": "error", "message": "QR code has expired"}), 400
    
    # Jeśli wszystko się zgadza, kod jest poprawny
    return jsonify({"status": "success", "message": "QR code is valid", "user_id": user_id})

# Start serwera
if __name__ == '__main__':
    app.run(debug=True)
