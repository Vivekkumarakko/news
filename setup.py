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
        "scikit-learn>=1.2.2",
        "pandas>=1.5.3",
        "joblib>=1.2.0",
        "requests>=2.28.2",
        "python-dotenv>=1.0.0",
        "google-generativeai>=0.3.2",
        "deep-translator>=1.11.4",
        "beautifulsoup4>=4.11.2",
        "numpy>=1.23.5",
        "scipy>=1.10.1",
        "pydantic>=1.10.12",
    ],
    python_requires=">=3.9,<3.10",
    include_package_data=True,
    zip_safe=False,
)
