#!/bin/bash

echo "🚀 CIDion AI - Quick Deploy Script"
echo "================================="
echo ""

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "📝 Initializing Git repository..."
    git init
    git add .
    git commit -m "Initial commit - CIDion AI"
fi

echo "🌐 Choose your deployment platform:"
echo "1. Render.com (Recommended - Free with sleep)"
echo "2. Railway.app (Free $5/month credit)"
echo "3. Fly.io (Free tier available)"
echo "4. Manual setup instructions"
echo ""

read -p "Enter your choice (1-4): " choice

case $choice in
    1)
        echo ""
        echo "🎯 Render.com Deployment:"
        echo "1. Push this code to GitHub"
        echo "2. Go to https://render.com and sign up"
        echo "3. Click 'New +' → 'Web Service'"
        echo "4. Connect your GitHub repository"
        echo "5. Use these settings:"
        echo "   - Build Command: pip install -r requirements.txt"
        echo "   - Start Command: python -m uvicorn src.api.app:create_app --factory --host 0.0.0.0 --port \$PORT"
        echo "6. Add Environment Variable: GEMINI_API_KEY = your_api_key"
        echo "7. Deploy!"
        echo ""
        echo "📱 You'll get a URL like: https://cidion-ai-abc123.onrender.com"
        ;;
    2)
        echo ""
        echo "🚂 Railway.app Deployment:"
        echo "1. Install Railway CLI: npm install -g @railway/cli"
        echo "2. Run: railway login"
        echo "3. Run: railway init"
        echo "4. Run: railway up"
        echo "5. Set environment: railway variables set GEMINI_API_KEY=your_key"
        echo ""
        echo "📱 You'll get a URL like: https://cidion-ai.up.railway.app"
        ;;
    3)
        echo ""
        echo "✈️  Fly.io Deployment:"
        echo "1. Install Fly CLI: https://fly.io/docs/hands-on/install-flyctl/"
        echo "2. Run: fly auth login"
        echo "3. Run: fly launch"
        echo "4. Run: fly secrets set GEMINI_API_KEY=your_key"
        echo "5. Run: fly deploy"
        echo ""
        echo "📱 You'll get a URL like: https://cidion-ai.fly.dev"
        ;;
    4)
        echo ""
        echo "📚 Manual Setup:"
        echo "Check DEPLOY.md for detailed instructions"
        echo "All deployment files are ready in your project!"
        ;;
    *)
        echo "❌ Invalid choice. Please run the script again."
        ;;
esac

echo ""
echo "🔑 Don't forget to set your GEMINI_API_KEY environment variable!"
echo "🎉 Happy deploying!"
