from setuptools import setup, find_packages

setup(
    name="fake-news-detector",
    version="1.0.0",
    description="A machine learning-powered fake news detection system",
    author="Your Name",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.104.1",
        "uvicorn[standard]>=0.24.0",
        "scikit-learn>=1.3.2",
        "pandas>=2.1.4",
        "joblib>=1.3.2",
        "requests>=2.31.0",
        "python-dotenv>=1.0.0",
        "google-generativeai>=0.3.2",
        "deep-translator>=1.11.4",
        "beautifulsoup4>=4.12.2",
        "numpy>=1.24.3",
        "scipy>=1.11.4",
        "pydantic>=2.5.0",
    ],
    python_requires=">=3.11,<3.12",
    include_package_data=True,
    zip_safe=False,
)
