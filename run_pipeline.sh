#!/bin/bash

# Activate virtual environment
source venv/bin/activate

# Run scraper to cluster articles
python scraper.py

# Run filter to filter narratives
python filter.py

# Run neutralize.js to summarize narratives using xAI API
# node neutralize.js

# Deactivate virtual environment
deactivate