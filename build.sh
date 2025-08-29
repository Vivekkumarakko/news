#!/bin/bash

# Exit on any error
set -e

echo "🚀 Starting build process..."

# Set environment variables to avoid Cython compilation issues
export SKLEARN_SKIP_CYTHON=1
export SKLEARN_SKIP_OPENMP=1
export SKLEARN_SKIP_THREADING=1
export SKLEARN_SKIP_AVX2=1
export SKLEARN_SKIP_AVX512=1
export SKLEARN_SKIP_SSE=1
export SKLEARN_SKIP_NEON=1
export SKLEARN_SKIP_ALTIVEC=1
export SKLEARN_SKIP_VSX=1
export SKLEARN_SKIP_AVX=1
export SKLEARN_SKIP_FMA=1
export SKLEARN_SKIP_SSE2=1
export SKLEARN_SKIP_SSE3=1
export SKLEARN_SKIP_SSSE3=1
export SKLEARN_SKIP_SSE41=1
export SKLEARN_SKIP_SSE42=1
export SKLEARN_SKIP_POPCNT=1
export SKLEARN_SKIP_BMI1=1
export SKLEARN_SKIP_BMI2=1
export SKLEARN_SKIP_LZCNT=1
export SKLEARN_SKIP_F16C=1
export SKLEARN_SKIP_FMA4=1
export SKLEARN_SKIP_XOP=1

echo "📦 Installing Python dependencies..."

# Upgrade pip first
python -m pip install --upgrade pip

# Try to install from deployment requirements first (pre-compiled wheels)
echo "🔧 Attempting to install pre-compiled wheels..."
if pip install --no-cache-dir -r requirements-deploy.txt; then
    echo "✅ Successfully installed pre-compiled wheels"
else
    echo "⚠️ Pre-compiled wheels failed, trying regular requirements..."
    # Fallback to regular requirements
    pip install --no-cache-dir -r requirements.txt
fi

echo "✅ Build complete - static site ready!"
