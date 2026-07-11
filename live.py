import os
import requests
from flask import Flask, request, render_template_string
from dotenv import load_dotenv

load_dotenv()
TAVUS_API_KEY = os.getenv("TAVUS_API_KEY")

PERSONA_ID = "<PERSONA_ID>"
REPLICA_ID = "<REPLICA_ID>"

HEADERS = {"x-api-key": TAVUS_API_KEY, "Content-Type": "application/json"}
API = "https://tavusapi.com/v2"

HTML = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Live AI Tutor</title>
  <style>
    body { font-family: system-ui; margin: 2rem; max-width: 780px; }
    textarea { width: 100%; height: 120px; padding: .7rem; border-radius: .6rem; border: 1px solid #ccc; }
    button { padding: .7rem 1rem; margin-top: .5rem; border-radius: .6rem; border: 1px solid #ccc; cursor: pointer; }
    iframe { width: 100%; height: 700px; border: none; border-radius: .8rem; margin-top: 1rem; }
    .note { color: #555; }
  </style>
</head>
<body>
  <h1>Live AI Tutor (embedded)</h1>
  
  <form method="post">
    <label for="context">Conversation context (what should the tutor know?)</label>
    <textarea id="context" name="context" placeholder="e.g., We’re covering quadratic equations; keep answers short and ask check-in questions."></textarea>
    <button type="submit">Start Live Call</button>
  </form>

  {% if conversation_url %}
    <p class="note">Share this link too: <a href="{{ conversation_url }}" target="_blank">{{ conversation_url }}</a></p>
    
    <iframe allow="camera; microphone; autoplay; clipboard-read; clipboard-write"
            src="{{ conversation_url }}"></iframe>
  {% endif %}
</body>
</html>
"""

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    conversation_url = None
    
    if request.method == "POST":
        # Form inputs se tutor ka custom
        ctx = request.form.get("context", "").strip()
        
        # Tavus /conversations endpoint ke liye payload (request body) banana
        body = {
            "persona_id": PERSONA_ID,
            "replica_id": REPLICA_ID
        }
        
        # Agar context empty nahi hai, toh hi request body mein inject karein
        if ctx:
            body["conversational_context"] = ctx

        # Tavus API ko POST request bhejna live streaming session create karne ke liye
        r = requests.post(f"{API}/conversations", headers=HEADERS, json=body, timeout=60)
        
        # HTTP errors check karna (e.g., Status 401, 500 aane par code exception generate karega)
        r.raise_for_status()
        
        # API response se uniquely generated conversational streaming WebRTC link nikalna
        conversation_url = r.json().get("conversation_url")

    # Pure dynamic layout aur variable state ko end-user ke browser par render karna
    return render_template_string(HTML, conversation_url=conversation_url)

# 5. Application entry point: Server ko run karna (Localhost:5002 par run karega)
if __name__ == "__main__":
    app.run(debug=True, port=5002)
