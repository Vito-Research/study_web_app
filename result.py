import streamlit as st
import pandas as pd
import datetime
import json
def results(date, data):
    def analyze(df, title = "", unit = "", col="restingHeartRate"):
       
            st.header(title)
            df["startDate"] = pd.to_datetime(df["dateTime"]).dt.date
            df["startWeek"] = pd.to_datetime(df["dateTime"]).dt.week

            aWeekAgo = pd.to_datetime(date + datetime.timedelta(days= -4))
        
            aWeekAfter = pd.to_datetime(date + datetime.timedelta(days= -4))
            dfBeforeSick = df[df["startDate"] > aWeekAgo and df["startDate"] < aWeekAfter]

            dfAfterSick = df[df["startDate"] < aWeekAgo or df["startDate"] > aWeekAfter]
            
            st.write(unit + " Before Sick: " + str(dfBeforeSick["value"][col].median()))
            st.write(unit + " Three days prior to symptoms: " + str(dfAfterSick["value"][col].median()))
            
            groupedByWeek = df.groupby(df["startWeek"])["value"][col].median()
            st.line_chart(groupedByWeek)
       


    st.header("Results")
    # st.metric("The algorithm detected your infection days prior", accuracy)
    st.caption("We are believe in transparency, therefore we believe that you should see your trends in realtime.  This is not a medical diagnosis, rather general trends while you had an illness.")

    try:
        analyze(pd.DataFrame.from_dict(data.heart_rate), "Heart Rate")
    except:
            st.error("Something went wrong")
    try:
        
        analyze(pd.read_json(pd.DataFrame(pd.DataFrame.from_dict(data.heart_rate_variability))), "Heart Rate Variability Rate", col="deepRmssd")
    except:
            st.error("Something went wrong")
    try:
        analyze(pd.read_json(pd.DataFrame(pd.DataFrame.from_dict(data.breathing_rate))), "Breathing Rate", col="breathingRate")
    except:
            st.error("Something went wrong")
    try:
        analyze(pd.DataFrame(pd.DataFrame(pd.DataFrame.from_dict(data.blood_oxygen))), "Blood Oxygen %", col="")
    except:
            st.error("Something went wrong")