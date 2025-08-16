---
title: KuralCompanion
emoji: 🌟
colorFrom: purple
colorTo: blue
sdk: docker
app_port: 8501
tags:
- streamlit
- ai
- wisdom
- tamil
- thirukkural
pinned: false
short_description: Ancient Wisdom for Modern Life
---

# KuralCompanion

A Streamlit application that provides intelligent access to the ancient Tamil wisdom of Thirukkural through modern AI-powered search and recommendation systems.

## Features

- **Intelligent Search**: Find relevant kurals using natural language queries
- **Theme-based Organization**: Browse kurals by 133 different themes
- **Emotion Matching**: Discover kurals that match your emotional state
- **Comprehensive Database**: Access to all 1,330 kurals with translations
- **Modern UI**: Beautiful, responsive interface built with Streamlit

## Quick Start

### Local Development

1. Clone the repository:
```bash
git clone https://github.com/yourusername/KuralCompanion.git
cd KuralCompanion
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run src/streamlit_app.py
```

### Docker Deployment

1. Build the Docker image:
```bash
docker build -t kuralcompanion .
```

2. Run the container:
```bash
docker run -p 8501:8501 kuralcompanion
```

### Hugging Face Spaces

The application is also available on Hugging Face Spaces:

[![Hugging Face Spaces](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Spaces-blue)](https://huggingface.co/spaces/yourusername/KuralCompanion)

#### Hugging Face Spaces Configuration

For Hugging Face Spaces deployment, the application uses:
- **Base Image**: `python:3.9-slim`
- **Port**: 8501 (Streamlit default)
- **Health Check**: Automatic health monitoring
- **Dependencies**: All required packages in `requirements.txt`

The Dockerfile is optimized for Hugging Face Spaces and should build successfully without the previous `software-properties-common` dependency issue.

## Project Structure

```
KuralCompanion/
├── src/
│   ├── streamlit_app.py          # Main Streamlit application
│   ├── kural_database.py         # Core database (400 kurals)
│   ├── comprehensive_kurals.py   # Extended database (400 kurals)
│   ├── extended_kurals.py        # Complete database (530 kurals)
│   ├── theme_classifier.py       # Theme classification logic
│   └── thirukkural.json          # Source data
├── Dockerfile                     # Docker configuration
├── requirements.txt               # Python dependencies
└── README.md                     # This file
```

## Database Structure

The application uses three tiered databases:
- **Core Database**: First 400 kurals covering fundamental themes
- **Comprehensive Database**: Next 400 kurals for deeper exploration
- **Extended Database**: Remaining 530 kurals for complete coverage

Each kural includes:
- Tamil text (original)
- English translation
- Detailed explanation
- Theme classification
- Emotional context
- Multiple commentary sources

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the [MIT License](LICENSE).

## Acknowledgments

- Thiruvalluvar for the timeless wisdom of Thirukkural
- The Tamil community for preserving this cultural heritage
- Streamlit for the excellent web application framework
