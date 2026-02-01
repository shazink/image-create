# Deployment Guide for Render

## Step 1: Deploy Backend

1. Go to [render.com](https://render.com) and sign in
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository: `shazink/image-create`
4. Configure the service:
   - **Name:** `image-gen-backend` (or your choice)
   - **Root Directory:** `backend`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `./start.sh`
   - **Instance Type:** Free
5. Add **Environment Variable**:
   - Key: `FREEPIK_API_KEY`
   - Value: `FPSX704de92ec6f01f15acbaea65afa782e0`
6. Click **"Create Web Service"**
7. **Copy your backend URL** (e.g., `https://image-gen-backend.onrender.com`)

## Step 2: Update Frontend API URL

Before deploying the frontend, update `frontend/src/App.jsx`:

Replace line 16:
```javascript
const res = await fetch("http://localhost:8000/generate", {
```

With your Render backend URL:
```javascript
const res = await fetch("https://YOUR-BACKEND-URL.onrender.com/generate", {
```

Then commit and push:
```bash
git add frontend/src/App.jsx
git commit -m "Update API URL for production"
git push
```

## Step 3: Deploy Frontend

1. In Render, click **"New +"** → **"Static Site"**
2. Connect the same GitHub repository
3. Configure:
   - **Name:** `image-gen-frontend`
   - **Root Directory:** `frontend`
   - **Build Command:** `npm install && npm run build`
   - **Publish Directory:** `dist`
4. Click **"Create Static Site"**

## Done! 🎉

Your app will be live at:
- Frontend: `https://image-gen-frontend.onrender.com`
- Backend: `https://image-gen-backend.onrender.com`

Both will auto-deploy when you push to GitHub!

## Important Notes

- **First Deploy:** Backend may take 5-10 minutes on first deploy
- **Free Tier:** Services sleep after 15 min of inactivity (30 sec to wake up)
- **CORS:** Already configured in backend to allow all origins
