import requests

class Bookings:
    def __init__(self, url, resource_name, api_key):
        self.query_params={"api_key": api_key}
        self.url = url + "/" + resource_name

    def get_all_bookings(self):
        response = requests.get(self.url, params = self.query_params)
        return response
    
    def create_booking(self, eventTypeId, startTime, responses, timeZone, language):
        payload = {
            "eventTypeId": eventTypeId,
            "start": startTime,
            "responses": responses,
            "metadata": {},
            "timeZone": timeZone,
            "language": language
        }

        response = requests.post(self.url, params=self.query_params, data=payload)
        return response
    
    def find_booking(self, id):
        api_url = self.url + "/" + id
        response = requests.get(api_url, params=self.query_params)
        return response
    