from fastapi import FastAPI
from main import validate_events

app = FastAPI()

def occupancy(passengers: int) -> str:
    if 0 <= passengers <= 10:
        return "LOW"
    if 11 <= passengers <= 20:
        return "MEDIUM"
    if 21 <= passengers <= 30:
        return "HIGH"
    return "OVER_CAPACITY"

@app.post("/events")
def receive_event(event: dict):
    result = validate_events(event)
    
    if not result["accepted"]:
        return {
            "accepted": False,
            "errors": result["errors"],
            "occupancy_category": None
        }
    
    raw_event = result["event"]
    passengers_count = raw_event["Passengers"]
    category = occupancy(passengers_count)
    
    formatted_event = {
        "timestamp": raw_event.get("Timestamp"),
        "route": raw_event.get("Route"),
        "bus": raw_event.get("Bus"),
        "passengers": raw_event.get("Passengers"),
        "speed_kmh": raw_event.get("Speed_kmh"),
        "status": raw_event.get("Status")
    }
    
    return {
        "accepted": True,
        "errors": [],
        "occupancy_category": category,
        "event": formatted_event
    }