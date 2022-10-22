from urllib.parse import urlencode
import streamlit as st
import json
import fire
from fitbit import *
import datetime
from result import results
import json
from streamlit.components.v1 import html
import hashlib

def main():
    key_dict = json.loads(st.secrets['textkey'])
    fire.init(key_dict)

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
    
    You are being asked to participate in this study because you are a student at the University of North Florida who 
    has a smartwatch, are willing to download the app used to conduct the study, and are willing to report a COVID-19 
    diagnosis and/or log symptoms upon notification from the app. Please keep in mind that this is voluntary, 
    meaning you may only participate if you desire to. Participating in this study requires ten minutes of setup time 
    and roughly five minutes per month of symptom logging. Benefits of this study include reducing future spread of 
    viral infections via real-time alerting of infection, encouraging further testing of infectious diseases, 
    and conducting a more in-depth analysis of one’s health via a medical professional’s supervision. 
    
    There are no known risks to participating in this study. The data used in this study are collected anonymously, 
    and neither the researchers nor anyone else will know the origin of the data other than the fact that they came 
    from an authorized participant via the app, thus the data are not linked to participants.
    """)

    st.subheader("Upload Data")
    st.markdown("""
        1. Click \"Authorize with Fitbit\"
        2. If prompted, enter your login information
        3. Once redirected to Vito's website, copy the URL
        4. Paste the URL into the text box below
    """)

    link = "https://www.fitbit.com/oauth2/authorize?response_type=code&client_id=238Y7Z&redirect_uri=https://www.vitovitals.org&scope=heartrate%20sleep%20oxygen_saturation%20respiratory_rate%20temperature&expires_in=604800"
    st.markdown(f'[Authorize with Fitbit]({link})', unsafe_allow_html=True)
    st.caption(link)

    response_container = st.container()

    preview = st.expander("Data Preview")
    preview_placeholder = preview.empty()
    preview_placeholder.write("No data to display")

    fitbit_data = FitbitData()

    h = hashlib.new('sha256')
    date = st.date_input("Enter date that you had an infection")
    anchorDate = datetime.datetime.strftime(date.today(), '%Y-%m-%d')
    URL = "https://api.fitbit.com/oauth2/token?client_id={clientID}&code={code}&code_verifier={verifier}&grant_type=authorization_code"
    if str(datetime.datetime.strftime(date, '%Y-%m-%d')) != str(anchorDate):
   
            try:
                parms = st.experimental_get_query_params()
        
                token = parms.get("code")[0]
                st.write(token)
                token = requests.get(URL.format(clientID="2389P9", code=token, verifier=urlencode(h.hexdigest), auth=TokenAuth(token))).text()
                    
                st.write(token)
                user_id = ""

                preview_container = preview_placeholder.container()
                preview_container.markdown(f"**User ID:**  \n{user_id}")
                preview_container.markdown(f"**Access Token:**  \n{token}")
                
                start_date = datetime.datetime.strftime(pd.to_datetime(date + datetime.timedelta(days= -40)), '%Y-%m-%d')
                end_date = datetime.datetime.strftime(pd.to_datetime(date + datetime.timedelta(days= 20)), '%Y-%m-%d')

                fitbit_data.heart_rate = get_heart_rate(token, start_date, end_date)
                fitbit_data.heart_rate_variability = get_heart_rate_variability(token, start_date, end_date)
                fitbit_data.breathing_rate = get_breathing_rate(token, start_date, end_date)
                fitbit_data.oxygen_saturation = get_oxygen_saturation(token, start_date, end_date)

                preview_container.write(fitbit_data.heart_rate)
                preview_container.write(fitbit_data.heart_rate_variability)
                preview_container.write(fitbit_data.breathing_rate)
                preview_container.write(fitbit_data.oxygen_saturation)
            except IndexError:
                response_container.error("Invalid input")

    col1, col2 = st.columns([1, 6])
    if col1.button("Submit") and not fitbit_data.is_empty():
            with col2:
                with st.spinner("Uploading data..."):
                    fire.upload_fitbit_data(fitbit_data)
                    
            st.success("Data uploaded successfully!")
            results(date=date, data=fitbit_data)

if __name__ == "__main__":
    main()
