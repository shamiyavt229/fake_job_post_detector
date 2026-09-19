import json

from django.test import TestCase


class PredictJobViewTests(TestCase):
    def test_valid_prediction_request(self):
        payload = {
            "description": "We are looking for a software engineer to join our team and build products for customers using modern technologies and agile practices.",
            "company_email": "jobs@company.com",
        }

        response = self.client.post(
            "/api/predict/",
            data=json.dumps(payload),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("prediction", response.json())
        self.assertIn("warnings", response.json())

    def test_empty_body_returns_400_instead_of_500(self):
        response = self.client.post(
            "/api/predict/",
            data="",
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error"], "Invalid JSON payload.")

    def test_malformed_json_returns_400_instead_of_500(self):
        response = self.client.post(
            "/api/predict/",
            data="{bad json}",
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error"], "Invalid JSON payload.")
