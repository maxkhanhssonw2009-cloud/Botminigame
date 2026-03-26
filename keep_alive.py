# keep_alive.py
# Simple Flask webserver to keep the bot alive on hosting services that require a web app.
from flask import Flask
from threading import Thread

app = Flask("keep_alive")

@app.route("/")
def home():
    return "Nhanh Như Chớp bot is alive."

def run():
    app.run(host="0.0.0.0", port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

if __name__ == "__main__":
    keep_alive()