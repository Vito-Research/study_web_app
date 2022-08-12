import streamlit as st
import pandas as pd
def results(date, hrDF, hrvDF, brDF, o2DF):
    def analyze(df, title):
        
        df["startTime"] = pd.to_datetime(df["dateTime"]).dt.hour
        df["startDate"] = pd.to_datetime(df["dateTime"]).dt.date
        df["startWeek"] = pd.to_datetime(df["dateTime"]).dt.week

        # aWeekAgo = pd.to_datetime(datetime.datetime.now() + datetime.timedelta(days= daysBefore))
       
        dfBeforeSick = df[df["startDate"] < date]

        dfAfterSick = df[df["startDate"] > date]
        
        st.write(unit + " Before Sick: " + str(dfBeforeSick["value"].median()))
        st.write(unit + " Three days prior to symptoms: " + str(dfAfterSick["value"].median()))
        
        groupedByWeek = df.groupby(df["startWeek"])['value'].median()
        st.line_chart(groupedByWeek)

    accuracy = 0.0

    st.header("Results")
    st.metric("The algorithm detected your infection days prior", accuracy)
    st.caption("We are believe in transparency, therefore we believe that you should see your trends in realtime.  This is not a medical diagnosis, rather general trends while you had an illness.")
    analyze(hrDF, "Heart Rate")
    analyze(hrvDF, "Heart Rate Variability Rate")
    analyze(brDF, "Breathing Rate")
    analyze(o2DF, "Blood Oxygen %")

