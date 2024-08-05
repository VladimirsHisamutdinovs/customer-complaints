# Dockerfile for TimesFM service
FROM python:3.10.12-bullseye

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "timesfm_script.py"]
