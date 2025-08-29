#!/bin/bash

# Simple Netlify build script
echo "🚀 Starting Netlify build..."

# Set environment variables to avoid Cython compilation
export SKLEARN_SKIP_CYTHON=1
export SKLEARN_SKIP_OPENMP=1
export SKLEARN_SKIP_THREADING=1
export SKLEARN_SKIP_AVX2=1
export SKLEARN_SKIP_AVX512=1
export SKLEARN_SKIP_SSE=1

echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

echo "✅ Build complete - static site ready!"
