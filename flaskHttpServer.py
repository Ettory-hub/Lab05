from flask import Flask, request, jsonify, abort

app = Flask(__name__)
subscribers = {}

@app.get("/")
def home():
    return "Hello from Flask PubSub!", 200

@app.get("/list-subscribers")
def list_subscribers():
    return jsonify({"subscribers": subscribers}), 200

@app.post("/add-subscriber")
def add_subscriber():
    data = request.get_json(silent=True) or {}
    name = (data.get("name") or "").strip()
    url = (data.get("url") or data.get("URI") or "").strip()
    if not name or not url:
        abort(400, description="Both 'name' and 'url' are required.")
    if name in subscribers:
        abort(409, description=f"Subscriber '{name}' already exists.")
    subscribers[name] = url
    print(f"[ADD] name={name} url={url}")
    return jsonify({"ok": True, "message": f"Added {name}", "count": len(subscribers)}), 201

@app.delete("/delete-subscriber/<name>")
def delete_subscriber(name=""):
    name = (name or "").strip()
    if name not in subscribers:
        abort(404, description=f"Subscriber '{name}' not found.")
    url = subscribers.pop(name)
    print(f"[DEL] name={name} url={url}")
    return jsonify({"ok": True, "message": f"Deleted {name}", "count": len(subscribers)}), 200

@app.post("/publish")
def publish():
    data = request.get_json(silent=True) or {}
    subject = (data.get("subject") or "").strip()
    payload = data.get("payload")
    if not subject:
        abort(400, description="Field 'subject' is required.")
    notified = []
    for n, u in subscribers.items():
        print(f"[NOTIFY] -> {n} @ {u} | subject='{subject}' payload={payload!r}")
        notified.append({"name": n, "url": u})
    return jsonify({"ok": True, "subject": subject, "notified": notified}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
