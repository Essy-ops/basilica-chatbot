import json
import firebase_admin
from firebase_admin import credentials, firestore

# Load your admin credentials
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Load your answers
with open("answers.json", "r") as f:
    answers = json.load(f)

# Upload each intent as a document in the "answers" collection
for intent_id, text in answers.items():
    db.collection("answers").document(intent_id).set({"text": text})
    print(f"Uploaded: {intent_id}")

print(f"\nDone! {len(answers)} documents uploaded to Firestore.")