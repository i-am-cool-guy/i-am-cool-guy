FROM python:3.9-slim

WORKDIR /Neo
COPY requirements.txt .
RUN apt-get update && apt-get install git -y
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8080

CMD ["python", "main.py"]
