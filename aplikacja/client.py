import requests
from PIL import Image
from io import BytesIO

# Pobierz kod QR z serwera
response = requests.get('http://127.0.0.1:5000/generate_qr')

# Sprawdź czy odpowiedź jest poprawna
if response.status_code == 200:
    # Otwórz obraz QR
    img = Image.open(BytesIO(response.content))
    img.show()  # Wyświetl obraz
else:
    print(f"Failed to retrieve QR code: {response.status_code}")
