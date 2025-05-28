from flask import Flask, render_template, request, send_file
import yt_dlp
import os
import uuid

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/download", methods=["POST"])
def download():
    url = request.form.get("url")
    video_id = str(uuid.uuid4())
    output_path = f"downloads/{video_id}.%(ext)s"

    ydl_opts = {
        'outtmpl': output_path,
        'format': 'mp4/bestaudio/best',
        'quiet': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
        return send_file(filename, as_attachment=True)
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    os.makedirs("downloads", exist_ok=True)
    app.run(host="0.0.0.0", port=5000)
