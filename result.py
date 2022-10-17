import streamlit as st
import pandas as pd
import datetime
def results(date, data):
    def analyze(df, title = "", unit = ""):
        try:
            df["startTime"] = pd.to_datetime(df["dateTime"]).dt.hour
            df["startDate"] = pd.to_datetime(df["dateTime"]).dt.date
            df["startWeek"] = pd.to_datetime(df["dateTime"]).dt.week

            aWeekAgo = pd.to_datetime(date + datetime.timedelta(days= -4))
        
            aWeekAfter = pd.to_datetime(date + datetime.timedelta(days= -4))
            dfBeforeSick = df[df["startDate"] > aWeekAgo and df["startDate"] < aWeekAfter]

            dfAfterSick = df[df["startDate"] < aWeekAgo or df["startDate"] > aWeekAfter]
            
            st.write(unit + " Before Sick: " + str(dfBeforeSick["value"].median()))
            st.write(unit + " Three days prior to symptoms: " + str(dfAfterSick["value"].median()))
            
            groupedByWeek = df.groupby(df["startWeek"])['value'].median()
            st.line_chart(groupedByWeek)
        except:
            st.error("Something went wrong")


    st.header("Results")
    # st.metric("The algorithm detected your infection days prior", accuracy)
    st.caption("We are believe in transparency, therefore we believe that you should see your trends in realtime.  This is not a medical diagnosis, rather general trends while you had an illness.")
    analyze(pd.read_json(data.heart_rate), "Heart Rate")
    analyze(pd.read_json(data.heart_rate_variability), "Heart Rate Variability Rate")
    analyze(pd.read_json(data.breathing_rate), "Breathing Rate")
    analyze(pd.read_json(data.oxygen_saturation), "Blood Oxygen %")