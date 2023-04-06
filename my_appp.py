
import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image

# Title / Text

st.title("This is a title")
st.text("This is a text")

# Markdown

st.markdown("# Streamlit")
st.markdown("## Streamlit")
st.markdown("### Streamlit")
st.markdown("#### Streamlit")

# Header / Subheader

st.header("This is a header")
st.subheader("This is a subheader")

# success-info-error

st.success("This is a success message")
st.info("This is a info message")
st.error("This is a error message")
st.warning("This is a warning message")
st.exception("NameError('name three is not defined')")

# Help

st.help(range)

# Write

st.write("Hello C12 Cohort")
st.text("Hello C12 Cohort")

st.write(range(10))

# image

img = Image.open("20220527_160455.jpg")
st.image(img, caption="C12")

# Video

st.video("https://www.youtube.com/watch?v=uHKfrz65KSU")

# Checkbox

st.checkbox("Up and Down")

cbox = st.checkbox("Hide and Seek")

if st.checkbox("hide and seek"):
    st.write("hide")
else:
    st.write("seek")


# radio button   

st.radio("Select a color", ("Blue", "Red", "Yellow"))

status = st.radio("Select a color", ("blue", "orange", "yellow"))
st.write("Your favorite color is", status)

# button

st.button("Click me")

if st.button("Press me"):
    st.success("Prediction is ...")

# select box

st.selectbox("Your color", ["Blue", "Red", "Green"])

occupation=st.selectbox("Your Occupation", ["Programmer", "DataScientist", "Doctor"])
st.write("You selected this option :", occupation)

# multi select

st.multiselect("Select multiple numbers",[1,2,3,4,5])

multi_select = st.multiselect("Select multiple numbers",[6,7,8,9,10])
st.write("You selected this option :", multi_select)


# slider

option1 = st.slider("Select a number", min_value=5, max_value=70, value=30, step=5)
option2 = st.slider("Select a number", min_value=10, max_value=80, step=5)
option3 = st.slider("Select a number", 10)


result = option1 * option2
st.write("The result is:", result)


# text input

st.text_input("Enter your age", placeholder="Your name age")

name = st.text_input("Enter your name", placeholder="Your name here")
if st.button("Submit"):
    st.write("Hello", name.title())


# code

st.code("import pandas as pd")
st.code("import pandas as pd\nimport numpy as np")


with st.echo():
    import pandas as pd
    import numpy as np
    df = pd.DataFrame({"a":[1,2,3], "b":[4,5,6]})
    df


# date input

import datetime
today = st.date_input("Today is", datetime.datetime.now())

date = st.date_input("Enter the date")


# time input

hour = st.time_input(str(pd.Timestamp.now()))
st.write("Hour is", hour)

time = st.time_input("Time is")


# sidebar

st.sidebar.title("sidebar title")

st.sidebar.header("Sidebar header")
a=st.sidebar.slider("input",0,5,2,1)
x=st.sidebar.slider("input2")


st.write("# sidebar input result")
st.success(a*x)


# Dataframe oluşturma

df = pd.read_csv("Advertising.csv")

# 1. method

st.table(df.head())
st.table(df.tail())

# 2. method
st.write(df.sample(3))
st.write(df.isnull().sum())

# 3.method

st.dataframe(df.describe())
st.dataframe(df.shape)


# Project Example

import pickle

filename = 'my_model'
model = pickle.load(open(filename, 'rb'))

st.write(df.describe())

TV = st.sidebar.number_input("TV:",min_value=5, max_value=300)
radio = st.sidebar.number_input("radio:",min_value=1, max_value=50)
newspaper = st.sidebar.number_input("newspaper:",min_value=0, max_value=120)

my_dict = {
           "TV": TV,
           "radio": radio,
           "newspaper": newspaper
          }

df=pd.DataFrame.from_dict([my_dict])

st.table(df)

if st.button("Predict"):
    pred = model.predict(df)
    st.write(pred[0])






