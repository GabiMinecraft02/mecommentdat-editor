from flask import Flask, render_template, request, send_file, send_from_directory
import io
import os

app = Flask(__name__)

# chemin vers le fichier vide
EMPTY_FILE = os.path.join("tools", "files", "mecomment.dat")

@app.route("/", methods=["GET", "POST"])
def index():
    content = ""

    # ouvrir un fichier uploadé
    if request.method == "POST" and "file" in request.files:
        file = request.files["file"]
        if file.filename != "":
            content = file.read().decode("utf-8", errors="ignore")

    return render_template("index.html", content=content)

@app.route("/robots.txt")
def robots():
    return send_from_directory("google_search_console", "robots.txt")

@app.route("/sitemap.xml")
def sitemap():
    return send_from_directory("google_search_console", "sitemap.xml")

@app.route("/download", methods=["POST"])
def download():
    text = request.form.get("editor", "")

    buffer = io.BytesIO()
    buffer.write(text.encode("utf-8"))
    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name="mecomment.dat",
        mimetype="text/plain"
    )

@app.route("/empty")
def empty():
    return send_file(
        EMPTY_FILE,
        as_attachment=True,
        download_name="mecomment.dat"
    )

if __name__ == "__main__":
    app.run(debug=True)
    app.run(host="0.0.0.0", port=5000, debug=True)
