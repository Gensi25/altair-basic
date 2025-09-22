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

#####

st.subheader("Average fuel efficiency")

mpg = alt.Chart(cars).mark_line(point=True).encode(
    alt.X('Year'),
    alt.Y('average(Miles_per_Gallon)')
)

hp = alt.Chart(cars).mark_line(point=True).encode(
    alt.X('Year'),
    alt.Y('average(Horsepower)')
)

chart = mpg & hp

st.altair_chart(chart)

st.text(
    "We can see that, in this dataset, over the 1970s and early ’80s the average fuel efficiency improved while the average horsepower decreased.")

#####

st.subheader("Horsepower efficiency")

chart = alt.Chart(cars).mark_point().encode(
    x='Horsepower',
    y='Miles_per_Gallon',
    color='Origin',
    tooltip=['Name', 'Origin']  # show Name and Origin in a tooltip
).interactive()

st.write(chart)

#####

st.subheader("As")

# create an interval selection over an x-axis encoding
brush = alt.selection_interval(encodings=['x'])

# determine opacity based on brush
opacity = alt.condition(brush, alt.value(0.9), alt.value(0.1))

# an overview histogram of cars per year
# add the interval brush to select cars over time
overview = alt.Chart(cars).mark_bar().encode(
    alt.X('Year:O', timeUnit='year',  # extract year unit, treat as ordinal
          axis=alt.Axis(title=None, labelAngle=0)  # no title, no label angle
          ),
    alt.Y('count()', title=None),  # counts, no axis title
    opacity=opacity
).add_params(
    brush  # add interval brush selection to the chart
).properties(
    width=400,  # set the chart width to 400 pixels
    height=50  # set the chart height to 50 pixels
)

# a detail scatterplot of horsepower vs. mileage
# modulate point opacity based on the brush selection
detail = alt.Chart(cars).mark_point().encode(
    alt.X('Horsepower'),
    alt.Y('Miles_per_Gallon'),
    # set opacity based on brush selection
    opacity=opacity
).properties(width=400)  # set chart width to match the first chart

# vertically concatenate (vconcat) charts using the '&' operator
chart = overview & detail

st.write(chart)

st.text(
    "The upper histogram shows the count of cars per year and uses an interactive selection to modify the opacity of points in the lower scatter plot, which shows horsepower versus mileage")

st.text("Drag out an interval in the upper chart and see how it affects the points in the lower chart.")
