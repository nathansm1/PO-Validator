
import streamlit as st
from PIL import Image
import pytesseract
import fitz  # PyMuPDF
import io
import re

st.title("🔍 PO Image Validator - Model & Voltage Checker")

# --- Upload files ---
st.header("1. Upload Files")
image_file = st.file_uploader("Upload Equipment Image (Nameplate)", type=["jpg", "jpeg", "png"])
pdf_file = st.file_uploader("Upload Purchase Order (PDF)", type=["pdf"])

# --- Function to extract text from image ---
def extract_text_from_image(img_file):
    image = Image.open(img_file)
    text = pytesseract.image_to_string(image)
    return text

# --- Function to extract text from PDF ---
def extract_text_from_pdf(pdf_file):
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    full_text = ""
    for page in doc:
        full_text += page.get_text()
    return full_text

# --- Function to extract Model and Voltage ---
def extract_model_voltage(text):
    model_match = re.search(r"MAR\d{2,4}-\d{1,2}", text.upper())
    voltage_match = re.search(r"(\d{3}|\d{2})\s?V", text.upper())
    model = model_match.group(0) if model_match else "Not found"
    voltage = voltage_match.group(0).replace(" ", "") if voltage_match else "Not found"
    return model, voltage

# --- Run extraction and comparison ---
if image_file and pdf_file:
    st.header("2. Extraction Results")

    # Extract from image
    st.subheader("🔹 From Image:")
    img_text = extract_text_from_image(image_file)
    img_model, img_voltage = extract_model_voltage(img_text)
    st.write(f"**Model:** {img_model}")
    st.write(f"**Voltage:** {img_voltage}")

    # Extract from PDF
    st.subheader("🔹 From Purchase Order:")
    pdf_text = extract_text_from_pdf(pdf_file)
    po_model, po_voltage = extract_model_voltage(pdf_text)
    st.write(f"**Model:** {po_model}")
    st.write(f"**Voltage:** {po_voltage}")

    # Comparison
    st.header("3. ✅ Comparison")
    st.write("Comparing extracted values...")

    model_match = img_model == po_model
    voltage_match = img_voltage == po_voltage

    st.write(f"**Model Match:** {'✅ Yes' if model_match else '❌ No'}")
    st.write(f"**Voltage Match:** {'✅ Yes' if voltage_match else '❌ No'}")

    if not model_match or not voltage_match:
        st.error("Discrepancy detected. Please verify manually.")
    else:
        st.success("All values match. Verified!")

else:
    st.info("Please upload both an image and a PO PDF to begin.")
