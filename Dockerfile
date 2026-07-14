FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY intent_classifier_v1.joblib .
COPY tfidf_vectorizer_v1.joblib .

EXPOSE 8081

CMD gunicorn --bind 0.0.0.0:${PORT:-8081} --workers 1 --threads 4 app:app
