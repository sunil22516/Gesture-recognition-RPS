# ROCK-ing BOT — Deployment Guide

## Project Structure
```
rps-app/
├── frontend/
│   └── index.html        ← deploy to Netlify
└── backend/
    ├── app.py            ← deploy to Render
    └── requirements.txt
```

---

## STEP 1 — Deploy Backend to Render (free)

1. Go to https://render.com → sign up / log in
2. New → **Web Service** → connect your GitHub repo
3. Put your backend folder contents in the repo
4. **Copy your saved model** `rock_paper_scissors_model.h5` into the backend folder
5. Render settings:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app:app --host 0.0.0.0 --port 10000`
6. Deploy → copy the URL (e.g. `https://rocking-bot.onrender.com`)

---

## STEP 2 — Update Frontend with Backend URL

In `frontend/index.html`, find line:
```js
const API_URL = "https://YOUR-RENDER-APP.onrender.com/predict";
```
Replace with your actual Render URL:
```js
const API_URL = "https://rocking-bot.onrender.com/predict";
```

---

## STEP 3 — Deploy Frontend to Netlify

**Option A (drag & drop — easiest):**
1. Go to https://netlify.com → log in
2. Drag your `frontend/` folder onto the Netlify dashboard
3. Done — get your live URL!

**Option B (GitHub):**
1. Push `frontend/` to GitHub
2. Netlify → New Site → connect repo
3. Publish directory: `frontend`

---

## STEP 4 — Fix CORS (after deploy)

In `backend/app.py`, update CORS to your Netlify URL:
```python
allow_origins=["https://your-site.netlify.app"]
```
Redeploy backend on Render.

---

## Notes
- Render free tier **sleeps after 15 min** of inactivity — first request may take ~30s to wake up
- For always-on, upgrade Render to paid ($7/mo) or use Railway.app
- Model file must be in the same folder as `app.py` on Render
