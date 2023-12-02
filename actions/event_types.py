import requests

class EventTypes:
    def __init__(self, url, resource_name, api_key):
        self.query_params = {"api_key": api_key}
        self.url = url + "/" + resource_name

    def create_event_type(self, meeting_title, meeting_length):
        payload = {
            "title": meeting_title,
            "slug": meeting_title + "-{{$guid}}",
            "length": meeting_length,
            "metadata": {},
        }

        response = requests.post(self.url, params=self.query_params, data=payload)
        return response

    def find_event_type(self, event_id):
        api_url = self.url + "/" + event_id
        response = requests.get(api_url, params=self.query_params)
        return response

  