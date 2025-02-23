# Dockerfile
FROM python:3.10-slim-buster

# 1. Instalează Tesseract și alte pachete de sistem necesare
RUN apt-get update && apt-get install -y --no-install-recommends \
    tesseract-ocr \
    libtesseract-dev \
    && rm -rf /var/lib/apt/lists/*

# 2. Setăm un director de lucru în container
WORKDIR /app

# 3. Copiem fișierele proiectului în container
COPY . /app

# 4. Instalăm pachetele Python
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# 5. Setăm variabila de mediu pentru Gunicorn (portul pe care va rula)
ENV PORT=8000

# 6. Comanda de start a aplicației (Gunicorn)
# 'FoodScannerAPI.wsgi:application'
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

CMD ["/app/entrypoint.sh"]
