from flask import Flask, request, jsonify, send_file
from werkzeug.utils import secure_filename
from datetime import timedelta
import os
import tempfile
import whisper

app = Flask(__name__)

TEMP_DIR = tempfile.gettempdir()

@app.route("/transcribe", methods=["POST"])
def transcribe():
    # Check if the post request has the file part
    if "audio" not in request.files:
        return jsonify({"error": "No audio file found."}), 400
    
    file = request.files["audio"]

    if file.filename == "":
        return jsonify({"error": "No audio file selected."}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "Only WAV, MP3, and OGG audio files are allowed."}), 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(TEMP_DIR, filename)

    try:
        file.save(file_path)

        model = whisper.load_model("small")  # Specify your desired model here
        print("Whisper model loaded.")

        transcription = model.transcribe(audio=file_path)
        segments = transcription.get("segments", [])

        srt_file_path = os.path.join(TEMP_DIR, "subtitles.vtt")
        with open(srt_file_path, "w", encoding="utf-8") as srt_file:
            srt_file.write("WEBVTT\n\n")
            for segment in segments:
                start_time = str(timedelta(seconds=segment["start"])).split(".")[0]
                end_time = str(timedelta(seconds=segment["end"])).split(".")[0]
                text = segment["text"].strip()
                segment_id = segment["id"] + 1
                srt_segment = f"{segment_id}\n{start_time}.000 --> {end_time}.000\n{text}\n\n"
                srt_file.write(srt_segment)

        return send_file(srt_file_path, as_attachment=True, download_name="subtitles.vtt", mimetype="text/vtt")

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ["wav", "mp3", "ogg"]

if __name__ == "__main__":
    app.run()
