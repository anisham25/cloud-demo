import os, socket, time
from flask import Flask, jsonify

app = Flask(__name__, static_folder="public", static_url_path="")
STARTED = time.time()  # when this copy of the app started
hits = 0  # kept in this copy's memory only

@app.get("/")
def home():
    return app.send_static_file("index.html")

@app.get("/api/where")
def where():
    global hits
    hits += 1
    return jsonify(
        running_on="Vercel" if os.environ.get("VERCEL") else "my laptop",
        region=os.environ.get("VERCEL_REGION", "local"),
        machine=socket.gethostname(),
        copy_age_seconds=round(time.time() - STARTED),
        hits_on_this_copy=hits,
    )
