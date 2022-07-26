import streamlit as st 
import streamlit.components.v1 as components
from fitbit import heartrate
st.image("Vito.png")

st.header("Vito Study")

st.subheader("A study aiming to detect infection in realtime using smartwatch data")

link = '[More Information](https://vitovitals.org)'
st.markdown(link, unsafe_allow_html=True)
st.image("Promo.png")
st.write("""

This form is designed to describe the study’s goals, the overall nature of the study, risks involved, and the amount of time commitment necessary. 
This study is designed to measure the risk of Covid-19 using physiological data commonly found on smartwatches.   

You are being asked to participate in this study because you are a student at the University of North Florida who has a smartwatch, are willing to download the app used to conduct the study and are willing to report COVID-19 diagnosis and or log symptoms upon notification from the app, please keep in mind this is voluntary, meaning you may only participate if you desire to. 
Participating in this study requires ten minutes of set up time, and roughly five minutes per month of symptom logging. 
Benefits of this study include reducing future spread of viral infections via real time alerting of infection, encouraging further testing of infectious diseases, and making more in-depth analysis of one’s health via a medical professional’s supervision.   

There are no known risks to participating in this study. 
The data collected in this study is collected anonymously, the researchers nor anyone else will know the origin of the data other than the fact that it came from an authorized participant via the app, thus the data is not linked to participants. 
""")


link = '[Authorize with Fitbit](https://www.fitbit.com/oauth2/authorize?response_type=token&client_id=2389P9&redirect_uri=https%3A%2F%2Fvitovitals.org&scope=heartrate%20sleep%20oxygen_saturation%20respiratory_rate%20temperature&expires_in=604800)'
st.markdown(link, unsafe_allow_html=True)
st.caption("https://www.fitbit.com/oauth2/authorize?response_type=token&client_id=2389P9&redirect_uri=https%3A%2F%2Fvitovitals.org&scope=heartrate%20sleep%20oxygen_saturation%20respiratory_rate%20temperature&expires_in=604800")

fitbitResponse = st.text_input("Enter Response From Fitbit Authorization")

if fitbitResponse != "":
    parsed = fitbitResponse.split("#access_token=")[1]
    
    token = parsed.split("&user_id")[0]
    user_id = parsed.split("&user_id=")[1].split("&")[0]
    
    st.write(hr("2020-01-01", "2022-01-08", token, user_id))





