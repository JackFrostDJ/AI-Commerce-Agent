import requests
import os
import re
from recommender import recommend_text
from image_search import search_by_image
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

HF_API_TOKEN = os.getenv("HF_API_TOKEN")
HF_API_URL = "https://router.huggingface.co/featherless-ai/v1/chat/completions"
HF_API_URL_CLASS = "https://router.huggingface.co/hf-inference/models/facebook/bart-large-mnli"

headers = {
    "Authorization": f"Bearer {HF_API_TOKEN}",
    "Content-Type": "application/json"
}

conversation_history = []
system_prompt = (
    "You are Comma, a friendly AI assistant for a commerce website. "
    "You help users with product searches from images and recommendations. "
    "You always speak in a first person perspective as if speaking directly to user. "
    "If the user asks your name, respond with 'I'm Comma, your AI shopping assistant.' "
    "Do not repeat the user's question or label your responses as 'User' or 'Assistant'. "
    "Respond clearly and professionally in 1 or 2 concise sentences. "
    "Avoid rambling or giving overly detailed answers."
)

conversation_history.append({"role": "system", "content": system_prompt})

@app.route("/hybrid-search", methods=["POST"])
def hybrid_search():
    query = request.form.get("query", "").strip()
    image = request.files.get("image")

    label = "chat"
    if query:
        classification_payload = {
            "inputs": query,
            "parameters": {
                "candidate_labels": ["recommendation", "chat"]
            }
        }

        try:
            classify_res = requests.post(
                HF_API_URL_CLASS, headers=headers,
                json=classification_payload, timeout=15
            )
            classify_res.raise_for_status()
            label_data = classify_res.json()
            label = label_data.get("labels", ["chat"])[0].lower()
        except Exception as e:
            print("Classification failed, defaulting to chat. Error:", e)

    # Force recommendation if image is present even if classification fails
    if "recommendation" in label or image:
        try:
            results = search_by_image(image) if image else recommend_text(query)
        except Exception as e:
            print("Recommendation failed:", e)
            results = []

        if results:
            return jsonify({
                "reply": "Sure! Here are some product recommendations:",
                "results": results
            })
        else:
            return jsonify({
                "reply": "Sorry, I couldn't find anything matching that in our catalog.",
                "results": []
            })

    # Chat fallback
    global conversation_history
    conversation_history.append({"role": "user", "content": query})

    chat_payload = {
        "model": "HuggingFaceH4/zephyr-7b-alpha",
        "messages": conversation_history,
        "temperature": 0.5,
        "max_tokens": 80
    }

    try:
        chat_res = requests.post(HF_API_URL, headers=headers, json=chat_payload, timeout=20)
        chat_res.raise_for_status()
        reply = chat_res.json()["choices"][0]["message"]["content"].strip()

        if not reply.endswith(('.', '!', '?')):
            sentences = re.split(r'(?<=[.!?])\s+', reply)
            reply = ' '.join(s for s in sentences if s.endswith(('.', '!', '?')))
    except Exception as e:
        print("Chat request failed:", e)
        reply = "Something went wrong. Try again later."

    conversation_history.append({"role": "Comma", "content": reply})
    conversation_history = [conversation_history[0]] + conversation_history[-6:]

    return jsonify({
        "reply": reply,
        "results": []
    })

if __name__ == "__main__":
    app.run(debug=True)