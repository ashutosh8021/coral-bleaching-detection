import streamlit as st
from PIL import Image

from utils import load_model, predict, generate_gradcam

st.set_page_config(
    page_title="Coral Bleaching Detection",
    page_icon="🪸",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for enhanced UI/UX
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
    }
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
    }
    
    h1 {
        color: #00f5ff;
        text-align: center;
        padding: 30px 20px 10px 20px;
        font-size: 3.5rem !important;
        font-weight: 800 !important;
        text-shadow: 0 0 20px rgba(0, 245, 255, 0.5);
        letter-spacing: -1px;
    }
    
    h2 {
        color: #00f5ff !important;
        font-weight: 700 !important;
    }
    
    h3 {
        color: #ffffff !important;
        font-weight: 600 !important;
        font-size: 1.3rem !important;
    }
    
    .subtitle {
        text-align: center;
        color: #e0e0e0;
        font-size: 1.1rem;
        margin-bottom: 40px;
        padding: 20px 30px;
        background: rgba(0, 245, 255, 0.08);
        border-radius: 15px;
        box-shadow: 0 8px 32px rgba(0, 245, 255, 0.1);
        border: 1px solid rgba(0, 245, 255, 0.2);
        backdrop-filter: blur(10px);
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #00f5ff 0%, #00b8d4 100%);
        color: #000000;
        padding: 18px 40px;
        font-size: 1.1rem;
        font-weight: 700;
        border-radius: 30px;
        border: none;
        box-shadow: 0 8px 25px rgba(0, 245, 255, 0.4);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        width: 100%;
        letter-spacing: 0.5px;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #00b8d4 0%, #00f5ff 100%);
        box-shadow: 0 12px 35px rgba(0, 245, 255, 0.6);
        transform: translateY(-3px);
    }
    
    .prediction-box {
        background: rgba(30, 30, 60, 0.6);
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        margin: 20px 0;
        border: 2px solid rgba(0, 245, 255, 0.3);
        backdrop-filter: blur(10px);
    }
    
    .metric-card {
        background: rgba(40, 40, 80, 0.5);
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0, 245, 255, 0.2);
        margin: 10px 0;
        text-align: center;
        border: 1px solid rgba(0, 245, 255, 0.25);
        backdrop-filter: blur(5px);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0, 245, 255, 0.3);
    }
    
    .upload-section {
        background: rgba(30, 30, 60, 0.5);
        padding: 35px;
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
        margin: 20px 0;
        border: 2px solid rgba(0, 245, 255, 0.2);
        backdrop-filter: blur(10px);
    }
    
    .stProgress > div > div > div > div {
        background: linear-gradient(to right, #00f5ff, #00b8d4) !important;
        height: 8px !important;
        border-radius: 10px;
    }
    
    div[data-testid="stImage"] {
        border-radius: 20px;
        overflow: hidden;
        box-shadow: 0 8px 30px rgba(0, 245, 255, 0.2);
        border: 2px solid rgba(0, 245, 255, 0.3);
        transition: all 0.3s ease;
    }
    
    div[data-testid="stImage"]:hover {
        transform: scale(1.02);
        box-shadow: 0 12px 40px rgba(0, 245, 255, 0.3);
    }
    
    .healthy {
        color: #00f5ff !important;
        font-weight: 800 !important;
        font-size: 2.8rem !important;
        text-shadow: 0 0 20px rgba(0, 245, 255, 0.6);
        margin: 15px 0 !important;
    }
    
    .bleached {
        color: #ff4081 !important;
        font-weight: 800 !important;
        font-size: 2.8rem !important;
        text-shadow: 0 0 20px rgba(255, 64, 129, 0.6);
        margin: 15px 0 !important;
    }
    
    p {
        color: #e0e0e0 !important;
        line-height: 1.6;
    }
    
    label {
        color: #ffffff !important;
        font-weight: 600 !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: #00f5ff !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    [data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-size: 2.2rem !important;
        font-weight: 800 !important;
    }
    
    strong, b {
        color: #00f5ff !important;
        font-weight: 700 !important;
    }
    
    [data-testid="stFileUploader"] {
        background: rgba(30, 30, 60, 0.4);
        border: 2px dashed rgba(0, 245, 255, 0.4);
        border-radius: 15px;
        padding: 20px;
        transition: all 0.3s ease;
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: rgba(0, 245, 255, 0.6);
        background: rgba(30, 30, 60, 0.6);
    }
    
    [data-testid="stFileUploader"] label {
        color: #ffffff !important;
        font-size: 1.1rem !important;
    }
    
    .stMarkdown {
        color: #e0e0e0 !important;
    }
    
    hr {
        border-color: rgba(0, 245, 255, 0.2) !important;
    }
    
    /* Info box styling */
    .stAlert {
        background: rgba(0, 245, 255, 0.1) !important;
        border: 1px solid rgba(0, 245, 255, 0.3) !important;
        border-radius: 12px !important;
        color: #e0e0e0 !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("# 🪸 Coral Bleaching Detection")
st.markdown("### Automated Reef Health Monitoring with Visual Explanations")

st.markdown(
    """
    <div class="subtitle">
    🌊 Classify coral images as <b>Bleached</b> or <b>Healthy</b><br>
    with <b>visual heatmaps</b> showing which regions influenced the prediction.<br><br>
    ⚠️ <i>Research prototype</i>
    </div>
    """, unsafe_allow_html=True
)

st.markdown("<br>", unsafe_allow_html=True)

@st.cache_resource
def get_model():
    return load_model("coral_bleaching_resnet50_v1_1.pth")

model = get_model()

# Create two columns for better layout
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    uploaded_file = st.file_uploader(
        "📸 Upload a coral image",
        type=["jpg", "jpeg", "png"],
        help="Upload an image of coral to analyze its health status"
    )

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    
    # Center the button
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    with col_btn2:
        analyze_button = st.button("🔍 Analyze Coral Health", use_container_width=True)
    
    if analyze_button:
        with st.spinner("🧠 Analyzing image..."):
            label, confidence, probs, input_tensor = predict(image, model)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Side by side layout: Image on left, Results on right
        img_col, result_col = st.columns([1, 1])
        
        with img_col:
            st.markdown("### 📷 Uploaded Image")
            st.image(image, use_container_width=True)
        
        with result_col:
            # Display prediction with color coding
            label_class = "healthy" if label == "Healthy" else "bleached"
            emoji = "✅" if label == "Healthy" else "⚠️"
            
            st.markdown(f"### {emoji} Prediction Result")
            st.markdown(f'<p class="{label_class}">{label}</p>', unsafe_allow_html=True)
            
            # Confidence metrics
            st.metric(
                label="🎯 Confidence Score",
                value=f"{confidence*100:.1f}%",
                delta=None
            )
            
            # Progress bar
            st.progress(float(confidence))
            
            # Class Probabilities
            st.markdown("### 📈 Class Probabilities")
            prob_col1, prob_col2 = st.columns(2)
            
            with prob_col1:
                st.metric(
                    label="⚠️ Bleached",
                    value=f"{probs[0]*100:.1f}%"
                )
            
            with prob_col2:
                st.metric(
                    label="✅ Healthy",
                    value=f"{probs[1]*100:.1f}%"
                )
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        # Grad-CAM Explanation section below
        st.markdown("### 🔥 Visual Explanation (Grad-CAM)")
        
        with st.spinner("🎨 Generating heatmap..."):
            cam_image = generate_gradcam(
                image=image,
                input_tensor=input_tensor,
                model=model
            )
        
        # Display Grad-CAM side by side with original
        gradcam_col1, gradcam_col2 = st.columns(2)
        
        with gradcam_col1:
            st.markdown("**Original Image**")
            st.image(image.resize((224, 224)), use_container_width=True)
        
        with gradcam_col2:
            st.markdown("**Grad-CAM Heatmap**")
            st.image(cam_image, use_container_width=True)
        
        st.info(
            "🔍 **About Grad-CAM:** The heatmap highlights image regions that most influenced the model's prediction. "
            "Red/warm areas indicate high importance, while blue/cool areas show low importance. "
            "This improves model interpretability but does not guarantee biological causality.",
            icon="ℹ️"
        )
    else:
        # Show uploaded image before analysis
        col_preview1, col_preview2, col_preview3 = st.columns([1, 2, 1])
        with col_preview2:
            st.markdown("### 📷 Uploaded Image")
            st.image(image, use_container_width=True)

# Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: #64ffda;'>🌊 Coral Health Monitoring System | Powered by ResNet50 & Grad-CAM</p>",
    unsafe_allow_html=True
)
