import json
import os
import urllib3
import json

def lambda_handler(event, context):
    print(json.dumps(event['Records']))
    flask_url = os.environ["FLASK_URL"]

    api_url = flask_url + "/cal/video/transcribe"
    http = urllib3.PoolManager()


    file_name = event['Records'][0]['s3']['object']['key']
    bucket_name = event['Records'][0]['s3']['bucket']['name']
  
    payload = {
        'object_key': file_name,
        'bucket_name': bucket_name
    }
    encoded_data = json.dumps(payload).encode('utf-8')

    
    response = http.request("POST", api_url, body=encoded_data, headers={'Content-Type': 'application/json'})
    data = json.loads(response.data.decode('utf-8'))['json']

    print(data)

    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }