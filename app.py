import streamlit as st
from src.predict import load_assets, predict_cell

st.set_page_config(page_title="Blood Cell Detector", layout="wide")
st.title("🩸 Blood Cell Anomaly Detection")

# تحميل الموديل من ملف الـ predict
try:
    model, scaler = load_assets()
except Exception as e:
    st.error("Error loading model files from 'models/' folder.")

# المدخلات
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("🔬 Cell Morphology")
    cell_diameter_um = st.number_input("Cell Diameter (μm)", value=10.0)
    nucleus_area_pct = st.number_input("Nucleus Area (%)", value=40.0)
    chromatin_density = st.number_input("Chromatin Density", value=0.4)
    cytoplasm_ratio = st.number_input("Cytoplasm Ratio", value=0.5)
    circularity = st.number_input("Circularity", value=0.7)
    eccentricity = st.number_input("Eccentricity", value=0.3)
    granularity_score = st.number_input("Granularity Score", value=1.5)
    lobularity_score = st.number_input("Lobularity Score", value=1.5)
    membrane_smoothness = st.number_input("Membrane Smoothness", value=0.8)

with col2:
    st.subheader("🖼️ Image & Pixel Data")
    cell_area_px = st.number_input("Cell Area (px)", value=1000)
    perimeter_px = st.number_input("Perimeter (px)", value=100)
    mean_r = st.number_input("Mean Red (R)", value=120)
    mean_g = st.number_input("Mean Green (G)", value=120)
    mean_b = st.number_input("Mean Blue (B)", value=120)
    stain_intensity = st.number_input("Stain Intensity", value=0.5)
    magnification_x = st.number_input("Magnification (X)", value=100)
    image_resolution_px = st.number_input("Resolution (px)", value=224)

with col3:
    st.subheader("👤 Patient & Blood Indices")
    patient_age_group = st.selectbox("Age Group", options=[("Pediatric", 0), ("Adult", 1), ("Elderly", 2)], format_func=lambda x: x[0])[1]
    patient_sex = st.selectbox("Sex", options=[("Male", 0), ("Female", 1)], format_func=lambda x: x[0])[1]
    wbc_count_per_ul = st.number_input("WBC Count (/μL)", value=7000)
    rbc_count_millions_per_ul = st.number_input("RBC Count (M/μL)", value=4.5)
    hemoglobin_g_dl = st.number_input("Hemoglobin (g/dL)", value=13.5)
    hematocrit_pct = st.number_input("Hematocrit (%)", value=40.0)
    platelet_count_per_ul = st.number_input("Platelets (/μL)", value=250000)
    mcv_fl = st.number_input("MCV (fL)", value=88.0)
    mchc_g_dl = st.number_input("MCHC (g/dL)", value=33.0)

# زر التنبؤ
if st.button("Predict Cell Status", type="primary"):
    features = [
        cell_diameter_um, nucleus_area_pct, chromatin_density, cytoplasm_ratio,
        circularity, eccentricity, granularity_score, lobularity_score,
        membrane_smoothness, cell_area_px, perimeter_px, mean_r, mean_g, mean_b,
        stain_intensity, patient_age_group, patient_sex, wbc_count_per_ul,
        rbc_count_millions_per_ul, hemoglobin_g_dl, hematocrit_pct,
        platelet_count_per_ul, mcv_fl, mchc_g_dl, magnification_x, image_resolution_px
    ]
    
    prediction = predict_cell(model, scaler, features)
    
    st.divider()
    if prediction == 1:
        st.error("⚠️ Prediction: **ABNORMAL CELL** (Anomaly Detected)")
    else:
        st.success("✅ Prediction: **NORMAL CELL**")