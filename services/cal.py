import requests
import os
import json

BASE_URL = "https://api.cal.com/v1/"


def make_cal_call(url, payload, method="GET"):
    url += f'?apiKey={os.environ.get("CAL_API_KEY")}'
    if method == "GET":
        resp = requests.get(url, params=payload)
    else:
        resp = requests.post(url, json=payload)

    return json.loads(resp.text)


def get_event_types():
    url = BASE_URL + "event-types"
    resp = make_cal_call(url, {})
    events = []
    for event in resp["event_types"]:
        events.append(
            {
                "id": event["id"],
                "title": event["title"],
                "length": event["length"],
            }
        )
    return events


def get_availablity(username, eventId, dateFrom, dateTo):
    url = BASE_URL + "availability"
    resp = make_cal_call(
        url,
        {
            "username": username,
            "eventTypeId": eventId,
            "dateFrom": dateFrom,
            "dateTo": dateTo,
        },
        method="GET",
    )
    return resp


def create_booking(eventId, start, timeZone, attendees, metadata={}, language="en"):
    url = BASE_URL + "bookings"
    resp = make_cal_call(
        url,
        {
            "start": start,
            "eventTypeId": eventId,
            "timeZone": timeZone,
            "responses": attendees,
            "metadata": metadata,
            "language": language,
        },
        method="POST",
    )
    return resp


if __name__ == "__main__":
    # print(get_event_types())
    # print(
    #     "Get Availiabilty: ",
    #     get_availablity("pandasaurav", 517882, "2023-12-05 12:00:00", "2023-12-08 13:00:00")
    # )
    print(
        create_booking(
            517882,
            "2023-12-05T15:00:00.000Z",
            "America/New_York",
            {"name": "Saurav", "email": "sgp65@cornell.edu", "location": "Office"},
        )
    )
