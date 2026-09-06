# 🚀 Deployment Guide - Render + Netlify

## Stack
- **Backend:** Render.com
- **Frontend:** Netlify
- **Total Cost:** $0-7/month

---

## 📁 Configuration Files

```
CalHacks2025/
├── backend/
│   ├── Dockerfile               # Docker configuration
│   └── .env.example            # Environment variables template
└── frontend/
    ├── .env.production.example  # Production env template
    └── netlify.toml            # Netlify deployment config
```

---

## 🚀 Quick Start Deployment (30 minutes)

### Step 1: Deploy Backend (15 min)

1. **Push to GitHub:**
   ```bash
   cd /home/rifatxia/Desktop/CalHacks2025
   git add .
   git commit -m "Ready for deployment"
   git push origin main
   ```

2. **Deploy to Render:**
   - Go to https://render.com
   - Sign up with GitHub
   - New Web Service → Connect repository
   - Configure:
     - Root Directory: `backend`
     - Build: `pip install -r requirements.txt`
     - Start: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - Add environment variables:
     - `ANTHROPIC_API_KEY`
     - `FISH_AUDIO_API_KEY`
     - `ENVIRONMENT=production`
   - Deploy!

3. **Copy backend URL:** `https://your-backend.onrender.com`

### Step 2: Deploy Frontend to Netlify (10 min)

1. **Create production env file:**
   ```bash
   cd frontend
   echo "VITE_API_URL=https://your-backend.onrender.com" > .env.production
   ```

2. **Deploy to Netlify:**
   - Go to https://netlify.com
   - Sign up with GitHub
   - New Site → Import from Git
   - Connect your repository
   - Configure:
     - **Base directory:** `frontend`
     - **Build command:** `npm run build`
     - **Publish directory:** `frontend/dist`
   
3. **Add environment variable:**
   - Site Settings → Environment Variables
   - Add: `VITE_API_URL` = `https://your-backend.onrender.com`

4. **Deploy!**
   - Click "Deploy site"
   - Copy your Netlify URL: `https://your-app.netlify.app`

### Step 3: Update CORS (5 min)

1. Go to Render Dashboard → Environment Variables
2. Add: `ALLOWED_ORIGINS` = `https://your-app.netlify.app`
3. Redeploy backend

### Step 4: Test! ✅

Visit your Netlify URL and test all features.

---

## 🔑 Required API Keys

You need these API keys before deployment:

1. **Anthropic API Key**
   - Get from: https://console.anthropic.com/
   - Used for: 3D generation and cost estimation
   - Cost: Pay-as-you-go (~$0.003 per request)

2. **Fish Audio API Key**
   - Get from: https://fish.audio/
   - Used for: Voice transcription
   - Cost: Free tier available

3. **Reka API Key** (Optional)
   - Get from: https://platform.reka.ai/
   - Used for: Research agent (currently disabled)
   - Cost: Free tier available

---

## 💰 Cost Breakdown

### Free Tier
- **Backend (Render Free):** $0/month
  - ⚠️ Cold starts after 15 min inactivity
- **Frontend (Netlify Free):** $0/month
  - ✅ 100GB bandwidth
  - ✅ Fast CDN
- **API Costs:** Pay-as-you-go
  - Anthropic: ~$0.003 per generation
  - Fish Audio: Free tier
- **Total:** $0/month + API usage

### Recommended (No Cold Starts)
- **Backend (Render Starter):** $7/month
  - ✅ No cold starts
  - ✅ Fast response times
- **Frontend (Netlify Free):** $0/month
- **Total:** $7/month + API usage

---

## 🎨 Features Ready for Production

✅ **Drawing to 3D Generation**
- Upload hand-drawn sketches
- AI generates 3D house designs
- Instant preview

✅ **Voice Input**
- Record voice descriptions
- Automatic transcription
- Generate designs from voice

✅ **Cost Estimation**
- Automatic material calculation
- Individual item costs
- Total cost: $50,000 (calculated dynamically)
- Professional table display

✅ **Responsive Design**
- Works on desktop, tablet, mobile
- Touch-friendly drawing canvas
- Adaptive layouts

---

## 🔒 Security Features

✅ API keys stored in environment variables
✅ CORS configured for production
✅ HTTPS enabled by default (Render + Vercel)
✅ Input validation on backend
✅ Error handling and logging

---

## 📈 Scaling Considerations

### Current Capacity (Free Tier)
- **Concurrent users:** 10-20
- **Requests/day:** Unlimited (with cold starts)
- **Storage:** Temporary (images not persisted)

### To Scale Further:
1. **Upgrade to Render Starter ($7/month)**
   - Handles 100+ concurrent users
   - No cold starts

2. **Add Database (PostgreSQL)**
   - Store user designs
   - Save cost estimates
   - User accounts

3. **Add CDN for Images**
   - Use Cloudinary or AWS S3
   - Faster image loading
   - Persistent storage

4. **Add Caching**
   - Redis for API responses
   - Reduce API costs
   - Faster responses

---

## 🐛 Common Issues & Solutions

### Issue: Backend returns 502 Bad Gateway
**Solution:** 
- Check Render logs for errors
- Verify all environment variables are set
- Ensure Python dependencies installed correctly

### Issue: CORS errors in browser
**Solution:**
- Add your Vercel URL to `ALLOWED_ORIGINS` in Render
- Redeploy backend
- Clear browser cache

### Issue: Images not loading
**Solution:**
- Check browser console for errors
- Verify backend URL in frontend `.env.production`
- Test backend `/docs` endpoint directly

### Issue: Cold starts (15-30 second delay)
**Solution:**
- Upgrade to Render Starter ($7/month)
- Or implement keep-alive ping service

---

## 📖 Full Deployment Instructions

See **`DEPLOY.md`** for complete step-by-step deployment guide.

---

## 🎉 You're Ready!

1. Read `DEPLOY.md`
2. Follow the 30-minute deployment process
3. Test your live app
4. Share with users!

**Good luck! 🚀**
