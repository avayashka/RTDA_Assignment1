dataset = [
    {
        "Timestamp": "08:00",
        "Route": "AITU-Campus–Residence",
        "Bus": "B01",
        "Passengers": "18",
        "Speed_kmh": "31",
        "Status": "ON_ROUTE",
    },
    {
        "Timestamp": "08:01",
        "Route": "AITU-Campus–Residence",
        "Bus": "B02",
        "Passengers": "22",
        "Speed_kmh": "28",
        "Status": "ON_ROUTE",
    },
    {
        "Timestamp": "08:02",
        "Route": "AITU-Campus–Residence",
        "Bus": "B01",
        "Passengers": "21",
        "Speed_kmh": "29",
        "Status": "ON_ROUTE",
    },
    {
        "Timestamp": "08:03",
        "Route": "AITU-Campus–Residence",
        "Bus": "B02",
        "Passengers": "25",
        "Speed_kmh": "27",
        "Status": "ON_ROUTE",
    },
    {
        "Timestamp": "08:04",
        "Route": "AITU-Campus–Residence",
        "Bus": "B01",
        "Passengers": "24",
        "Speed_kmh": "0",
        "Status": "STOPPED",
    },
    {
        "Timestamp": "08:05",
        "Route": "AITU-Campus–Residence",
        "Bus": "B02",
        "Passengers": "26",
        "Speed_kmh": "30",
        "Status": "ON_ROUTE",
    },
    {
        "Timestamp": "08:06",
        "Route": "AITU-Campus–Residence",
        "Bus": "B01",
        "Passengers": "23",
        "Speed_kmh": "32",
        "Status": "ON_ROUTE",
    },
    {
        "Timestamp": "08:07",
        "Route": "AITU-Campus–Residence",
        "Bus": "B02",
        "Passengers": "28",
        "Speed_kmh": "26",
        "Status": "ON_ROUTE",
    },
    {
        "Timestamp": "08:08",
        "Route": "AITU-Campus–Residence",
        "Bus": "B01",
        "Passengers": "27",
        "Speed_kmh": "25",
        "Status": "ON_ROUTE",
    },
    {
        "Timestamp": "08:09",
        "Route": "AITU-Campus–Residence",
        "Bus": "B02",
        "Passengers": "30",
        "Speed_kmh": "24",
        "Status": "ON_ROUTE",
    },
]

from datetime import datetime

def validate_events(event):
    errors = []
    try:
        timestamp = datetime.strptime(event["Timestamp"], "%H:%M")
        formatted_timestamp = timestamp.strftime("%H:%M")
    except (KeyError, TypeError, ValueError):
        formatted_timestamp = None
        errors.append("Invalid timestamp format")
        
    try:
        passengers = int(event.get("Passengers"))
        if passengers < 0:
            errors.append("Passengers count must be a non-negative integer")
    except (ValueError, TypeError):
        passengers = None
        errors.append("Invalid Passengers value")

    try:
        speed = float(event.get("Speed_kmh"))
        if not (0 <= speed <= 120):
            errors.append("Speed of a bus is out of bounds")
    except (ValueError, TypeError):
        speed = None
        errors.append("Invalid Speed value")

    status = str(event.get("Status")).upper()
    if status not in ["ON_ROUTE", "STOPPED"]:
        errors.append("Invalid Status")

    if errors:
        return {"accepted": False, "errors": errors}

    return {
        "accepted": True,
        "event": {
            **event, 
            "Timestamp": formatted_timestamp,
            "Passengers": passengers,
            "Speed_kmh": speed,
            "Status": status
        },
        "errors": [],
    }

def events_stream(events_list):
    for event in events_list:
        validation = validate_events(event)
        if validation["accepted"]:
            yield event    

def events_chronology(stream):
    last = None
    for event in stream:
        current = event.get("Timestamp")
        if last is not None:
            if current < last:
                print("Chronology Error")
        last = current
        print(event)

import json
if __name__ == "__main__":
    stream = events_stream(dataset)
    events_chronology(stream)

    with open("events.json", "w") as file:
        json.dump(dataset, file)

    passengers = [int(event["Passengers"]) for event in dataset]
    avg_passengers = sum(passengers) / len(passengers)
    max_passengers = max(passengers)
    stopped = sum(event["Status"] == "STOPPED" for event in dataset)
    busiest_event = max(dataset, key=lambda event: int(event["Passengers"]))
    busiest_minute = busiest_event["Timestamp"]
    busiest_bus = busiest_event["Bus"]

    print("The average passengers count = ", avg_passengers)
    print("The maximum passengers count = ", max_passengers)
    print("The number of stopped events = ", stopped)
    print(f"The busiest event was {busiest_bus} Bus at {busiest_minute}")