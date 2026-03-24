# 🪨 RPS using CNN and recognition system — Hand Gesture Classifier

> An end-to-end ML project that classifies Rock, Paper, Scissors hand gestures using a custom CNN, deployed as a full-stack web application.

---

## 💡 What This Project Does

ROCK-ing BOT takes an image of a hand gesture, classifies it as **Rock**, **Paper**, or **Scissors** in real time, and returns a confidence score with a per-class probability breakdown. It also includes a playable game mode where the model predicts your move and the bot plays against you.

 The project is about — raw data → trained model → REST API → deployed frontend.

---

## 🧠 Tech Stack

| Layer | Technology |
|---|---|
| Model | TensorFlow / Keras (Custom CNN) |
| Data Processing | NumPy, OpenCV, scikit-learn |
| Backend API | FastAPI (Python) |
| Frontend | HTML + CSS + Vanilla JS |
| Hosting | Render (backend) · Netlify (frontend) |

---

## 🏗️ Architecture

```
User uploads image
      │
      ▼
[Netlify Frontend]  ── HTTP POST ──▶  [Render Backend / FastAPI]
                                              │
                                              ▼
                                      [Keras CNN Model]
                                              │
                                              ▼
                              { prediction, confidence, breakdown }
```

---

## 🔬 The Model

A custom CNN built from scratch:

```
Input (150×150×3)
  → Conv2D(32) + MaxPool
  → Conv2D(64) + MaxPool
  → Conv2D(64) + MaxPool
  → Flatten → Dropout(0.4) → Dense(512) → Dense(3, softmax)
```

**Training**: 2,523 images · 10 epochs · Adam optimizer  
**Augmentation**: horizontal/vertical flip, 90° rotation, zoom, height/width shift

---

## 📊 Results — 90.3% Accuracy

```
              precision    recall  f1-score   support

       Paper       0.90      0.90      0.90       124
        Rock       1.00      0.89      0.94       124
    Scissors       0.83      0.93      0.88       124

    accuracy                           0.90       372
   macro avg       0.91      0.90      0.90       372
```

**Overall Accuracy: 90.32%**

Notable: Rock achieves perfect precision (1.00) — when the model predicts Rock, it is always correct.

---

## 🐛 Key Bugs I Found & Fixed

### 1. Label Map Ordering (Critical — caused wrong predictions)
`os.listdir()` returns folders in random order each session. Labels were shuffled between training and inference, so the model was confidently predicting the wrong class.

**Fix**: One line — `sorted(os.listdir(directory))` guarantees alphabetical order every run.

### 2. Deprecated Generator API
`sample_images.next()` throws `AttributeError` on newer TensorFlow. Replaced with Python's built-in `next(sample_images)`.

### 3. Variable Name Collision
`train_images` was defined as a Keras generator, then silently overwritten with a NumPy array. The Gradio cell later crashed trying to call `.class_indices` on a NumPy array.

### 4. Out-of-Order Import
`classification_report` was used 2 cells before it was imported — `NameError` at runtime. Fixed by moving all sklearn imports to the top.

---

## 🚀 Running Locally

```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn app:app --reload --port 8000

# Frontend — open frontend/index.html
# Update API_URL to http://localhost:8000/predict
```

---

## 🌐 Deployment

1. Push `backend/` + `.h5` model to GitHub → deploy on **Render**
2. Set start command: `uvicorn app:app --host 0.0.0.0 --port 10000`
3. Paste Render URL into `frontend/index.html`
4. Drag `frontend/` folder onto **Netlify** → live in seconds

---

## 🔮 What I'd Improve

- **Transfer Learning (MobileNetV2)** — better real-world generalization beyond clean dataset images
- **Webcam support** — capture gestures live from the browser
- **Persist label_map as JSON** — avoid label re-ordering issues entirely across sessions

---

*TensorFlow · FastAPI · Netlify · Render*
