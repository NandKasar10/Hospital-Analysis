---
title: Hospital Department Load Analysis
emoji: 🏥
colorFrom: blue
colorTo: green
sdk: gradio
app_file: app.py
pinned: false

---

# 🏥 Hospital Department Load Analysis

A Pandas + Gradio app to analyze patient counts per hospital department, visualize with bar charts, and generate a stats report.  
Deployed on Hugging Face Spaces.

## Features
- Upload hospital visit data in CSV format
- Compute patient counts per department
- Visualize results with interactive bar charts
- Generate a concise stats report

## Quick Start (Local)
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python app.py