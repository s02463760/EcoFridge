import os
import openai
import streamlit as st
from PIL import Image
import requests
from openai import OpenAI
from pathlib import Path

# Set page title and favicon
st.set_page_config(
    page_title="Recipe Recommendation",
    page_icon=":fork_and_knife:",
    layout="wide",
)

# Set OpenAI API key
openai.api_key = "API_KEY_HERE"
client = OpenAI(api_key="API_KEY_HERE")

# Function to download image from URL
def download_image(filename, url):
    response = requests.get(url)
    if response.status_code == 200:
        # Create the images directory if it doesn't exist
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        # Save the image to file
        with open(filename, "wb") as file:
            file.write(response.content)
    else:
        st.error("Error downloading image from URL.")

# Function to generate filename from input prompt
def filename_from_input(prompt):
    # Remove all non-alphanumeric characters from the prompt except spaces
    alphanum = "".join(
        char if char.isalnum() or char == " " else "" for char in prompt
    )
    # Split the alphanumeric prompt into words
    alphanum_split = alphanum.split()
    # Take the first three words if there are more than three, else take all of them
    if len(alphanum_split) > 3:
        alphanum_split = alphanum_split[:3]
    # Join the words with underscores and return the result
    return "images/" + "_".join(alphanum_split) + ".png"

# Function to generate image using OpenAI API
def get_image(prompt, model="dall-e-2"):
    with st.spinner("Generating image..."):
        image = client.images.generate(
            prompt=prompt,
            model=model,
            n=1,
            size="1024x1024",
        )
    # Download the image
    filename = filename_from_input(prompt)
    download_image(filename, image.data[0].url)
    return filename

# Main Streamlit app
st.markdown("# Recipe Recommendations 🍽️")
st.write(
    "Enter what you have in your refrigerator and we'll recommend a recipe for you!"
)

with st.form(key="chat"):
    prompt = st.text_input("Ingredients", placeholder="Enter ingredients...")
    submitted = st.form_submit_button("Get Recipe 🍲")

    if submitted:
        filename = get_image(prompt)
        image = Image.open(filename)
        st.image(image, caption="Generated Recipe 🥗", use_column_width=True)
        st.text("Click Get Recipe again to see more options")
