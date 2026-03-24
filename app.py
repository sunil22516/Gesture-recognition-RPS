from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import numpy as np
from PIL import Image
import io
import os
import tensorflow as tf
import gdown
import os

app = FastAPI(title="ROCK-ing BOT API")

# ── CORS — allow your Netlify domain ──────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # replace * with your netlify URL after deploy
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Load model once at startup ────────────────────────────────

MODEL_PATH = "rock_paper_scissors_model.h5"
FILE_ID = "https://drive.google.com/file/d/1GZ_G0dA269_UfnM3cmKdyrTI1uQlJlrS/view?usp=sharing"   # ← only thing you change

# Download model if not already present
if not os.path.exists(MODEL_PATH):
    print("Downloading model from Google Drive...")
    gdown.download(f"https://drive.google.com/uc?id={FILE_ID}", MODEL_PATH, quiet=False)
    print("Model downloaded!")

model = tf.keras.models.load_model(MODEL_PATH)

# ── Label map — sorted alphabetically (matches your training) ─
CLASS_NAMES = ["paper", "rock", "scissors"]  # sorted() order
EMOJI = {"rock": "🪨", "paper": "📄", "scissors": "✂️"}


@app.get("/")
def root():
    return {"status": "ROCK-ing BOT API is live ⚡"}


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        # Read and preprocess image
        contents = await file.read()
        img = Image.open(io.BytesIO(contents)).convert("RGB")
        img = img.resize((150, 150))
        img_array = np.array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        # Predict
        pred = model.predict(img_array)
        class_idx = int(np.argmax(pred))
        label = CLASS_NAMES[class_idx]
        confidence = float(np.max(pred)) * 100

        # All class probabilities
        breakdown = {
            CLASS_NAMES[i]: round(float(pred[0][i]) * 100, 1)
            for i in range(len(CLASS_NAMES))
        }

        return JSONResponse({
            "prediction": label,
            "emoji": EMOJI[label],
            "confidence": round(confidence, 1),
            "breakdown": breakdown
        })

    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
