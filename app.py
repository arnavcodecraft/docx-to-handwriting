import streamlit as st
from docx import Document
from PIL import Image, ImageDraw, ImageFont
import os

st.set_page_config(page_title="Docx to Handwriting", page_icon="✍️", layout="centered")

st.title("✍️ Docx to Realistic Handwritten Notes")
st.write("Convert your Word documents into authentic-looking handwritten notes instantly!")

# File uploaders
uploaded_docx = st.file_uploader("Upload your Word Document (.docx)", type=["docx"])
uploaded_font = st.file_uploader("Upload a Handwriting Font (.ttf)", type=["ttf"])

if uploaded_docx is not None:
    # Save uploaded docx temporarily
    with open("temp.docx", "wb") as f:
        f.write(uploaded_docx.getbuffer())

    # Read text from docx
    doc = Document("temp.docx")
    full_text = [para.text for para in doc.paragraphs if para.text.strip()]
    text = "\n".join(full_text)

    if st.button("Generate Handwritten Notes"):
        if uploaded_font is not None:
            font_path = "temp_font.ttf"
            with open(font_path, "wb") as f:
                f.write(uploaded_font.getbuffer())
        else:
            font_path = None
            st.warning("Please upload a .ttf handwriting font for best results. Using default system font fallback.")

        # Page Setup
        img_width, img_height = 1240, 1754
        margin = 100
        line_spacing = 45

        try:
            font = ImageFont.truetype(font_path, size=36) if font_path else ImageFont.load_default()
        except Exception:
            font = ImageFont.load_default()

        image = Image.new("RGB", (img_width, img_height), color=(255, 255, 255))
        draw = ImageDraw.Draw(image)

        x, y = margin, margin
        max_width = img_width - (margin * 2)

        paragraphs = text.split("\n")
        for paragraph in paragraphs:
            words = paragraph.split(" ")
            current_line = ""
            for word in words:
                test_line = current_line + word + " "
                bbox = draw.textbbox((0, 0), test_line, font=font)
                w = bbox[2] - bbox[0]
                
                if w <= max_width:
                    current_line = test_line
                else:
                    draw.text((x, y), current_line, fill=(20, 24, 82), font=font)
                    y += line_spacing
                    current_line = word + " "
                    
                    if y > img_height - margin:
                        # For simplicity, saving single page or first page preview here
                        break

            if current_line:
                draw.text((x, y), current_line, fill=(20, 24, 82), font=font)
                y += line_spacing * 1.5

        # Save and display result
        output_path = "handwritten_output.png"
        image.save(output_path)
        
        st.success("Notes generated successfully!")
        st.image(output_path, caption="Generated Handwritten Note", use_container_width=True)
        
        with open(output_path, "rb") as file:
            st.download_button(
                label="Download Image",
                data=file,
                file_name="handwritten_notes.png",
                mime="image/png"
            )
