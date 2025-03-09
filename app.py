import streamlit as st
import os
from PIL import Image
import caption_generator
import database

# Initialize the database
database.init_db()

st.title("📸 AI-Powered Media Caption Generator")
st.write("Upload an image or a video, and get an AI-generated caption.")

uploaded_file = st.file_uploader("Upload Image or Video", type=["jpg", "png", "mp4"])

if uploaded_file:
    file_path = os.path.join("uploads", uploaded_file.name)
    os.makedirs("uploads", exist_ok=True)
    
    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())

    # Image processing
    if uploaded_file.type in ["image/jpeg", "image/png"]:
        st.image(file_path, caption="Uploaded Image", use_column_width=True)
        
        caption = caption_generator.generate_caption(file_path)
        st.subheader("📝 Generated Caption:")
        st.write(caption)

    # Video processing
    elif uploaded_file.type == "video/mp4":
        st.video(file_path)
        st.subheader("🔄 Processing Video...")
        captions = caption_generator.generate_video_captions(file_path)
        
        for frame, caption in captions.items():
            st.image(frame, caption=f"Frame Caption: {caption}")

# Display stored captions
st.subheader("📂 Stored Captions")
stored_files = os.listdir("uploads")

for file_name in stored_files:
    caption = database.get_caption(os.path.join("uploads", file_name))
    if caption:
        st.write(f"**{file_name}**: {caption}")


