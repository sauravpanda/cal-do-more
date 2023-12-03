from flask import Flask, request
import json
from services.transcribe import transcribe_video, process_transcriptions
from services.whisper import whisper_video
from services.extract_info import get_topics, segregate_tasks
from services.cal import create_booking
from services.git_helper import create_github_issue
import traceback

app = Flask(__name__)


@app.route("/cal/video/transcribe", methods=["POST", "GET"])
def cal_transcribe():
    RESP = "Unknown method"
    if request.method == "POST":
        # print(request.json)
        try:
            bucket_name = request.json["bucket_name"]
            object_key = request.json["object_key"]
            transcription_data = transcribe_video(bucket_name, object_key)
            transcripts = process_transcriptions(transcription_data)
            results = get_topics(transcripts)
            segregate_tasks(results)
            RESP = "Successfully transcribed"
        except Exception as e:
            print(e, traceback.format_exc())
            RESP = "Failed to transcribed"
    return RESP


@app.route("/cal/video/whisper", methods=["POST", "GET"])
def cal_whisper():
    if request.method == "POST":
        # print(request.json)
        bucket_name = request.json["bucket_name"]
        object_key = request.json["object_key"]
        results = whisper_video(bucket_name, object_key)
        return json.dumps(results)


@app.route("/response")
def slack_hook():
    RESP = "Failed to Process"
    data = request.args.get("data")
    eventType = request.args.get("type")
    if data == "yes" and eventType == "issue":
        title = request.args.get("title")
        desc = request.args.get("desc", "")
        create_github_issue(title, desc)
        RESP = "Added Github Issue"
        # print(title, desc)
    elif data == "yes" and eventType == "event":
        summary = request.args.get("summary", "")
        dt = request.args.get("time")
        create_booking(dt, desc=summary)
        RESP = "Added Cal booking"

    return RESP


@app.route("/")
def hello():
    return "Hello, World!"


if __name__ == "__main__":
    app.run(debug=True)
