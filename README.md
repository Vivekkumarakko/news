# 🧠 Global Fake News + Reality Checker

A machine learning-powered fake news detection system with AI-powered explanations and cross-referencing capabilities.

## ✨ Features

- **🤖 ML-Powered Detection**: Uses trained machine learning models to classify news as real or fake
- **🔍 AI Explanations**: Gemini AI provides human-like explanations of predictions
- **📰 Headline Cross-Reference**: Compares news with current headlines via SerpAPI
- **🌍 Multi-language Support**: Automatic translation and analysis in multiple languages
- **📊 Confidence Scoring**: Provides confidence levels and probability scores
- **🔬 Model Explainability**: Shows which words/features influenced the prediction
- **📱 Modern Web Interface**: Beautiful, responsive frontend with real-time analysis

## 🏗️ Architecture

- **Frontend**: Static HTML/CSS/JS (deployed to Netlify)
- **Backend**: FastAPI Python service (deployed to Railway/Heroku/Hugging Face)
- **ML Models**: Pre-trained scikit-learn models for fake news detection
- **AI Services**: Google Gemini AI for explanations, SerpAPI for headlines

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/fake-news-detector.git
cd fake-news-detector
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Environment Variables
Create a `.env` file:
```bash
GOOGLE_API_KEY=your_gemini_api_key_here
SERPAPI_KEY=your_serpapi_key_here
```

### 4. Run Locally
```bash
python start.py
```

The API will be available at `http://localhost:8000`

## 🌐 Deployment

### Frontend (Netlify)
1. Push your code to GitHub
2. Connect repository to Netlify
3. Deploy automatically

### Backend (Choose One)

#### Option 1: Railway (Recommended)
```bash
npm install -g @railway/cli
railway login
railway init
railway up
```

#### Option 2: Heroku
```bash
heroku create your-app-name
heroku config:set GOOGLE_API_KEY=your_key
git push heroku main
```

#### Option 3: Hugging Face Spaces
1. Create new Space
2. Upload code
3. Set environment variables
4. Deploy

## 📁 Project Structure

```
fake-news-detector/
├── app.py                 # FastAPI backend
├── start.py              # Local development script
├── index.html            # Frontend interface
├── requirements.txt      # Python dependencies
├── Procfile             # Heroku deployment
├── railway.json         # Railway configuration
├── Dockerfile           # Docker deployment
├── netlify.toml         # Netlify configuration
├── model/               # ML model files
│   ├── fake_news_model.pkl
│   └── vectorizer.pkl
├── DEPLOYMENT.md        # Detailed deployment guide
└── README.md            # This file
```

## 🔧 API Endpoints

- `GET /` - Health check
- `GET /health` - Detailed system status
- `POST /analyze` - Analyze news content

### Example API Usage
```bash
curl -X POST "http://localhost:8000/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Your news content here",
    "useHeadlines": true,
    "useGemini": true
  }'
```

## 🎯 How It Works

1. **Input Processing**: Accepts text, URLs, or file uploads
2. **Text Analysis**: Uses ML models to classify content
3. **Cross-Reference**: Compares with current news headlines
4. **AI Explanation**: Gemini AI provides human-readable insights
5. **Confidence Scoring**: Calculates prediction confidence and similarity scores
6. **Results Display**: Presents comprehensive analysis with explanations

## 🔑 Required API Keys

- **Google Gemini AI**: For AI-powered explanations
- **SerpAPI**: For headline cross-referencing

Both are optional but enhance functionality significantly.

## 🧪 Testing

### Backend Testing
```bash
# Health check
curl http://localhost:8000/health

# Test analysis
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "test content"}'
```

### Frontend Testing
1. Open `index.html` in browser
2. Enter test news content
3. Verify API connection works

## 🐛 Troubleshooting

### Common Issues

1. **Model Loading Errors**
   - Ensure `model/` directory exists with required files
   - Check file permissions

2. **API Key Issues**
   - Verify environment variables are set correctly
   - Check API key validity

3. **CORS Errors**
   - Backend CORS is configured for development
   - Restrict origins in production

4. **Memory Issues**
   - ML models can be memory-intensive
   - Consider using lighter models for production

## 📈 Performance

- **Response Time**: Typically 1-3 seconds for analysis
- **Memory Usage**: ~500MB for ML models
- **Scalability**: Designed for horizontal scaling
- **Caching**: Built-in caching for repeated requests

## 🔒 Security

- Input validation and sanitization
- CORS configuration
- Environment variable protection
- Rate limiting considerations

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Scikit-learn for ML capabilities
- Google Gemini AI for intelligent explanations
- SerpAPI for news headline data
- FastAPI for the robust backend framework

## 📞 Support

For support and questions:
- Check the [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions
- Open an issue on GitHub
- Review the troubleshooting section above

---

**Ready to detect fake news? Deploy your instance and start analyzing! 🚀**
