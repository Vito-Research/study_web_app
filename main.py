import streamlit as st
import fire
from fitbit import *
from result import results
from datetime import date
import datetime
from results import results

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

    link = "https://www.fitbit.com/oauth2/authorize?response_type=token&client_id=2389P9&redirect_uri=https%3A%2F%2Fvitovitals.org&scope=heartrate%20sleep%20oxygen_saturation%20respiratory_rate%20temperature&expires_in=604800"
    st.markdown(f'[Authorize with Fitbit]({link})', unsafe_allow_html=True)
    st.caption(link)

    response_container = st.container()
    fitbit_response = response_container.text_input("Enter Response From Fitbit Authorization")

    preview = st.expander("Data Preview")
    preview_placeholder = preview.empty()
    preview_placeholder.write("No data to display")

    fitbit_data = FitbitData()

    if fitbit_response != "":
        try:
            parsed = fitbit_response.split("#access_token=")[1]
            token = parsed.split("&user_id")[0]
            user_id = parsed.split("&user_id=")[1].split("&")[0]

            preview_container = preview_placeholder.container()
            preview_container.markdown(f"**User ID:**  \n{user_id}")
            preview_container.markdown(f"**Access Token:**  \n{token}")

            fitbit_data.heart_rate = get_heart_rate(token, user_id, "2020-01-01", "2022-01-08")
            fitbit_data.heart_rate_variability = get_heart_rate_variability(token, user_id, "2020-01-01", "2022-01-08")
            fitbit_data.breathing_rate = get_breathing_rate(token, user_id, "2020-01-01", "2022-01-08")
            fitbit_data.oxygen_saturation = get_oxygen_saturation(token, user_id, "2020-01-01", "2022-01-08")

            preview_container.write(fitbit_data.heart_rate)
            preview_container.write(fitbit_data.heart_rate_variability)
            preview_container.write(fitbit_data.breathing_rate)
            preview_container.write(fitbit_data.oxygen_saturation)
            
            anchorDate = datetime.datetime.strftime(date.today(), '%Y-%m-%d')
            date = st.date_input("Enter date that you had an infection")
            st.write(str(datetime.datetime.strftime(date, '%Y-%m-%d')))
          

            col1, col2 = st.columns([1, 6])
            if col1.button("Submit"):
                with col2:
                    with st.spinner("Uploading data..."):
                        fire.upload_fitbit_data(fitbit_data)
                st.success("Data uploaded successfully!")
                results(date, fitbit_data)
        except:
            st.error("Error uploading data!")
        


if __name__ == "__main__":
    main()
