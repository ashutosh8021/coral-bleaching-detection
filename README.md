# 🪸 Coral Bleaching Detection

A Streamlit web application for automated coral health monitoring using deep learning and visual explanations.

![Coral Bleaching Detection](screenshots/image.png)

## 📋 Overview

This application classifies coral images as **Bleached** or **Healthy** using a ResNet50 deep learning model and provides visual explanations through Grad-CAM heatmaps to show which regions of the image influenced the prediction.

## ✨ Features

- 🖼️ **Image Upload**: Easy drag-and-drop interface for coral images
- 🔍 **Binary Classification**: Identifies coral as Bleached or Healthy
- 📊 **Confidence Scores**: Shows prediction confidence and class probabilities
- 🔥 **Grad-CAM Visualization**: Heatmap overlay showing important image regions
- 🎨 **Modern UI**: Clean, responsive interface with dark theme

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/coral-bleaching-detection.git
cd coral-bleaching-detection
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
streamlit run app.py
```

The app will open in your default browser at `http://localhost:8501`

## 📦 Requirements

- streamlit
- torch
- torchvision
- Pillow
- numpy
- pytorch-grad-cam

See `requirements.txt` for specific versions.

## 🎯 Usage

1. **Upload Image**: Click "Browse files" or drag and drop a coral image (JPG, JPEG, or PNG)
2. **Analyze**: Click the "🔍 Analyze Coral Health" button
3. **View Results**: 
   - See the prediction (Bleached/Healthy)
   - Check confidence score and probabilities
   - View Grad-CAM heatmap visualization

## 🧠 Model

The application uses a **ResNet50** architecture pretrained and fine-tuned for coral bleaching detection. The model file (`coral_bleaching_resnet50_v1_1.pth`) contains the trained weights.

### Grad-CAM

Gradient-weighted Class Activation Mapping (Grad-CAM) provides visual explanations by highlighting the regions in the input image that were most important for the model's prediction.

## 📁 Project Structure

```
coral_streamlit_app/
├── app.py                              # Main Streamlit application
├── utils.py                            # Helper functions (model loading, prediction, Grad-CAM)
├── requirements.txt                    # Python dependencies
├── coral_bleaching_resnet50_v1_1.pth  # Trained model weights
├── screenshots/                        # Application screenshots
│   └── image.png
├── .gitignore                          # Git ignore file
├── .gitattributes                      # Git LFS configuration
└── README.md                           # This file
```

## ⚠️ Disclaimer

This is a **research prototype** for reef health monitoring. The predictions should not be used as the sole basis for critical decisions regarding coral reef conservation without expert validation.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available under the MIT License.

## 🌊 Acknowledgments

- ResNet50 architecture from PyTorch
- Grad-CAM implementation from pytorch-grad-cam
- Streamlit for the web framework

---

**Built with ❤️ for coral reef conservation**
