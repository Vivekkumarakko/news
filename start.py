#!/usr/bin/env python3
"""
Simple startup script for Fake News Detector
Run this to start the FastAPI backend locally
"""

import os
import sys
import uvicorn
from pathlib import Path

def main():
    """Start the FastAPI application"""
    
    # Check if model files exist
    model_dir = Path("model")
    if not model_dir.exists():
        print("❌ Error: 'model' directory not found!")
        print("Please ensure you have the model files in the 'model/' directory:")
        print("  - model/fake_news_model.pkl")
        print("  - model/vectorizer.pkl")
        sys.exit(1)
    
    # Check for required model files
    required_files = ["fake_news_model.pkl", "vectorizer.pkl"]
    missing_files = [f for f in required_files if not (model_dir / f).exists()]
    
    if missing_files:
        print(f"❌ Error: Missing model files: {', '.join(missing_files)}")
        print("Please ensure all model files are present in the 'model/' directory")
        sys.exit(1)
    
    print("✅ Model files found")
    
    # Check environment variables
    env_vars = {
        "GOOGLE_API_KEY": "Google Gemini AI API key (optional)",
        "SERPAPI_KEY": "SerpAPI key for headlines (optional)"
    }
    
    print("\n🔑 Environment Variables:")
    for var, description in env_vars.items():
        value = os.getenv(var)
        if value:
            print(f"  ✅ {var}: {value[:10]}... (set)")
        else:
            print(f"  ⚠️  {var}: Not set ({description})")
    
    # Get port from environment or use default
    port = int(os.getenv("PORT", 8000))
    
    print(f"\n🚀 Starting Fake News Detector API on port {port}")
    print(f"📱 Frontend will be available at: http://localhost:{port}")
    print(f"🔍 API documentation at: http://localhost:{port}/docs")
    print(f"❤️  Health check at: http://localhost:{port}/health")
    print("\nPress Ctrl+C to stop the server")
    
    try:
        uvicorn.run(
            "app:app",
            host="0.0.0.0",
            port=port,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
