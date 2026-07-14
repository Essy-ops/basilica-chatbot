"""
BASILICA — Chatbot API
Milestone 5: Cloud Deployment & Integration (local version first, Cloud Run next)
"""

import re
import joblib
import firebase_admin
from firebase_admin import credentials, firestore
from flask import Flask, request, jsonify
from flask_cors import CORS

CONFIDENCE_THRESHOLD = 0.40
FALLBACK_MESSAGE = (
    "I'm not fully sure about that one. Please contact the parish office directly "
    "and they'll be happy to help you."
)

app = Flask(__name__)
CORS(app)

model = joblib.load("intent_classifier_v1.joblib")
vectorizer = joblib.load("tfidf_vectorizer_v1.joblib")

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()


def clean_text(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^\w\s?']", "", text)
    text = re.sub(r"\s+", " ", text)
    return text


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json(silent=True) or {}
    question = data.get("question", "").strip()

    if not question:
        return jsonify({"error": "Missing 'question' field"}), 400

    cleaned = clean_text(question)
    X = vectorizer.transform([cleaned])
    probs = model.predict_proba(X)[0]
    top_idx = probs.argmax()
    predicted_intent = model.classes_[top_idx]
    confidence = float(probs[top_idx])

    if confidence < CONFIDENCE_THRESHOLD:
        return jsonify({
            "question": question,
            "intent": None,
            "confidence": round(confidence, 3),
            "answer": FALLBACK_MESSAGE,
        })

    doc = db.collection("answers").document(predicted_intent).get()
    if doc.exists:
        answer_text = doc.to_dict().get("text", FALLBACK_MESSAGE)
    else:
        answer_text = FALLBACK_MESSAGE

    return jsonify({
        "question": question,
        "intent": predicted_intent,
        "confidence": round(confidence, 3),
        "answer": answer_text,
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081, debug=True)
