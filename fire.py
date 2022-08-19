import uuid

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


class Batch:
    MAX_OPERATIONS = 500

    def __init__(self, firestore_client):
        self.firestore_client = firestore_client
        self.batch = firestore_client.batch()
        self.batches = [self.batch]
        self.operation_count = 0

    def create(self, reference, data):
        self.batch.create(reference, data)
        self.__incr_operation_count()

    def set(self, reference, data):
        self.batch.set(reference, data)
        self.__incr_operation_count()

    def update(self, reference, field_updates):
        self.batch.update(reference, field_updates)
        self.__incr_operation_count()

    def delete(self, reference):
        self.batch.delete(reference)
        self.__incr_operation_count()

    def commit(self):
        for batch in self.batches:
            batch.commit()
        self.batches.clear()
        self.__new_batch()

    def __incr_operation_count(self):
        self.operation_count += 1
        if self.operation_count >= self.MAX_OPERATIONS:
            self.__new_batch()

    def __new_batch(self):
        self.batch = self.firestore_client.batch()
        self.batches.append(self.batch)
        self.operation_count = 0


def init(certificate_path):
    if not firebase_admin._apps:
        cred = credentials.Certificate(certificate_path)
        firebase_admin.initialize_app(cred)


def upload_fitbit_data(fitbit_data):
    db = firestore.client()
    doc_ref = db.collection("data").document(str(uuid.uuid4()))
    batch = Batch(db)

    upload_heart_rate(batch, doc_ref, fitbit_data.heart_rate)
    upload_heart_rate_variability(batch, doc_ref, fitbit_data.heart_rate_variability)
    upload_breathing_rate(batch, doc_ref, fitbit_data.breathing_rate)
    upload_oxygen_saturation(batch, doc_ref, fitbit_data.oxygen_saturation)

    batch.commit()


def upload_heart_rate(batch, doc_ref, data):
    for hr in data[next(iter(data))]:
        hr_ref = doc_ref.collection("heartRate").document()
        hr_fields = {"dateTime": hr["dateTime"]}
        if "restingHeartRate" in hr["value"]:
            hr_fields["restingHeartRate"] = hr["value"]["restingHeartRate"]
        batch.set(hr_ref, hr_fields)

        for custom_hr_zone in hr["value"]["customHeartRateZones"]:
            custom_hr_zone_ref = hr_ref.collection("customHeartRateZones").document()
            batch.set(custom_hr_zone_ref, custom_hr_zone)
        for hr_zone in hr["value"]["heartRateZones"]:
            hr_zone_ref = hr_ref.collection("heartRateZones").document()
            batch.set(hr_zone_ref, hr_zone)


def upload_heart_rate_variability(batch, doc_ref, data):
    for hrv in data[next(iter(data))]:
        hrv_ref = doc_ref.collection("heartRateVariability").document()
        batch.set(hrv_ref, {
            "dateTime": hrv["dateTime"],
            "dailyRmssd": hrv["value"]["dailyRmssd"],
            "deepRmssd": hrv["value"]["deepRmssd"]
        })


def upload_breathing_rate(batch, doc_ref, data):
    for br in data[next(iter(data))]:
        br_ref = doc_ref.collection("breathingRate").document()
        batch.set(br_ref, {
            "dateTime": br["dateTime"],
            "breathingRate": br["value"]["breathingRate"]
        })


def upload_oxygen_saturation(batch, doc_ref, data):
    for spo2 in data:
        spo2_ref = doc_ref.collection("oxygenSaturation").document()
        batch.set(spo2_ref, {
            "dateTime": spo2["dateTime"],
            "avg": spo2["value"]["avg"],
            "min": spo2["value"]["min"],
            "max": spo2["value"]["max"]
        })
