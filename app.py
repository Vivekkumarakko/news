from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import os
import sys
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Graceful imports with fallbacks
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
    logger.info("✅ Gemini AI available")
except ImportError:
    GEMINI_AVAILABLE = False
    genai = None
    logger.warning("⚠️ Gemini AI not available")

try:
    import requests
    REQUESTS_AVAILABLE = True
    logger.info("✅ Requests library available")
except ImportError:
    REQUESTS_AVAILABLE = False
    requests = None
    logger.warning("⚠️ Requests library not available")

try:
    from deep_translator import GoogleTranslator
    TRANSLATOR_AVAILABLE = True
    logger.info("✅ Translator available")
except ImportError:
    TRANSLATOR_AVAILABLE = False
    GoogleTranslator = None
    logger.warning("⚠️ Translator not available")

try:
    from bs4 import BeautifulSoup
    BS4_AVAILABLE = True
    logger.info("✅ BeautifulSoup available")
except ImportError:
    BS4_AVAILABLE = False
    BeautifulSoup = None
    logger.warning("⚠️ BeautifulSoup not available")

from functools import lru_cache
from urllib.parse import urlparse, parse_qs

# Environment variable checks with defaults
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
SERPAPI_KEY = os.getenv("SERPAPI_KEY")

# Model loading with error handling
try:
    model = joblib.load("model/fake_news_model.pkl")
    vectorizer = joblib.load("model/vectorizer.pkl")
    MODEL_LOADED = True
    logger.info("✅ ML model loaded successfully")
except Exception as e:
    logger.error(f"❌ Failed to load model files: {e}")
    MODEL_LOADED = False
    model = None
    vectorizer = None

# Gemini setup with fallback
if GEMINI_AVAILABLE and GOOGLE_API_KEY:
    try:
        genai.configure(api_key=GOOGLE_API_KEY)
        gemini = genai.GenerativeModel("gemini-1.5-flash")
        GEMINI_READY = True
        logger.info("✅ Gemini AI configured successfully")
    except Exception as e:
        logger.error(f"❌ Gemini setup failed: {e}")
        GEMINI_READY = False
        gemini = None
else:
    GEMINI_READY = False
    gemini = None
    if not GOOGLE_API_KEY:
        logger.warning("⚠️ No GOOGLE_API_KEY provided")

# Class labels for UI controls
try:
    if MODEL_LOADED and hasattr(model, "classes_"):
        CLASS_LABELS = [str(c) for c in model.classes_]
        if len(CLASS_LABELS) < 2:
            CLASS_LABELS = ["FAKE", "REAL"]
    else:
        CLASS_LABELS = ["FAKE", "REAL"]
except Exception:
    CLASS_LABELS = ["FAKE", "REAL"]

