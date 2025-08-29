# 🚀 Fake News Detector - Deployment Guide

This guide will help you deploy your Fake News Detector application to production. The application consists of two parts:
1. **Frontend**: Static HTML/CSS/JS (deployed to Netlify)
2. **Backend**: FastAPI Python service (deployed to Railway, Heroku, or Hugging Face Spaces)

## 📋 Prerequisites

- Python 3.11+
- Git repository
- API keys for:
  - Google Gemini AI (`GOOGLE_API_KEY`)
  - SerpAPI (`SERPAPI_KEY`)

## 🎯 Quick Start

### Option 1: Railway (Recommended - Free Tier Available)

1. **Deploy Backend to Railway:**
   ```bash
   # Install Railway CLI
   npm install -g @railway/cli
   
   # Login to Railway
   railway login
   
   # Initialize and deploy
   railway init
   railway up
   ```

2. **Set Environment Variables in Railway Dashboard:**
   - `GOOGLE_API_KEY`: Your Google Gemini API key
   - `SERPAPI_KEY`: Your SerpAPI key

3. **Get your API endpoint** from Railway dashboard (e.g., `https://your-app.railway.app`)

### Option 2: Heroku

1. **Deploy Backend to Heroku:**
   ```bash
   # Install Heroku CLI
   # Create new app
   heroku create your-fake-news-detector
   
   # Set environment variables
   heroku config:set GOOGLE_API_KEY=your_key_here
   heroku config:set SERPAPI_KEY=your_key_here
   
   # Deploy
   git push heroku main
   ```

2. **Get your API endpoint** from Heroku (e.g., `https://your-app.herokuapp.com`)

### Option 3: Hugging Face Spaces

1. **Create a new Space** on Hugging Face
2. **Upload your code** to the Space
3. **Set environment variables** in the Space settings
4. **Deploy** using the Space's built-in deployment

## 🌐 Deploy Frontend to Netlify

1. **Connect your repository:**
   - Go to [Netlify](https://netlify.com)
   - Click "New site from Git"
   - Connect your GitHub/GitLab repository

2. **Build settings:**
   - Build command: `echo "Static site ready"`
   - Publish directory: `.`
   - Branch: `main` (or your default branch)

3. **Update API endpoint:**
   - In the deployed site, update the API endpoint field with your backend URL
   - Or modify `index.html` to use your backend URL by default

## 🔧 Environment Variables

Set these in your backend deployment platform:

```bash
GOOGLE_API_KEY=your_google_gemini_api_key
SERPAPI_KEY=your_serpapi_key
```

## 📁 File Structure

```
fake-news-detector/
├── app.py                 # FastAPI backend
├── index.html            # Frontend (Netlify)
├── requirements.txt      # Python dependencies
├── Procfile             # Heroku deployment
├── railway.json         # Railway configuration
├── Dockerfile           # Docker deployment
├── netlify.toml         # Netlify configuration
├── model/               # ML model files
│   ├── fake_news_model.pkl
│   └── vectorizer.pkl
└── DEPLOYMENT.md        # This file
```

## 🚀 Deployment Commands

### Local Testing
```bash
# Install dependencies
pip install -r requirements.txt

# Run backend locally
python app.py

# Open http://localhost:8000 in browser
```

### Docker Deployment
```bash
# Build image
docker build -t fake-news-detector .

# Run container
docker run -p 8000:8000 fake-news-detector
```

## 🔍 Testing Your Deployment

1. **Test Backend Health:**
   ```bash
   curl https://your-backend-url/health
   ```

2. **Test Analysis Endpoint:**
   ```bash
   curl -X POST https://your-backend-url/analyze \
     -H "Content-Type: application/json" \
     -d '{"text": "test news content"}'
   ```

3. **Test Frontend:**
   - Open your Netlify site
   - Enter test news content
   - Verify API connection works

## 🐛 Troubleshooting

### Common Issues:

1. **Model Loading Errors:**
   - Ensure `model/` directory is included in deployment
   - Check file permissions

2. **API Key Issues:**
   - Verify environment variables are set correctly
   - Check API key validity

3. **CORS Errors:**
   - Backend CORS is configured to allow all origins
   - In production, restrict to your Netlify domain

4. **Memory Issues:**
   - ML models can be memory-intensive
   - Consider using lighter models for production

### Logs and Debugging:

- **Railway:** Check logs in Railway dashboard
- **Heroku:** Use `heroku logs --tail`
- **Local:** Check console output

## 🔒 Security Considerations

1. **API Keys:** Never commit API keys to version control
2. **CORS:** Restrict origins in production
3. **Rate Limiting:** Consider adding rate limiting for production use
4. **Input Validation:** Sanitize user inputs

## 📈 Scaling Considerations

1. **Model Optimization:** Consider model quantization for faster inference
2. **Caching:** Implement Redis for caching frequent requests
3. **Load Balancing:** Use multiple instances for high traffic
4. **CDN:** Serve static assets through CDN

## 🆘 Support

If you encounter issues:

1. Check the logs in your deployment platform
2. Verify environment variables are set correctly
3. Test the backend endpoints directly
4. Check the health endpoint for system status

## 🎉 Success!

Once deployed, your Fake News Detector will be available at:
- **Frontend:** `https://your-site.netlify.app`
- **Backend:** `https://your-backend-url.com`

Update the API endpoint in your frontend to point to your backend, and you're ready to detect fake news! 🧠✨
