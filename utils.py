import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image
import numpy as np

from pytorch_grad_cam import GradCAM
from pytorch_grad_cam.utils.image import show_cam_on_image

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

CLASSES = ["Bleached", "Healthy"]

# ------------------
# Load Model
# ------------------
def load_model(model_path):
    model = models.resnet50(pretrained=False)
    model.fc = nn.Linear(model.fc.in_features, 2)

    state = torch.load(model_path, map_location=DEVICE)
    if isinstance(state, dict) and "state_dict" in state:
        model.load_state_dict(state["state_dict"])
    else:
        model.load_state_dict(state)

    model.eval()
    model.to(DEVICE)
    return model


# ------------------
# Image Transform
# ------------------
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])


# ------------------
# Prediction
# ------------------
def predict(image, model):
    image = image.convert("RGB")
    input_tensor = transform(image).unsqueeze(0).to(DEVICE)

    with torch.no_grad():
        outputs = model(input_tensor)
        probs = torch.softmax(outputs, dim=1)
        conf, pred = torch.max(probs, 1)

    return (
        CLASSES[pred.item()],
        conf.item(),
        probs.cpu().numpy()[0],
        input_tensor
    )


# ------------------
# Grad-CAM (FIXED)
# ------------------
def generate_gradcam(image, input_tensor, model):
    target_layers = [model.layer4[-1]]

    cam = GradCAM(
        model=model,
        target_layers=target_layers
    )

    grayscale_cam = cam(input_tensor=input_tensor)[0]

    image_np = np.array(image.resize((224, 224))).astype(np.float32) / 255.0
    cam_image = show_cam_on_image(image_np, grayscale_cam, use_rgb=True)

    return cam_image
