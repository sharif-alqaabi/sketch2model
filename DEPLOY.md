# 🚀 Deployment Guide - Render + Netlify

## Stack
- **Backend:** Render.com
- **Frontend:** Netlify
- **Cost:** $0-7/month

---

## Prerequisites

### 1. Get API Keys

- **Anthropic API Key:** https://console.anthropic.com/
- **Fish Audio API Key:** https://fish.audio/

### 2. Push Code to GitHub

```bash
cd /home/rifatxia/Desktop/CalHacks2025
git add .
git commit -m "Ready for deployment"
git push origin main
```

---

## Step 1: Deploy Backend to Render (15 min)

### 1.1 Create Render Account
- Go to https://render.com
- Sign up with GitHub

### 1.2 Create New Web Service
- Click "New +" → "Web Service"
- Connect your GitHub repository
- Select your repository

### 1.3 Configure Service
- **Name:** `drawing-to-3d-backend`
- **Root Directory:** `backend`
- **Environment:** `Python 3`
- **Build Command:** `pip install --upgrade pip && pip install -r requirements.txt`
- **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
- **Instance Type:** Free (or Starter for $7/month - no cold starts)

**Note:** Render will auto-detect Python and use the build command. The Dockerfile is optional.

### 1.4 Add Environment Variables
Click "Advanced" → "Add Environment Variable":

```
ANTHROPIC_API_KEY = your_anthropic_key_here
FISH_AUDIO_API_KEY = your_fish_audio_key_here
ENVIRONMENT = production
```

### 1.5 Deploy
- Click "Create Web Service"
- Wait 5-10 minutes for deployment
- **Copy your backend URL:** `https://drawing-to-3d-backend.onrender.com`

### 1.6 Verify Backend
- Visit: `https://your-backend-url.onrender.com/docs`
- You should see the FastAPI documentation page

---

## Step 2: Deploy Frontend to Netlify (10 min)

### 2.1 Create Production Environment File

```bash
cd frontend
echo "VITE_API_URL=https://your-backend-url.onrender.com" > .env.production
```

**Replace** `your-backend-url.onrender.com` with your actual Render URL!

### 2.2 Create Netlify Account
- Go to https://netlify.com
- Sign up with GitHub

### 2.3 Create New Site
- Click "Add new site" → "Import an existing project"
- Choose "Deploy with GitHub"
- Select your repository
- Configure build settings:
  - **Base directory:** `frontend`
  - **Build command:** `npm run build`
  - **Publish directory:** `frontend/dist`

### 2.4 Add Environment Variable
- Before deploying, click "Show advanced"
- Click "New variable"
- Add:
  ```
  Key: VITE_API_URL
  Value: https://your-backend-url.onrender.com
  ```

### 2.5 Deploy
- Click "Deploy site"
- Wait 2-5 minutes
- **Copy your frontend URL:** `https://your-app.netlify.app`

---

## Step 3: Update CORS (5 min)

### 3.1 Add Frontend URL to Backend
- Go to Render Dashboard
- Select your backend service
- Go to "Environment" tab
- Click "Add Environment Variable"
- Add:
  ```
  Key: ALLOWED_ORIGINS
  Value: https://your-app.netlify.app
  ```

### 3.2 Redeploy Backend
- Click "Manual Deploy" → "Deploy latest commit"
- Wait 2-3 minutes

---

## Step 4: Test Your App! ✅

### 4.1 Visit Your App
- Go to: `https://your-app.netlify.app`

### 4.2 Test Drawing Mode
1. Draw a simple house on the canvas
2. Click "Generate 3D Design"
3. Wait for the 3D image to appear
4. Click "Estimate Cost"
5. Verify cost table shows $50,000 total

### 4.3 Test Voice Mode
1. Click "Voice Input" tab
2. Click microphone and describe a house
3. Stop recording
4. Verify transcription appears
5. Verify 3D design generates
6. Verify cost estimation works

### 4.4 Check for Errors
- Open browser console (F12)
- Look for any red errors
- If you see CORS errors, double-check Step 3

---

## Troubleshooting

### Backend Returns 502 Bad Gateway
**Solution:**
- Check Render logs: Dashboard → Logs
- Verify all environment variables are set
- Check if deployment completed successfully

### CORS Errors in Browser Console
**Solution:**
- Verify `ALLOWED_ORIGINS` includes your Netlify URL
- Make sure it's the exact URL (with https://)
- Redeploy backend after adding CORS

### Images Not Loading
**Solution:**
- Check browser console for errors
- Verify `VITE_API_URL` is set correctly in Netlify
- Test backend directly: `https://your-backend-url.onrender.com/docs`

### Cold Starts (15-30 second delay on first request)
**Solution:**
- This is normal on Render free tier
- Upgrade to Render Starter ($7/month) to eliminate cold starts

### Build Fails on Netlify
**Solution:**
- Check build logs in Netlify dashboard
- Verify `VITE_API_URL` environment variable is set
- Try building locally first: `cd frontend && npm run build`

---

## Cost Summary

| Tier | Backend | Frontend | Total | Notes |
|------|---------|----------|-------|-------|
| **Free** | Render Free | Netlify Free | $0/mo | Cold starts after 15 min |
| **Recommended** | Render Starter | Netlify Free | $7/mo | No cold starts, faster |

**Plus API costs:** ~$0.003 per 3D generation (Anthropic)

---

## Post-Deployment

### Monitor Usage
- **Render:** Dashboard → Metrics
- **Netlify:** Site → Analytics
- **Anthropic:** https://console.anthropic.com/usage

### Custom Domain (Optional)
- **Netlify:** Site settings → Domain management → Add custom domain
- **Render:** Settings → Custom domains

### Automatic Deployments
Both Render and Netlify auto-deploy when you push to GitHub:
```bash
git add .
git commit -m "Update feature"
git push origin main
# Automatically deploys to production!
```

---

## URLs to Save

- **Backend:** `https://_____________________.onrender.com`
- **Frontend:** `https://_____________________.netlify.app`
- **Backend Logs:** Render Dashboard → Logs
- **Frontend Logs:** Netlify Dashboard → Deploys → Deploy log

---

## Success! 🎉

Your app is now live and accessible to anyone with the URL. Share it with users and start collecting feedback!

### Next Steps:
- Share your app URL
- Monitor usage and costs
- Collect user feedback
- Plan improvements
- Consider upgrading to Render Starter ($7/mo) for better performance
