import streamlit as st
import pandas as pd
import numpy as np


st.title("Streamlit Text Input")

name = st.text_input("Enter your name")
if name:
    st.write(f"Hello, {name}")

age = st.slider("Select your age",0,100,25)
st.write(f"Your age is {age}")

options = ["Java","C#","Python","C++"]
choice=st.selectbox("Choose your favorite language:", options)

st.write(f"Your selected choice: {choice}")

data = {
    "Name" : ["Alice", "Bob", "Charlie", "Diana", "Ethan"],
    "Age" : [28, 34, 22, 30, 25],
    "City" : ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix"]
}

df = pd.DataFrame(data)
st.write(df)

uploaded_file = st.file_uploader("Choose a CSV file", type='csv')
if uploaded_file is not None:
    df=pd.read_csv(uploaded_file)
    st.write(df)

