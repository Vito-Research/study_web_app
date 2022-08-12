import uuid

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


def init(certificate_path):
    if not firebase_admin._apps:
        cred = credentials.Certificate(certificate_path)
        firebase_admin.initialize_app(cred)


def upload_fitbit_data(fitbit_data):
    doc_ref = firestore.client().collection("data").document(str(uuid.uuid4()))

    upload_heart_rate(doc_ref, fitbit_data.heart_rate)
    upload_heart_rate_variability(doc_ref, fitbit_data.heart_rate_variability)
    upload_breathing_rate(doc_ref, fitbit_data.breathing_rate)
    upload_oxygen_saturation(doc_ref, fitbit_data.oxygen_saturation)


def upload_heart_rate(doc_ref, data):
    for hr in data[next(iter(data))]:
        hr_ref = doc_ref.collection("heartRate").document(str(uuid.uuid4()))
        hr_fields = {"dateTime": hr["dateTime"]}
        if "restingHeartRate" in hr["value"]:
            hr_fields["restingHeartRate"] = hr["value"]["restingHeartRate"]
        hr_ref.set(hr_fields)

        for custom_hr_zone in hr["value"]["customHeartRateZones"]:
            hr_ref.collection("customHeartRateZones").add(custom_hr_zone)
        for hr_zone in hr["value"]["heartRateZones"]:
            hr_ref.collection("heartRateZones").add(hr_zone)


def upload_heart_rate_variability(doc_ref, data):
    for hrv in data[next(iter(data))]:
        doc_ref.collection("heartRateVariability").add({
            "dateTime": hrv["dateTime"],
            "dailyRmssd": hrv["value"]["dailyRmssd"],
            "deepRmssd": hrv["value"]["deepRmssd"]
        })


def upload_breathing_rate(doc_ref, data):
    for br in data[next(iter(data))]:
        doc_ref.collection("breathingRate").add({
            "dateTime": br["dateTime"],
            "breathingRate": br["value"]["breathingRate"]
        })


def upload_oxygen_saturation(doc_ref, data):
    for spo2 in data:
        doc_ref.collection("oxygenSaturation").add({
            "dateTime": spo2["dateTime"],
            "avg": spo2["value"]["avg"],
            "min": spo2["value"]["min"],
            "max": spo2["value"]["max"]
        })
