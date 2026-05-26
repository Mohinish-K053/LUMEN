import os, io, json, base64, traceback
import torch
import torch.nn as nn
from torchvision import transforms
import torchvision.models as tvmodels
from PIL import Image

CLASS_NAMES = ["anger", "disgust", "fear", "happy", "neutral", "sadness", "surprise"]

COGNITIVE_LOAD_MAP = {
    "anger":    "High Load",
    "disgust":  "High Load",
    "fear":     "High Load",
    "sadness":  "High Load",
    "surprise": "Optimal Load",
    "neutral":  "Optimal Load",
    "happy":    "Low Load"
}

def model_fn(model_dir):
    try:
        device = torch.device("cpu")
        net = tvmodels.resnet18(weights=None)
        net.conv1 = nn.Conv2d(1, 64, kernel_size=7, stride=2, padding=3, bias=False)
        net.fc = nn.Sequential(
            nn.Linear(512, 256), nn.ReLU(), nn.Dropout(0.5),
            nn.Linear(256, len(CLASS_NAMES))
        )
        model_file = next(
            (os.path.join(model_dir, f) for f in os.listdir(model_dir) if f.endswith(".pth")),
            None
        )
        if not model_file:
            raise FileNotFoundError("No .pth found in " + model_dir)
        net.load_state_dict(torch.load(model_file, map_location=device))
        net.eval()
        print("✅ Model loaded:", model_file)
        return net
    except Exception:
        traceback.print_exc()
        raise

def input_fn(request_body, content_type):
    data = json.loads(request_body)
    img_bytes = base64.b64decode(data["image"])
    return Image.open(io.BytesIO(img_bytes)).convert("L")

def predict_fn(image, model):
    tfm = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize((0.5,), (0.5,))
    ])
    x = tfm(image).unsqueeze(0)
    with torch.no_grad():
        out   = model(x)
        probs = torch.softmax(out, dim=1)
        conf, idx = torch.max(probs, 1)
    emotion = CLASS_NAMES[idx.item()]
    return {
        "emotion":        emotion,
        "cognitive_load": COGNITIVE_LOAD_MAP[emotion],
        "confidence":     round(conf.item(), 4)
    }

def output_fn(prediction, accept):
    return json.dumps(prediction), "application/json"