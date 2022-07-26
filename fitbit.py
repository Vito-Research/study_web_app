from datetime import timedelta
import streamlit as st
import pandas as pd
import requests
from pandas import json_normalize
import base64
URL = "https://api.fitbit.com/1/user/~/{data}/date/{start}/{end}.json"


class FitbitData:

    def __init__(self, heart_rate=None, heart_rate_variability=None, breathing_rate=None, oxygen_saturation=None):
        self.heart_rate = heart_rate
        self.heart_rate_variability = heart_rate_variability
        self.breathing_rate = breathing_rate
        self.oxygen_saturation = oxygen_saturation

    def is_empty(self):
        try:
            return (not self.heart_rate and not self.heart_rate_variability and
                not self.breathing_rate and not self.oxygen_saturation)
        except:
            return False

class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r

class TokenAuth(requests.auth.AuthBase):
    def __init__(self, token: str):
        self.token = token

    def __call__(self, r):
        r.headers["authorization"] = "Basic " +  str(self.token)
        return r
def get(access_token, data, start, end, days_per_request=0):
    warning = False
    if not warning:
        if days_per_request > 0:
            dates = [d.strftime("%Y-%m-%d") for d in pd.date_range(start=start, end=end, freq=f"{days_per_request}D")]
        
            if dates[len(dates) - 1] != end:
                dates.append((pd.to_datetime(end) + timedelta(days=1)).strftime("%Y-%m-%d"))
            if len(dates) > 1:
                response = {}

                for i in range(0, len(dates) - 1):
                    start_date = dates[i]
                    end_date = (pd.to_datetime(dates[i + 1]) - timedelta(days=1)).strftime("%Y-%m-%d")
                    current_response = requests.get(
                        URL.format(data=data, start=start_date, end=end_date),
                        auth=BearerAuth(access_token)
                    ).json()
                    if "Too Many Requests" in current_response:
                        warning = True
                        st.warning("Too many requests")
                        break
                    if not response:
                        response = current_response
                    else:
                        key = next(iter(response))
                        try:
                            response[key].extend(current_response[key])
                        except:
                            st.warning("response error")
                    
                        break
                return response
    return pd.DataFrame.from_dict(requests.get(
        URL.format(data=data, start=start, end=end),
        auth=BearerAuth(access_token)
    ).json())


def get_heart_rate(access_token, start, end):
    return get(access_token, "activities/heart", start, end)


def get_oxygen_saturation(access_token, start, end):
    return get(access_token, "spo2", start, end)


def get_breathing_rate(access_token, start, end):
    return get(access_token, "br", start, end, days_per_request=30)


def get_heart_rate_variability(access_token, start, end):
    return get(access_token, "hrv", start, end, days_per_request=30)
