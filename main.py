import streamlit as st

from fitbit import get_breathing_rate
from fitbit import get_heart_rate
from fitbit import get_heart_rate_variability
from fitbit import get_oxygen_saturation

st.image("Vito.png")
st.header("Vito Study")
st.subheader("A study aiming to detect infection in real time using smartwatch data")

link = '[More Information](https://vitovitals.org)'
st.markdown(link, unsafe_allow_html=True)
st.image("Promo.png")
st.write("""
This form is designed to describe the study’s goals, the overall nature of the study, the risks involved, 
and the time commitment necessary. This study is designed to measure the risk of COVID-19 using physiological data 
commonly found on smartwatches. 

You are being asked to participate in this study because you are a student at the University of North Florida who has 
a smartwatch, are willing to download the app used to conduct the study, and are willing to report a COVID-19 diagnosis 
and/or log symptoms upon notification from the app. Please keep in mind that this is voluntary, meaning you may only 
participate if you desire to. Participating in this study requires ten minutes of setup time and roughly five 
minutes per month of symptom logging. Benefits of this study include reducing future spread of viral infections via 
real-time alerting of infection, encouraging further testing of infectious diseases, and conducting a more in-depth 
analysis of one’s health via a medical professional’s supervision. 

There are no known risks to participating in this study. The data used in this study are collected anonymously, 
and neither the researchers nor anyone else will know the origin of the data other than the fact that they came from an 
authorized participant via the app, thus the data are not linked to participants.
""")

st.subheader("1. Press the \"Authorize with Fitbit\"")
st.subheader("2. Enter login information")
st.subheader("3. Once redirected to Vito's website, copy the url")
st.subheader("4. Paste the url into the textbox below")

link = "https://www.fitbit.com/oauth2/authorize?response_type=token&client_id=2389P9&redirect_uri=https%3A%2F%2Fvitovitals.org&scope=heartrate%20sleep%20oxygen_saturation%20respiratory_rate%20temperature&expires_in=604800"
st.markdown(f'[Authorize with Fitbit]({link})', unsafe_allow_html=True)
st.caption(link)

fitbitResponse = st.text_input("Enter Response From Fitbit Authorization")

if fitbitResponse != "":
    parsed = fitbitResponse.split("#access_token=")[1]

    token = parsed.split("&user_id")[0]
    st.write(token)
    user_id = parsed.split("&user_id=")[1].split("&")[0]
    st.write(user_id)

    st.write(get_heart_rate(token, user_id, "2020-01-01", "2022-01-08"))
    st.write(get_breathing_rate(token, user_id, "2020-01-01", "2022-01-08"))
    st.write(get_heart_rate_variability(token, user_id, "2020-01-01", "2022-01-08"))
    st.write(get_oxygen_saturation(token, user_id, "2020-01-01", "2022-01-08"))
