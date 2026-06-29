import streamlit as st
import ollama
from PIL import Image
import pytesseract

st.set_page_config(page_title="Gemma Medical Scribe", page_icon="🩺", layout="wide")

st.title("🩺 Gemma-Medical-Scribe")
st.subheader("Offline Clinical Reasoning at the Edge")
st.caption("Powered by Gemma 4 E4B · Running locally via Ollama · Zero internet required")

# Sidebar — model status
with st.sidebar:
    st.markdown("### 🖥️ System Status")
    st.success("Gemma 4 E4B — Online (Local)")
    st.error("Internet — Disconnected")
    st.info("Mode: Full Offline Edge")
    st.markdown("---")
    st.markdown("**Model:** `gemma4:e4b`")
    st.markdown("**Runtime:** Ollama")
    st.markdown("**OCR Engine:** Tesseract")

# Tabs for input modes
tab1, tab2 = st.tabs(["✍️ Manual Notes", "📷 Scan Chart"])

def generate_medical_summary(patient_notes):
    response = ollama.chat(model='gemma4:e4b', messages=[
        {'role': 'system', 'content': 'You are a professional medical scribe. Structure notes clearly and flag any urgent findings.'},
        {'role': 'user', 'content': f'Summarize these notes into a SOAP format: {patient_notes}'}
    ])
    return response['message']['content']

with tab1:
    notes = st.text_area("Enter raw patient observations:", height=200,
                         placeholder="e.g. 34F, persistent cough 3 weeks, night sweats, weight loss 4kg, T 38.4°C, SpO2 94%…")
    if st.button("Generate SOAP Note", type="primary"):
        if notes:
            with st.spinner("Gemma 4 E4B reasoning locally…"):
                summary = generate_medical_summary(notes)
                st.markdown("### 📋 Generated SOAP Note")
                st.markdown(summary)
                st.download_button("📥 Download Note", summary, file_name="soap_note.txt")
        else:
            st.warning("Please enter patient observations first.")

with tab2:
    uploaded = st.file_uploader("Upload a photo of the patient chart", type=["jpg", "jpeg", "png"])
    if uploaded:
        img = Image.open(uploaded)
        st.image(img, caption="Uploaded Chart", use_column_width=True)
        if st.button("Transcribe & Analyse", type="primary"):
            with st.spinner("Running OCR + Gemma 4 E4B locally…"):
                raw_text = pytesseract.image_to_string(img)
                summary = generate_medical_summary(raw_text)
                st.markdown("### 🔍 OCR Extracted Text")
                st.code(raw_text)
                st.markdown("### 📋 Generated SOAP Note")
                st.markdown(summary)
                st.download_button("📥 Download Note", summary, file_name="soap_note.txt")
