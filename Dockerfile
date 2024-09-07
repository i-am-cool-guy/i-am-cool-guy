FROM python:3.9-slim

RUN pip install -r requirements.txt
WORKDIR /Neo
COPY ./Neo
EXPOSE 8080

CMD ["python", "main.py"]
