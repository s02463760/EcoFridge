import os
import openai
import streamlit as st
from openai import OpenAI


st.set_page_config(
    page_title="Fridge Alert",
    page_icon=":fork_and_knife:",
    layout="wide",
)

#openai.api_key = os.environ["OPENAI_API_KEY"]

client = OpenAI(api_key="OPENAI_API_KEY") 

# create a wrapper function
def get_completion(prompt, model="gpt-3.5-turbo"):
   completion = client.chat.completions.create(
        model=model,
        messages=[
        {"role":"system",
         "content": "Your job is to create, suggest recipes, and alert users of expiration dates."},
        {"role": "user",
         "content": prompt},
        ]
    )
   return completion.choices[0].message.content

st.markdown("# Fridge Alert 🍽️")
st.write(
    "Enter what you have in your refrigerator and we'll alert the ingredients for you!"
)

# create our streamlit app
with st.form(key = "chat"):
    prompt = st.text_input("Alert", placeholder="Enter information about your ingredients...")
    submitted = st.form_submit_button("Get your alert information 🍲")
    
    if submitted:
        st.write(get_completion(prompt))
