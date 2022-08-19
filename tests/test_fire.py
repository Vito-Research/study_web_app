import pathlib
import unittest
import uuid

from firebase_admin import firestore

import fire


def get_certificate_path():
    return pathlib.Path(__file__).parent.parent.joinpath(pathlib.Path("serviceAccount.json")).resolve()


class TestFire(unittest.TestCase):

    def test_upload_heart_rate(self):
        data = {
            "activities-heart": [
                {
                    "dateTime": "2019-05-08",
                    "value": {
                        "customHeartRateZones": [
                            {
                                "caloriesOut": 1164.09312,
                                "max": 90,
                                "min": 30,
                                "minutes": 718,
                                "name": "Below"
                            }
                        ],
                        "heartRateZones": [
                            {
                                "caloriesOut": 979.43616,
                                "max": 86,
                                "min": 30,
                                "minutes": 626,
                                "name": "Out of Range"
                            }
                        ],
                        "restingHeartRate": 76
                    }
                }
            ]
        }

        fire.init(get_certificate_path())
        db = firestore.client()
        doc_ref = db.collection("test").document(str(uuid.uuid4()))
        batch = fire.Batch(db)
        fire.upload_heart_rate(batch, doc_ref, data)
        batch.commit()

        hr_snapshot = next(doc_ref.collection("heartRate").stream())
        hr = hr_snapshot.to_dict()
        self.assertEqual("2019-05-08", hr["dateTime"])
        self.assertEqual(76, hr["restingHeartRate"])

        custom_hr_zones = next(hr_snapshot.reference.collection("customHeartRateZones").stream()).to_dict()
        self.assertEqual(1164.09312, custom_hr_zones["caloriesOut"])
        self.assertEqual(90, custom_hr_zones["max"])
        self.assertEqual(30, custom_hr_zones["min"])
        self.assertEqual(718, custom_hr_zones["minutes"])
        self.assertEqual("Below", custom_hr_zones["name"])

        hr_zones = next(hr_snapshot.reference.collection("heartRateZones").stream()).to_dict()
        self.assertEqual(979.43616, hr_zones["caloriesOut"])
        self.assertEqual(86, hr_zones["max"])
        self.assertEqual(30, hr_zones["min"])
        self.assertEqual(626, hr_zones["minutes"])
        self.assertEqual("Out of Range", hr_zones["name"])

        firestore.client().recursive_delete(doc_ref)

    def test_upload_heart_rate_variability(self):
        data = {
            "hrv": [
                {
                    "value": {
                        "dailyRmssd": 62.887,
                        "deepRmssd": 64.887
                    },
                    "dateTime": "2021-10-25"
                }
            ]
        }

        fire.init(get_certificate_path())
        db = firestore.client()
        doc_ref = db.collection("test").document(str(uuid.uuid4()))
        batch = fire.Batch(db)
        fire.upload_heart_rate_variability(batch, doc_ref, data)
        batch.commit()

        hrv = next(doc_ref.collection("heartRateVariability").stream()).to_dict()
        self.assertEqual("2021-10-25", hrv["dateTime"])
        self.assertEqual(62.887, hrv["dailyRmssd"])
        self.assertEqual(64.887, hrv["deepRmssd"])

        firestore.client().recursive_delete(doc_ref)

    def test_upload_breathing_rate(self):
        data = {
            "br": [
                {
                    "value": {
                        "breathingRate": 17.8
                    },
                    "dateTime": "2021-10-25"
                }
            ]
        }

        fire.init(get_certificate_path())
        db = firestore.client()
        doc_ref = db.collection("test").document(str(uuid.uuid4()))
        batch = fire.Batch(db)
        fire.upload_breathing_rate(batch, doc_ref, data)
        batch.commit()

        br = next(doc_ref.collection("breathingRate").stream()).to_dict()
        self.assertEqual("2021-10-25", br["dateTime"])
        self.assertEqual(17.8, br["breathingRate"])

        firestore.client().recursive_delete(doc_ref)

    def test_upload_oxygen_saturation(self):
        data = [
            {
                "dateTime": "2021-10-01",
                "value": {
                    "avg": 94.7,
                    "min": 94.0,
                    "max": 100.0
                }
            }
        ]

        fire.init(get_certificate_path())
        db = firestore.client()
        doc_ref = db.collection("test").document(str(uuid.uuid4()))
        batch = fire.Batch(db)
        fire.upload_oxygen_saturation(batch, doc_ref, data)
        batch.commit()

        spo2 = next(doc_ref.collection("oxygenSaturation").stream()).to_dict()
        self.assertEqual("2021-10-01", spo2["dateTime"])
        self.assertEqual(94.7, spo2["avg"])
        self.assertEqual(94.0, spo2["min"])
        self.assertEqual(100.0, spo2["max"])

        firestore.client().recursive_delete(doc_ref)


if __name__ == "__main__":
    unittest.main()
