"""Flight search tool for EasyTrip-Agent."""

from __future__ import annotations

import json
from typing import Optional

from langchain_core.tools import tool


@tool
def search_flights(
    origin: str,
    destination: str,
    departure_date: str,
    return_date: Optional[str] = None,
    passengers: int = 1,
) -> str:
    """Search for flights between two cities.

    Args:
        origin: Departure city or airport code (e.g. "DEL" or "Delhi").
        destination: Arrival city or airport code (e.g. "BOM" or "Mumbai").
        departure_date: Departure date in YYYY-MM-DD format.
        return_date: Optional return date in YYYY-MM-DD format.
        passengers: Number of passengers (default 1).

    Returns:
        A JSON string with mock flight options. Replace this with a real
        flight API integration when ready.
    """
    trip_type = "round_trip" if return_date else "one_way"

    # Placeholder response until a live flight API is wired in.
    results = {
        "origin": origin,
        "destination": destination,
        "departure_date": departure_date,
        "return_date": return_date,
        "passengers": passengers,
        "trip_type": trip_type,
        "flights": [
            {
                "airline": "IndiGo",
                "flight_number": "6E-204",
                "departure_time": "06:15",
                "arrival_time": "08:25",
                "duration": "2h 10m",
                "price_inr": 4500 * passengers,
                "cabin": "Economy",
            },
            {
                "airline": "Air India",
                "flight_number": "AI-865",
                "departure_time": "11:40",
                "arrival_time": "14:05",
                "duration": "2h 25m",
                "price_inr": 6200 * passengers,
                "cabin": "Economy",
            },
            {
                "airline": "Vistara",
                "flight_number": "UK-995",
                "departure_time": "18:30",
                "arrival_time": "20:45",
                "duration": "2h 15m",
                "price_inr": 7800 * passengers,
                "cabin": "Economy",
            },
        ],
        "note": "Mock data. Connect a real flight API for live results.",
    }
    return json.dumps(results, indent=2)
