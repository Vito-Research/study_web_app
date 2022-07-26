import requests

class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token
    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r

def hr(start, end, access_token, user_id):
    
    return requests.get("https://api.fitbit.com/1/user/" + str(user_id) + "/activities/heart/date/" + str(start) + "/"+ str(end) + ".json", auth=BearerAuth(access_token)).json()

def o2(start, end, access_token):
    
    requests.get("https://api.fitbit.com/1/user/"  + str(user_id) + "/spo2/date/" + str(start) + str(end) + ".json", auth=BearerAuth(access_token))

def rr(start, end, access_token):
    
    requests.get("https://api.fitbit.com/1/user/"  + str(user_id) + "/br/date/" + str(start) + str(end) + ".json", auth=BearerAuth(access_token))

def hrv(start, end, access_token):
    
    requests.get("https://api.fitbit.com/1/user/"  + str(user_id) + "/hrv/date/" + str(start) + str(end) + ".json", auth=BearerAuth(access_token))