# FastAPI app
app = FastAPI(
    title="Fake News Detector API",
    description="API for detecting fake news using machine learning",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this to your Netlify domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class NewsAnalysisRequest(BaseModel):
    text: str = ""
    url: str = ""
    useHeadlines: bool = True
    useGemini: bool = True
    margin: float = 0.5
    simWeight: float = 0.5
    positiveLabel: str = "REAL"
    probThreshold: float = 0.6
    disableTranslation: bool = False

class NewsAnalysisResponse(BaseModel):
    success: bool
    result: list
    model_loaded: bool
    gemini_ready: bool
    error: str = None

@lru_cache(maxsize=256)
def safe_fetch_headlines(query):
    """Safe headline fetching with comprehensive error handling"""
    if not query or not query.strip():
        return "(No query provided)"
        
    if not REQUESTS_AVAILABLE:
        return "(Headlines unavailable: requests library not available)"
        
    if not SERPAPI_KEY:
        return "(Headlines unavailable: missing SERPAPI_KEY environment variable)"
        
    try:
        url = f"https://serpapi.com/search.json?q={requests.utils.quote(query)}&tbm=nws&api_key={SERPAPI_KEY}"
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        data = r.json()
        articles = data.get("news_results", [])[:5]
        return "\n".join([f"- {a.get('title', 'Untitled')}" for a in articles]) if articles else "(No matching headlines)"
    except requests.exceptions.Timeout:
        return "(Headlines unavailable: request timeout)"
    except requests.exceptions.RequestException as e:
        return f"(Headlines unavailable: network error - {str(e)})"
    except Exception as exc:
        return f"(Headlines unavailable: {str(exc)})"

def safe_extract_url_text(url):
    """Safe URL text extraction with error handling"""
    if not url or not url.strip():
        return ""
        
    if not REQUESTS_AVAILABLE:
        return "(Install requests library for URL scraping)"
        
    if not BS4_AVAILABLE:
        return "(Install beautifulsoup4 for URL scraping)"
        
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        title = soup.title.get_text(strip=True) if soup.title else ""
        paras = [p.get_text(" ", strip=True) for p in soup.find_all("p")]
        body = " ".join(paras)
        combined = (title + "\n\n" + body).strip()
        return combined[:8000] if combined else "⚠️ No text extracted from URL"
    except requests.exceptions.Timeout:
        return "❌ URL fetch timeout"
    except requests.exceptions.RequestException as e:
        return f"❌ URL fetch error: {str(e)}"
    except Exception as exc:
        return f"❌ URL processing error: {str(exc)}"

def safe_explain_prediction(vect, top_k=10):
    """Safe prediction explanation with error handling"""
    if not MODEL_LOADED or not vectorizer:
        return "(Explainability unavailable: model not loaded)"
        
    try:
        coef = getattr(model, "coef_", None)
        feature_names = getattr(vectorizer, "get_feature_names_out", None)
        
        if coef is None or feature_names is None:
            return "(Explainability unavailable for this model type)"
            
        names = vectorizer.get_feature_names_out()
        dense = vect.toarray()[0]
        weights = coef[0]
        contributions = dense * weights
        top_idx = contributions.argsort()[-top_k:][::-1]
        items = [f"{names[i]}: {contributions[i]:.3f}" for i in top_idx if dense[i] != 0.0]
        return "Top contributing terms:\n" + ("\n".join(items) if items else "(No strong token contributions detected)")
        
    except Exception as exc:
        return f"(Explainability error: {str(exc)})"

def safe_analyze_news(text, use_headlines=True, use_gemini=True, margin=0.5, sim_weight=0.5, positive_label=None, prob_threshold=0.6, disable_translation=False):
    """Safe news analysis with comprehensive error handling"""
    if not text or not text.strip():
        return "⚠️ Please enter news content.", "", "", "", "", ""
        
    if not MODEL_LOADED:
        return "❌ Model not available. Check model files.", "", "", "", "", ""
        
    try:
        # Translation
        if disable_translation or not TRANSLATOR_AVAILABLE:
            translated = text
        else:
            try:
                translated = GoogleTranslator(source="auto", target="en").translate(text)
            except Exception:
                translated = text

        # Vectorization
        try:
            vect = vectorizer.transform([translated])
        except Exception as e:
            return f"❌ Text processing error: {str(e)}", "", "", "", "", ""

        # Prediction
        try:
            raw_score = float(model.decision_function(vect)[0])
            pred = model.predict(vect)[0]
            raw_conf = abs(round(raw_score, 2))
        except Exception as e:
            return f"❌ Prediction error: {str(e)}", "", "", "", "", ""

        # Headlines
        headlines = safe_fetch_headlines(" ".join(translated.split()[:5])) if use_headlines else "(Headlines disabled)"

        # Similarity calculation
        sim_value = None
        if use_headlines and headlines and not headlines.startswith("("):
            try:
                clean_headlines = headlines.replace("- ", " ")
                h_vec = vectorizer.transform([clean_headlines])
                a = vect.toarray()[0]
                b = h_vec.toarray()[0]
                a_norm = (a @ a) ** 0.5
                b_norm = (b @ b) ** 0.5
                if a_norm > 0 and b_norm > 0:
                    sim_value = float((a @ b) / (a_norm * b_norm))
                else:
                    sim_value = 0.0
            except Exception:
                sim_value = None

        # Score adjustment
        factor = 1.0
        if sim_value is not None:
            sim_clamped = max(0.0, min(1.0, sim_value))
            factor = 1.0 - float(sim_weight) * (1.0 - sim_clamped)
        adjusted_score = raw_score * factor
        adjusted_conf = abs(round(adjusted_score, 2))

        # Probability computation
        try:
            model_classes = [str(c) for c in getattr(model, "classes_", ["FAKE", "REAL"])]
            pos_label = positive_label or (model_classes[1] if len(model_classes) > 1 else model_classes[0])
            
            if hasattr(model, "predict_proba"):
                proba = model.predict_proba(vect)[0]
                pos_index = model_classes.index(pos_label) if pos_label in model_classes else 1
                prob_raw = float(proba[pos_index])
            else:
                import math
                sigmoid = 1.0 / (1.0 + math.exp(-raw_score))
                if pos_label == (model_classes[1] if len(model_classes) > 1 else model_classes[0]):
                    prob_raw = float(sigmoid)
                else:
                    prob_raw = float(1.0 - sigmoid)
                    
            sigmoid_adj = 1.0 / (1.0 + math.exp(-adjusted_score))
            if pos_label == (model_classes[1] if len(model_classes) > 1 else model_classes[0]):
                prob_adj = float(sigmoid_adj)
            else:
                prob_adj = float(1.0 - sigmoid_adj)
                
        except Exception:
            prob_raw = None
            prob_adj = None

        # Final decision
        final_label = pred
        model_classes = [str(c) for c in getattr(model, "classes_", ["FAKE", "REAL"])]
        other_label = model_classes[0] if (positive_label or (len(model_classes) > 1 and model_classes[1])) != model_classes[0] else (model_classes[1] if len(model_classes) > 1 else model_classes[0])
        chosen_positive = (positive_label or (model_classes[1] if len(model_classes) > 1 else model_classes[0]))
        
        if prob_adj is not None:
            final_label = chosen_positive if prob_adj >= float(prob_threshold) else other_label
        else:
            final_label = chosen_positive if adjusted_score >= 0 else other_label
            
        if abs(adjusted_score) < float(margin):
            final_label = "UNSURE"

        # Gemini response
        if use_gemini and GEMINI_READY:
            try:
                prompt = f"User News:\n{translated}\n\nTop Headlines:\n{headlines}\n\nDoes this match? Explain clearly."
                gemini_response = gemini.generate_content(prompt).text
            except Exception as e:
                gemini_response = f"❌ Gemini Error: {str(e)}"
        else:
            gemini_response = "(Gemini disabled or unavailable)"

        # Explanation
        explanation = safe_explain_prediction(vect)

        return (
            f"🧠 Prediction: {final_label}",
            (
                f"📊 Confidence (raw/adj): {raw_conf} / {adjusted_conf}" +
                (f" | Prob (raw/adj): {prob_raw:.2f}/{prob_adj:.2f} | thr={float(prob_threshold):.2f}" if (prob_raw is not None and prob_adj is not None) else "")
            ),
            f"📰 Headlines:\n{headlines}",
            f"🤖 Gemini Insight:\n{gemini_response}",
            explanation,
            (f"Cosine similarity: {sim_value:.3f}" if sim_value is not None else "Cosine similarity: N/A"),
        )
        
    except Exception as exc:
        return f"❌ Analysis error: {str(exc)}", "", "", "", "", ""

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "Fake News Detector API",
        "status": "running",
        "model_loaded": MODEL_LOADED,
        "gemini_ready": GEMINI_READY,
        "version": "1.0.0"
    }

