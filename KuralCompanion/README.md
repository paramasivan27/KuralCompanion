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

# 🌟 KuralCompanion - Ancient Wisdom for Modern Life

A digital sage that listens, understands, and gently guides—through the eternal words of Thiruvalluvar's Thirukkural.

## 🎯 Features

### Enhanced Kural Database
- **Comprehensive Collection**: 110+ Thirukkural verses organized by themes and emotions
- **Modular Structure**: Multiple database files for better organization and scalability
- **Intelligent Matching**: AI-powered emotion and theme detection for relevant verse selection
- **Search Functionality**: Search by theme, keyword, or kural number

### Core Capabilities
- **Emotion-to-Kural Mapping**: Detects emotions and themes from user input
- **Personalized Guidance**: Provides relevant Thirukkural verses with contextual meanings
- **Moral Reflections**: Gentle wisdom for modern life challenges
- **Interactive Interface**: Beautiful, modern UI with intuitive navigation

## 📁 Database Structure

The Kural database is organized into multiple files for better maintainability:

- `kural_database.py` - Main database with core kurals (55 verses)
- `comprehensive_kurals.py` - Additional kurals for extended coverage (22 verses)
- `extended_kurals.py` - Further kurals for maximum coverage (33 verses)

**Total Coverage**: 110 verses (8.3% of the complete 1,330 Thirukkural verses)

### Themes Covered
- Love & Relationships
- Friendship & Loyalty
- Wisdom & Knowledge
- Ethics & Morality
- Leadership & Integrity
- Wealth & Prosperity
- Forgiveness & Compassion
- Patience & Perseverance
- Courage & Strength
- Humility & Modesty
- Gratitude & Thankfulness

## 🚀 Technology Stack

- **Frontend**: Streamlit
- **Backend**: Python
- **AI/ML**: TextBlob for sentiment analysis
- **Data Processing**: Pandas, NumPy
- **Visualization**: Plotly Express
- **UI Components**: Streamlit Option Menu

## 📖 About Thirukkural

Thirukkural is a classic Tamil text consisting of 1,330 couplets dealing with the everyday virtues of an individual. It is one of the most important works in Tamil literature and is considered a masterpiece of ethical literature.

The text is divided into three sections:
- **Aram (Virtue)** - 380 verses on moral values
- **Porul (Wealth)** - 700 verses on political and economic matters  
- **Inbam (Love)** - 250 verses on human love and relationships

## 🛠️ Installation & Usage

### Prerequisites
- Python 3.7+
- pip

### Installation
```bash
# Clone the repository
git clone <repository-url>
cd KuralCompanion

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run src/streamlit_app.py
```

### Usage
1. **Home**: Welcome page with app overview
2. **Ask Kural**: Share your thoughts/emotions and receive relevant wisdom
3. **Explore Themes**: Browse kurals by theme, search by keyword, or find by number
4. **About**: Learn about the app and view database statistics

## 🔧 Database Expansion

To add more kurals to the database:

1. **Add to existing themes**: Edit the appropriate database file
2. **Create new themes**: Add new theme categories with relevant kurals
3. **Maintain structure**: Each kural should include:
   - `number`: Kural number (1-1330)
   - `tamil`: Original Tamil text
   - `transliteration`: Romanized Tamil
   - `english`: English translation
   - `meaning`: Contextual meaning
   - `theme`: Theme category
   - `emotions`: Associated emotions

### Example Kural Structure
```python
{
    "number": 1,
    "tamil": "அகர முதல எழுத்தெல்லாம் ஆதி பகவன் முதற்றே உலகு",
    "transliteration": "Agara mudhala ezhuththellaam aadhi bhagavan mudhatre ulagu",
    "english": "As the letter A is the first of all letters, so the eternal God is first in the world",
    "meaning": "Just as 'A' is the foundation of all letters, God is the foundation of all existence",
    "theme": "divine_love",
    "emotions": ["grateful", "reverent", "contemplative"]
}
```

## 🎨 UI Features

- **Responsive Design**: Works on desktop and mobile devices
- **Beautiful Cards**: Each kural displayed in an elegant card format
- **Emotion Badges**: Visual indicators for detected emotions
- **Interactive Charts**: Database statistics and theme breakdowns
- **Search Interface**: Multiple search options for easy navigation

## 🔮 Future Enhancements

- **Complete Database**: Expand to all 1,330 Thirukkural verses
- **Machine Learning**: Enhanced emotion and theme detection
- **Multi-language Support**: Additional language translations
- **User Profiles**: Personalized kural recommendations
- **Social Features**: Share favorite kurals and insights
- **API Integration**: RESTful API for external applications

## 🤝 Contributing

Contributions are welcome! Please feel free to:
- Add more Thirukkural verses to the database
- Improve emotion and theme detection algorithms
- Enhance the user interface
- Add new features and functionality
- Report bugs and suggest improvements

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- Thiruvalluvar for the timeless wisdom of Thirukkural
- The Tamil literary tradition for preserving this masterpiece
- The open-source community for the tools and libraries used

---

**"Ancient Wisdom for Modern Life"** - Let the eternal words of Thiruvalluvar guide your journey. 