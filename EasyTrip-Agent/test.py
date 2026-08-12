"""Smoke tests for EasyTrip-Agent tools and health endpoint."""

from __future__ import annotations

import json
import unittest
from unittest.mock import patch

from app import app
from tools.flight_tool import search_flights


class FlightToolTests(unittest.TestCase):
    def test_search_flights_returns_json(self):
        raw = search_flights.invoke(
            {
                "origin": "DEL",
                "destination": "BOM",
                "departure_date": "2026-09-01",
                "passengers": 2,
            }
        )
        data = json.loads(raw)
        self.assertEqual(data["origin"], "DEL")
        self.assertEqual(data["destination"], "BOM")
        self.assertEqual(data["passengers"], 2)
        self.assertGreaterEqual(len(data["flights"]), 1)


class AppTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_health(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["status"], "ok")

    def test_index(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"EasyTrip", response.data)

    def test_chat_requires_message(self):
        response = self.client.post("/chat", json={})
        self.assertEqual(response.status_code, 400)

    @patch("app.run_agent", return_value="Here are some flight options.")
    def test_chat_success(self, _mock_run):
        response = self.client.post(
            "/chat",
            json={"message": "Find flights from Delhi to Mumbai"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("reply", response.get_json())


if __name__ == "__main__":
    unittest.main()
