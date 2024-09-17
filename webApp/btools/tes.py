from cryptography.fernet import Fernet
from django.conf import settings

# Dapatkan kunci dari settings.py
key = settings.ENCRYPTION_KEY.encode()  # Mengubah menjadi bytes jika diperlukan

# Buat objek Fernet
cipher_suite = Fernet(key)

# Data yang ingin didekripsi
encrypted_data = b'gAAAAABm6QYgCweada4xBbqTIzqQUAOdG0U3cHgEofV6z77i879h85K8XLY_pvLu5ruBEYJJWcz-mr5ll5PotuiO4PV49y-XiQ=='

# Dekripsi data
try:
    decrypted_data = cipher_suite.decrypt(encrypted_data)
    print("Decrypted data:", decrypted_data.decode())
except Exception as e:
    print("Decryption failed:", e)