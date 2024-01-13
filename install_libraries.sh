#!/bin/bash

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install required libraries
pip install pandas numpy scikit-learn requests flask nltk selenium

# Download NLTK resources
python -m nltk.downloader punkt stopwords

# Deactivate the virtual environment
deactivate

echo "Libraries installed and configured."
