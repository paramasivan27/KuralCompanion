"""App CSS styles."""

def get_app_css():
    """Return the full CSS string for the app theme."""
    return """
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;0,600;0,700;1,400&family=Inter:wght@300;400;500;600;700&family=Noto+Sans+Tamil:wght@300;400;500;600;700&family=Noto+Serif+Tamil:ital,wght@0,400;0,500;0,600;0,700;1,400&display=swap');

    /* CSS Custom Properties for Palm Leaf Theme */
    :root {
        --palm-leaf: #DAC7A0;
        --temple-stone: #2B2A28;
        --kumkum-red: #A2322E;
        --turmeric-gold: #D3A014;
        --indigo-ink: #1F3C88;
        --soft-sand: #F5EEDC;
        --primary: var(--palm-leaf);
        --secondary: var(--temple-stone);
        --accent: var(--kumkum-red);
        --accent-secondary: var(--turmeric-gold);
        --link: var(--indigo-ink);
        --surface: var(--soft-sand);
        --text: var(--temple-stone);
        --text-light: #666;
        --background: #ffffff;
    }

    .stApp {
        background: var(--background) !important;
        color: var(--text) !important;
        font-family: 'Inter', sans-serif;
    }

    .main-header {
        font-family: 'EB Garamond', serif;
        font-size: 3.5rem;
        font-weight: 600;
        text-align: center;
        color: var(--primary) !important;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        position: relative;
        transition: color 0.3s ease;
    }

    .sub-header {
        font-family: 'Noto Serif Tamil', serif;
        font-size: 1.8rem;
        text-align: center;
        color: var(--text-light);
        margin-bottom: 2rem;
        font-weight: 400;
    }

    .kural-card {
        background: linear-gradient(135deg, var(--primary) 0%, var(--accent) 100%);
        padding: 2.5rem;
        border-radius: 20px;
        color: white;
        margin: 1.5rem 0;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
        border: 2px solid var(--accent-secondary);
        position: relative;
        overflow: hidden;
    }

    .kural-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="palm" x="0" y="0" width="20" height="20" patternUnits="userSpaceOnUse"><path d="M10 0L12 8L20 10L12 12L10 20L8 12L0 10L8 8Z" fill="white" opacity="0.05"/></pattern></defs><rect width="100" height="100" fill="url(%23palm)"/></svg>');
        opacity: 0.1;
    }

    .hr-kolam {
        height: 2px;
        background: linear-gradient(90deg, transparent 0%, var(--accent) 50%, transparent 100%);
        border: none;
        margin: 2rem 0;
        position: relative;
    }

    .hr-kolam::before {
        content: '•';
        position: absolute;
        left: 50%; top: 50%;
        transform: translate(-50%, -50%);
        color: var(--accent);
        font-size: 1.5rem;
        background: var(--background);
        padding: 0 1rem;
    }

    .theme-badge {
        display: inline-block;
        padding: 0.6rem 1.2rem;
        border-radius: 25px;
        font-weight: 600;
        margin: 0.3rem;
        font-family: 'Inter', sans-serif;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.15);
        transition: all 0.3s ease;
        background: linear-gradient(135deg, #6c5ce7, #5f3dc4);
        color: white;
    }

    .theme-badge:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }

    .tamil-text {
        font-family: 'Noto Serif Tamil', serif;
        font-size: 1.2rem;
        line-height: 1.8;
        color: var(--text);
    }

    .section-header {
        font-family: 'EB Garamond', serif;
        font-size: 2.5rem;
        color: var(--primary);
        margin: 2rem 0 1rem 0;
        position: relative;
        padding-left: 3rem;
    }

    .section-header::before {
        content: '🎵';
        position: absolute;
        left: 0; top: 0;
        font-size: 2rem;
        opacity: 0.7;
    }

    .stTextInput > div > div > input {
        border: 2px solid var(--accent);
        border-radius: 15px;
        padding: 12px 16px;
        font-family: 'Inter', sans-serif;
        background: var(--surface);
        color: var(--text);
    }

    .stTextInput > div > div > input:focus {
        border-color: var(--accent-secondary);
        box-shadow: 0 0 0 3px rgba(211, 160, 20, 0.1);
    }

    .stButton > button {
        background: linear-gradient(135deg, var(--accent), var(--accent-secondary));
        color: white;
        border: none;
        border-radius: 15px;
        padding: 12px 24px;
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.2);
    }

    .css-1d391kg {
        background: var(--surface);
        border-right: 2px solid var(--accent);
    }

    @media (max-width: 768px) {
        .main-header { font-size: 2.5rem; }
        .sub-header { font-size: 1.4rem; }
        .kural-card { padding: 1.5rem; }
    }

    .tamil-quote {
        font-family: 'Noto Serif Tamil', serif;
        font-size: 1.4rem;
        line-height: 2;
        color: var(--primary);
        text-align: center;
        margin: 2rem 0;
        padding: 2rem;
        background: var(--surface);
        border-radius: 15px;
        border-left: 4px solid var(--accent);
    }

    .kural-number {
        font-family: 'EB Garamond', serif;
        font-size: 1.2rem;
        color: var(--accent-secondary);
        font-weight: 600;
        margin-bottom: 0.5rem;
    }

    .explanation-text {
        font-family: 'Inter', sans-serif;
        line-height: 1.7;
        color: var(--text);
        margin: 1rem 0;
    }

    .css-1d391kg .css-1lcbmhc {
        background: var(--surface);
        border-right: 2px solid var(--accent);
    }

    .stMarkdown { color: var(--text); }
    .stText { color: var(--text); }

    ::-webkit-scrollbar { width: 8px; }
    ::-webkit-scrollbar-track { background: var(--surface); }
    ::-webkit-scrollbar-thumb { background: var(--accent); border-radius: 4px; }
    ::-webkit-scrollbar-thumb:hover { background: var(--accent-secondary); }
</style>
"""
