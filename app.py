import streamlit as st
import joblib
import numpy as np
import time

model = joblib.load("crop_recommendation_model.pkl")
label_encoder = joblib.load("label_encoder.pkl")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    .main {
        padding: 0rem 1rem;
    }
    
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        font-family: 'Poppins', sans-serif;
    }
    
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        backdrop-filter: blur(10px);
        margin-bottom: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        animation: fadeInDown 1s ease-out;
    }
    
    .main-title {
        font-size: 3rem;
        font-weight: 700;
        color: white;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        animation: glow 2s ease-in-out infinite alternate;
    }
    
    .main-subtitle {
        font-size: 1.2rem;
        color: rgba(255, 255, 255, 0.9);
        font-weight: 400;
        margin-top: 0;
    }
    
    .input-container {
        background: rgba(255, 255, 255, 0.1);
        padding: 2rem;
        border-radius: 15px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        margin-bottom: 2rem;
        animation: fadeInUp 1s ease-out;
    }
    
    .input-row {
        display: flex;
        gap: 1rem;
        margin-bottom: 1rem;
        flex-wrap: wrap;
    }
    
    .input-group {
        flex: 1;
        min-width: 250px;
    }
    
    .stNumberInput > div > div > input {
        background: rgba(255, 255, 255, 0.9);
        border: 2px solid rgba(255, 255, 255, 0.3);
        border-radius: 10px;
        padding: 0.5rem;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    
    .stNumberInput > div > div > input:focus {
        border-color: #4CAF50;
        box-shadow: 0 0 10px rgba(76, 175, 80, 0.3);
        transform: scale(1.02);
    }
    
    .stButton > button {
        width: 100%;
        padding: 1rem 2rem;
        font-size: 1.2rem;
        font-weight: 600;
        background: linear-gradient(45deg, #4CAF50, #45a049);
        color: white;
        border: none;
        border-radius: 15px;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(76, 175, 80, 0.4);
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(76, 175, 80, 0.6);
        background: linear-gradient(45deg, #45a049, #4CAF50);
    }

    /* --- ADDED CSS FOR CENTERING THE BUTTON --- */
    .center-btn-container {
        display: flex;
        justify-content: center;
        margin-top: 1rem; /* Add some space above the button */
    }
    .center-btn-container .stButton>button {
        width: auto; /* Let the button size itself */
        padding: 1rem 3rem; /* Adjust padding for a better look */
    }
    /* ------------------------------------------- */

    .result-container {
        background: rgba(255, 255, 255, 0.95);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        border: 1px solid rgba(255, 255, 255, 0.3);
        animation: bounceIn 0.8s ease-out;
        margin-top: 2rem;
    }
    
    .crop-result {
        font-size: 2.5rem;
        font-weight: 700;
        color: #2E7D32;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        animation: pulse 2s infinite;
    }
    
    .result-subtitle {
        font-size: 1.1rem;
        color: #666;
        margin-bottom: 1.5rem;
    }
    
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 1.5rem;
        margin-bottom: 2rem;
    }
    
    .feature-card {
        background: rgba(255, 255, 255, 0.1);
        padding: 1.5rem;
        border-radius: 15px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: transform 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(0,0,0,0.2);
    }
    
    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
        animation: float 3s ease-in-out infinite;
    }
    
    .feature-title {
        color: white;
        font-size: 1.3rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    .feature-desc {
        color: rgba(255, 255, 255, 0.8);
        font-size: 0.9rem;
        line-height: 1.5;
    }
    
    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes bounceIn {
        0% {
            opacity: 0;
            transform: scale(0.3);
        }
        50% {
            opacity: 1;
            transform: scale(1.05);
        }
        70% {
            transform: scale(0.9);
        }
        100% {
            opacity: 1;
            transform: scale(1);
        }
    }
    
    @keyframes glow {
        from {
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3), 0 0 10px rgba(255,255,255,0.3);
        }
        to {
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3), 0 0 20px rgba(255,255,255,0.6);
        }
    }
    
    @keyframes pulse {
        0% {
            transform: scale(1);
        }
        50% {
            transform: scale(1.05);
        }
        100% {
            transform: scale(1);
        }
    }
    
    @keyframes float {
        0%, 100% {
            transform: translateY(0px);
        }
        50% {
            transform: translateY(-10px);
        }
    }
    
    .loading-spinner {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid rgba(255,255,255,.3);
        border-radius: 50%;
        border-top-color: #fff;
        animation: spin 1s ease-in-out infinite;
        margin-right: 10px;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    
    .parameter-label {
        color: white;
        font-weight: 500;
        font-size: 1.1rem;
        margin-bottom: 0.5rem;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
    }
            


.section-title {
    text-align: center;
    color: white;
    font-size: 22px;
    font-weight: bold;
    margin-bottom: 15px;
}
        
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
    <h1 class="main-title">🌾 Smart Crop Recommendation</h1>
    <p class="main-subtitle">AI-Powered Agricultural Intelligence for Optimal Crop Selection</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="feature-grid">
        <div class="feature-card">
            <div class="feature-icon">🧪</div>
            <div class="feature-title">Soil Analysis</div>
            <div class="feature-desc">Advanced NPK analysis with pH monitoring for optimal soil conditions</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">🌡️</div>
            <div class="feature-title">Climate Factors</div>
            <div class="feature-desc">Temperature, humidity, and rainfall pattern analysis</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">🤖</div>
            <div class="feature-title">AI Prediction</div>
            <div class="feature-desc">Machine learning algorithms for accurate crop recommendations</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


with st.container():
    
    st.markdown('''
    <div class="input-container">
        <h3 class="section-title"> Enter Soil & Environmental Parameters</h3>
    ''', unsafe_allow_html=True)

    
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<p class="parameter-label">💧 Nitrogen (N)</p>', unsafe_allow_html=True)
        N = st.number_input("", min_value=0.0, max_value=200.0, step=1.0, key="nitrogen", help="Nitrogen content in soil (0-200)")

        st.markdown('<p class="parameter-label">🌡️ Temperature (°C)</p>', unsafe_allow_html=True)
        temperature = st.number_input("", min_value=0.0, max_value=50.0, step=0.1, key="temp", help="Average temperature in Celsius")

        st.markdown('<p class="parameter-label">⚗️ pH Value</p>', unsafe_allow_html=True)
        ph = st.number_input("", min_value=0.0, max_value=14.0, step=0.1, key="ph", help="Soil pH level (0-14)")

        st.markdown('<p class="parameter-label">🔥 Potassium (K)</p>', unsafe_allow_html=True)
        K = st.number_input("", min_value=0.0, max_value=200.0, step=1.0, key="potassium", help="Potassium content in soil (0-200)")

    with col2:
        st.markdown('<p class="parameter-label">⚡ Phosphorus (P)</p>', unsafe_allow_html=True)
        P = st.number_input("", min_value=0.0, max_value=200.0, step=1.0, key="phosphorus", help="Phosphorus content in soil (0-200)")

        st.markdown('<p class="parameter-label">💨 Humidity (%)</p>', unsafe_allow_html=True)
        humidity = st.number_input("", min_value=0.0, max_value=100.0, step=0.1, key="humidity", help="Relative humidity percentage")

        st.markdown('<p class="parameter-label">🌧️ Rainfall (mm)</p>', unsafe_allow_html=True)
        rainfall = st.number_input("", min_value=0.0, max_value=300.0, step=0.1, key="rainfall", help="Annual rainfall in millimeters")

    
    st.markdown('</div>', unsafe_allow_html=True)


col1, col2, col3 = st.columns([2, 1, 2])
with col2:
    predict_button = st.button("🔮 Get Crop Recommendation")


if predict_button:
  
    with st.spinner("🤖 Analyzing soil conditions and climate data..."):
       
        time.sleep(2)
        
        
        input_data = np.array([[N, P, K, temperature, humidity, ph, rainfall]])
        prediction = model.predict(input_data)
        crop_name = label_encoder.inverse_transform(prediction)[0]
        
    
        st.markdown(f"""
        <div class="result-container">
            <div class="crop-result">🌱 {crop_name.title()}</div>
            <div class="result-subtitle">Best crop recommendation for your conditions</div>
            <div style="margin-top: 1rem;">
                <span style="color: #4CAF50; font-weight: 600;">✅ Optimal Match</span>
                <span style="margin: 0 1rem; color: #ccc;">|</span>
                <span style="color: #FF9800; font-weight: 600;">📈 High Yield Potential</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.balloons()
        
        
st.markdown("""
<div style="text-align: center; padding: 2rem; color: rgba(255,255,255,0.7); margin-top: 3rem;">
    <p style="margin: 0; font-size: 0.9rem;">🌾 Smart Agriculture • AI-Powered Recommendations • 🌱</p>
    <p style="margin: 0.5rem 0 0 0; font-size: 0.8rem; opacity: 0.6;">Helping farmers make informed decisions with data-driven insights</p>
</div>
""", unsafe_allow_html=True)