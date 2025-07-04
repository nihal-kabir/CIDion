# 🚀 CIDion AI - Deployment Guide

Deploy your CIDion AI assistant for free with a public URL!

## 🔒 Security First

**⚠️ Before deploying, ensure security:**
- Your `.env` file is excluded from git (check `.gitignore`)
- Never commit API keys to your repository
- Use platform environment variables for production
- Review [SECURITY.md](SECURITY.md) for detailed guidelines

## 🌟 Quick Deploy Options

### 1. **Render.com (Recommended - Easiest)**

**Steps:**
1. Push your code to GitHub (if not already)
2. Go to [render.com](https://render.com) and sign up
3. Click "New +" → "Web Service"
4. Connect your GitHub repository
5. Use these settings:
   - **Name**: `cidion-ai`
   - **Environment**: `Python`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python -m uvicorn src.api.app:create_app --factory --host 0.0.0.0 --port $PORT`
6. Add Environment Variables:
   - `GEMINI_API_KEY`: Your API key
   - `PORT`: 10000
   - `HOST`: 0.0.0.0
7. Click "Create Web Service"

**Result**: You'll get a URL like `https://cidion-ai-abc123.onrender.com`

---

### 2. **Railway.app (Fast & Simple)**

**Steps:**
1. Install Railway CLI: `npm install -g @railway/cli`
2. Login: `railway login`
3. In your project folder: `railway init`
4. Deploy: `railway up`
5. Add environment variable: `railway variables set GEMINI_API_KEY=your_key_here`

**Result**: You'll get a URL like `https://cidion-ai-production.up.railway.app`

---

### 3. **Vercel (Serverless)**

**Steps:**
1. Install Vercel CLI: `npm install -g vercel`
2. In your project folder: `vercel`
3. Follow the prompts
4. Add environment variable: `vercel env add GEMINI_API_KEY`

---

### 4. **Fly.io (Global Edge)**

**Steps:**
1. Install Fly CLI: [flyctl](https://fly.io/docs/hands-on/install-flyctl/)
2. Login: `fly auth login`
3. Launch: `fly launch`
4. Set secrets: `fly secrets set GEMINI_API_KEY=your_key_here`
5. Deploy: `fly deploy`

---

## 🔧 Pre-Deployment Checklist

Before deploying, ensure:

- [ ] Your `GEMINI_API_KEY` is ready
- [ ] All files are in your repository
- [ ] `requirements.txt` is complete
- [ ] Port configuration is flexible (uses `$PORT` environment variable)

## 📱 Sharing Your App

Once deployed, you can share your public URL with friends:

**Example URLs:**
- Render: `https://your-app-name.onrender.com`
- Railway: `https://your-app-name.up.railway.app`
- Vercel: `https://your-app-name.vercel.app`
- Fly.io: `https://your-app-name.fly.dev`

## 💡 Tips for Free Tier

1. **Render**: App sleeps after 15 minutes of inactivity (first request takes ~30 seconds to wake up)
2. **Railway**: $5 monthly credit, usage-based billing
3. **Vercel**: Great for serverless, some limitations on execution time
4. **Fly.io**: 3 shared-cpu VMs free

## 🛡️ Security Notes

- Never commit your `.env` file with real API keys
- Use environment variables on the platform
- Your app will be publicly accessible

## 🚨 If You Need Help

1. Check the deployment logs on your chosen platform
2. Ensure your `GEMINI_API_KEY` is properly set
3. Verify the health check endpoint: `/api/health`

---

**Ready to deploy? Choose your platform and follow the steps above!** 🎉
