import streamlit as st
import pandas as pd
import datetime
def results(date, data):
    def analyze(df, title = "", unit = ""):
       
            st.header(title)
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
       


    st.header("Results")
    # st.metric("The algorithm detected your infection days prior", accuracy)
    st.caption("We are believe in transparency, therefore we believe that you should see your trends in realtime.  This is not a medical diagnosis, rather general trends while you had an illness.")

    preview = st.expander("Parsed Data Preview")
    preview.write(pd.DataFrame([vars(f) for f in data]))
    try:
        analyze(pd.DataFrame([vars(f) for f in data.heart_rate]), "Heart Rate")
    except:
            st.error("Something went wrong")
    try:
        analyze(pd.read_json(pd.DataFrame([vars(f) for f in data.heart_rate_variability])), "Heart Rate Variability Rate")
    except:
            st.error("Something went wrong")
    try:
        analyze(pd.read_json(pd.DataFrame([vars(f) for f in data.breathing_rate])), "Breathing Rate")
    except:
            st.error("Something went wrong")
    try:
        analyze(pd.DataFrame([vars(f) for f in data.oxygen_saturation]), "Blood Oxygen %")
    except:
            st.error("Something went wrong")