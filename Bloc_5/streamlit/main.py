import streamlit as st
from PIL import Image
import pandas as pd
import numpy as np
import requests
import re
import plotly.express as px
import plotly.graph_objects as go


def checkout_state(row):
    state = 'Unknown'
    if row['state'] == 'ended':
        if row['delay_at_checkout_in_minutes'] <= 0:
            state = "On time checkout"
        elif row['delay_at_checkout_in_minutes'] > 0:
            state = "Late checkout"
    if row['state'] == 'canceled':
        state = "Canceled"
    return state

def checkout_delay(row):

    if row['delay_at_checkout_in_minutes'] < 0 :
        delay = 'A- No delay'
    elif row['delay_at_checkout_in_minutes'] == 0 :
        delay = 'B- Perfect time'
    elif row['delay_at_checkout_in_minutes']  < 15 :
        delay ='C- Delay < 15 mins'
    elif row['delay_at_checkout_in_minutes']  < 60 :
        delay = 'D- Delay < 1 hour'
    elif row['delay_at_checkout_in_minutes']  > 60 :
        delay = 'E- Delay > 1 hour'
    else:
        delay = "F- It's too late"
    return delay


if __name__ == '__main__':


    st.set_page_config(page_title="Dashboard Getaround", page_icon="📊")

    # App
    st.title('Getaround Delay Analysis ⏱️ 🚗')

    st.markdown("# Dashboard Getaround")
    st.sidebar.header("Dashboard Getaround")
    
    @st.cache_resource
    def load_data():
        fname = 'get_around_delay_analysis_clean1.csv'
        data = pd.read_csv(fname)
        return data

    raw_df = load_data()



    ### Processing data
    df = raw_df.copy()



    #### modify 'state' column to add information on whether checkout is on time or late:
    df['state'] = df.apply(checkout_state, axis = 1)
    df['delay'] = df.apply(checkout_delay, axis = 1)


    # Content
    st.sidebar.header("Table of content")
    st.sidebar.markdown("""
        * [Preview of data set](#dataset-preview)
        * [Graph 1](#graph-1) - Distribution of the delay intervals 
        * [Graph 2](#graph-2) - Distribution of the delay intervals by their status
        * [Graph 3](#graph-3) - Distribution of the delay intervals by their status and checkin types
        * [Graph 4](#graph-4) - Playing with parameters to be able to interpret previous plot a bit better
        * [Graph 5](#graph-5) - Distribution of delta time between two rentals in minutes

        
    """)

    st.markdown("---")
    st.subheader('Dataset Preview')
    # Run the below code if the check is checked
    if st.checkbox('Show processed data'):
        st.subheader('Overview of 10 random rows')
        st.write(df.sample(10))
    st.markdown("""
        In this dataset, we use a clean version where processing has made before during the EDA.
    """)
    # Graph 1
    st.subheader('Graph 1')
    st.markdown("Distribution of the delay intervals")
    fig1 = px.histogram(df, x='delay')
    st.plotly_chart(fig1, use_container_width=True)

    st.markdown("""
        We can see that delay at checkout is very common among Getaround drivers.
        It can range from couple minutes to more than an hour.
    """)
    st.markdown("---")

    # Graph 2
    st.subheader('Graph 2')
    st.markdown("Distribution of the delay intervals by their status")
    fig2 = px.histogram(df, x='state', color='delay')
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown("""we can see that many people canceled their ride possibly due to the delay at checkout and for some people
    we have a unknown statut.
    """)
    st.markdown("---")

    # Graph 3
    st.subheader('Graph 3')
    st.markdown(
        "Distribution of rentals being on time or late by their status and checkin types")
    fig3 = px.histogram(df, x='state', color='delay',
                        facet_col='checkin_type')
    st.plotly_chart(fig3, use_container_width=True)
    st.markdown("""
        See comments with the next figure.
    """)
    st.markdown("---")


    # Graph 4
    st.subheader('Graph 4')
    st.markdown(
        "Playing with parameters to have better interpretation.")
    fig4 = px.histogram(df, x='state', color='delay',
                        facet_col='checkin_type')
    st.plotly_chart(fig4, use_container_width=True)
    st.markdown("""
        Checkin type of 'connect' are much less used by drivers than traditional mobile way of checking in.
        The drivers who checked in with 'connect' feature had much less delay in proportion than the drivers who checked in without 'connect' feature.

        It seems like the checkin type of 'connect' reduces the late checkouts.
    """)
    st.markdown("---")

    # Graph 5
    st.subheader('Graph 5')
    st.markdown("Distribution of delta time between two rentals in minutes")
    fig5 = px.box(
        df,
        x='state',
        y='time_delta_with_previous_rental_in_minutes',
        facet_col='checkin_type')
    fig5.update_layout(yaxis_title="Delta time between two rentals in minutes")
    # quartilemethod="exclusive") # or "inclusive", or "linear" by default
    st.plotly_chart(fig5, use_container_width=True)
    ("""
        Delta time between two rentals in minutes does not seem to have an real impact.
    """)
    st.markdown("---")

    st.markdown("made with ❤️ by [Yann VAN ISACKER (Github : Yann-VI)](https://github.com/Yann-VI)")

