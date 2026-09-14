import pytest
from main import validate_events
from api import occupancy

def test_validate_events():
    sample = {"Timestamp": "08:10", 
              "Route": "AITU-Campus–Residence", 
              "Bus": "B01", 
              "Passengers": "20", 
              "Speed_kmh": "31", 
              "Status": "ON_ROUTE"}
    result = validate_events(sample)
    assert result["accepted"] is True
    assert result["event"]["Passengers"] == 20
    assert result["event"]["Speed_kmh"] == 31.0

def test_negative_passengers():
    sample = {"Timestamp": "08:11", 
              "Route": "AITU-Campus–Residence", 
              "Bus": "B02", 
              "Passengers": "-3", 
              "Speed_kmh": "30", 
              "Status": "ON_ROUTE"}
    result = validate_events(sample)
    assert result["accepted"] is False
    assert "Passengers count must be a non-negative integer" in result["errors"]

def test_speed_boundaries():
    sample = {"Timestamp": "08:12", 
              "Route": "AITU-Campus–Residence", 
              "Bus": "B01", 
              "Passengers": "10", 
              "Speed_kmh": "138", 
              "Status": "ON_ROUTE"}
    result = validate_events(sample)
    assert result["accepted"] is False
    assert "Speed of a bus is out of bounds" in result["errors"]

def test_occupancy_category():
    assert occupancy(7) == "LOW"
    assert occupancy(14) == "MEDIUM"
    assert occupancy(21) == "HIGH"
    assert occupancy(42) == "OVER_CAPACITY"

def test_invalid_route():
    sample = {
        "Timestamp": "08:13",
        "Route": "EXPO-Direct",  
        "Bus": "B01",
        "Passengers": "15",
        "Speed_kmh": "25",
        "Status": "ON_ROUTE"
    }
    result = validate_events(sample)
    assert result["accepted"] is False
    assert "Invalid route specified" in result["errors"]
