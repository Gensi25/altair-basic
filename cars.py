import altair as alt
import streamlit as st
import vega_datasets
import polars as pl

@st.cache_data
def load_data():
    return vega_datasets.data.cars()

cars = load_data()

st.header("Cars")

if st.checkbox("Show raw data"):
    st.write(vega_datasets.data.cars.url)
    st.write(cars)

st.subheader("Average mileage per Gallon by the year of manufacture")

chart = alt.Chart(cars).mark_line().encode(
    alt.X("Year"),
    alt.Y('average(Miles_per_Gallon)')
)

st.altair_chart(chart)