@app.post("/analyze", response_model=NewsAnalysisResponse)
async def analyze_news(request: NewsAnalysisRequest):
    """Analyze news content for fake news detection"""
    try:
        # Get text from URL if provided
        text = request.text
        if request.url and not text:
            text = safe_extract_url_text(request.url)
        
        if not text:
            raise HTTPException(status_code=400, detail="No text content provided")
        
        # Analyze the news
        result = safe_analyze_news(
            text=text,
            use_headlines=request.useHeadlines,
            use_gemini=request.useGemini,
            margin=request.margin,
            sim_weight=request.simWeight,
            positive_label=request.positiveLabel,
            prob_threshold=request.probThreshold,
            disable_translation=request.disableTranslation
        )
        
        return NewsAnalysisResponse(
            success=True,
            result=result,
            model_loaded=MODEL_LOADED,
            gemini_ready=GEMINI_READY
        )
        
    except Exception as e:
        logger.error(f"Error in analyze_news: {str(e)}")
        return NewsAnalysisResponse(
            success=False,
            result=[],
            model_loaded=MODEL_LOADED,
            gemini_ready=GEMINI_READY,
            error=str(e)
        )

@app.get("/health")
async def health_check():
    """Detailed health check endpoint"""
    return {
        "status": "healthy",
        "model_loaded": MODEL_LOADED,
        "gemini_ready": GEMINI_READY,
        "requests_available": REQUESTS_AVAILABLE,
        "translator_available": TRANSLATOR_AVAILABLE,
        "bs4_available": BS4_AVAILABLE,
        "google_api_key": bool(GOOGLE_API_KEY),
        "serpapi_key": bool(SERPAPI_KEY)
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
