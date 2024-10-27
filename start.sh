set -eu

export PYTHONUNBUFFERED=true

# Pastikan pip terinstal
pip3 install --upgrade pip

# Menginstal dependensi langsung tanpa virtual environment
pip3 install -r requirements.txt

# Menjalankan aplikasi
python3 app.py