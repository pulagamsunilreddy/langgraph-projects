"""Flask web app for EasyTrip-Agent."""

from __future__ import annotations

from flask import Flask, jsonify, render_template, request

from backend import run_agent

app = Flask(__name__)


@app.get("/")
def index():
    return render_template("index.html")


@app.post("/chat")
def chat():
    payload = request.get_json(silent=True) or {}
    message = (payload.get("message") or "").strip()
    history = payload.get("history") or []

    if not message:
        return jsonify({"error": "Message is required."}), 400

    try:
        reply = run_agent(message, history=history)
        return jsonify({"reply": reply})
    except Exception as exc:  # noqa: BLE001
        return jsonify({"error": str(exc)}), 500


@app.get("/health")
def health():
    return jsonify({"status": "ok", "service": "EasyTrip-Agent"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
