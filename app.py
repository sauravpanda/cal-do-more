from flask import Flask, request
import json
from services.transcribe import transcribe_video, process_transcriptions
app = Flask(__name__)


@app.route('/cal/video/transcribe', methods = ['POST', 'GET'])
def cal_transcribe():
    if request.method == 'POST':
        print(request.json)
        bucket_name = request.json['bucket_name']
        object_key = request.json['object_key']
        transcription_data = transcribe_video(bucket_name, object_key)
        results = process_transcriptions(transcription_data)
        return json.dumps(results)


@app.route('/response')
def slack_hook():
    data = request.args.get('data')
    return f'Button clicked! Value: {data}'


@app.route('/')
def hello():
    return 'Hello, World!'


if __name__ == '__main__':
    app.run(debug=True)