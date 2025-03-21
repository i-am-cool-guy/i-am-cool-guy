FROM python:3.9-slim

WORKDIR /Neo
COPY requirements.txt .
RUN apt-get update && apt-get install -y \
    git \
    libjpeg-turbo-progs \
    libpng-dev \
    zlib1g-dev \
    libfreetype6-dev \
    libharfbuzz-dev \
    libwebp-dev \
    libtiff-dev \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8080

CMD ["python", "main.py"]
