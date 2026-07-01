"""App CSS styles — Burnt Crimson Literature Theme."""


def get_app_css():
    """Return the full CSS string for the app theme."""
    return """
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;0,600;0,700;1,400&family=Libre+Baskerville:ital,wght@0,400;0,700;1,400&family=Noto+Sans+Tamil:wght@300;400;500;600;700&family=Noto+Serif+Tamil:ital,wght@0,400;0,500;0,600;0,700;1,400&display=swap');

    /* ── Burnt Crimson Literature Theme Variables ── */
    :root {
        --gold:          #D4AF37;
        --gold-dark:     #B8860B;
        --gold-light:    #F0D060;
        --crimson-deep:  #3A0D0D;
        --crimson-darker:#2B0A0A;
        --crimson-mid:   #4A1515;
        --crimson-light: #5C1A1A;
        --cream:         #FDF5E6;
        --cream-dim:     #C9B99A;
        --cream-muted:   #9A8A70;
        --border:        #6B2525;
        --border-gold:   #8B6914;

        --primary:    var(--gold);
        --accent:     var(--gold-dark);
        --surface:    var(--crimson-mid);
        --background: var(--crimson-deep);
        --text:       var(--cream);
        --text-light: var(--cream-dim);
    }

    /* ── Global base ── */
    .stApp {
        background: var(--background) !important;
        color: var(--text) !important;
        font-family: 'EB Garamond', 'Libre Baskerville', Georgia, serif !important;
    }

    /* ── Sidebar ── */
    section[data-testid="stSidebar"] {
        background: var(--crimson-darker) !important;
        border-right: 2px solid var(--border-gold) !important;
    }

    section[data-testid="stSidebar"] * {
        color: var(--cream) !important;
        font-family: 'EB Garamond', serif !important;
    }

    /* option_menu inside sidebar */
    section[data-testid="stSidebar"] .nav-link {
        color: var(--cream-dim) !important;
        border-radius: 8px !important;
        font-size: 1.05rem !important;
        transition: all 0.2s ease !important;
    }

    section[data-testid="stSidebar"] .nav-link:hover {
        background: var(--crimson-light) !important;
        color: var(--gold) !important;
    }

    section[data-testid="stSidebar"] .nav-link.active {
        background: linear-gradient(135deg, var(--crimson-light), var(--crimson-mid)) !important;
        color: var(--gold) !important;
        border-left: 3px solid var(--gold) !important;
        font-weight: 600 !important;
    }

    section[data-testid="stSidebar"] .nav-link-selected {
        background: var(--crimson-light) !important;
        color: var(--gold) !important;
    }

    /* ── Main container ── */
    .block-container {
        background: var(--background) !important;
        padding-top: 2rem !important;
    }

    /* ── Page headers ── */
    .main-header {
        font-family: 'EB Garamond', serif;
        font-size: 3.2rem;
        font-weight: 700;
        text-align: center;
        color: var(--gold) !important;
        margin-bottom: 0.5rem;
        letter-spacing: 0.02em;
        text-shadow: 0 2px 8px rgba(212, 175, 55, 0.3);
    }

    .sub-header {
        font-family: 'Noto Serif Tamil', serif;
        font-size: 1.5rem;
        text-align: center;
        color: var(--cream-dim);
        margin-bottom: 2rem;
        font-style: italic;
        font-weight: 400;
    }

    /* ── Section divider ── */
    .hr-kolam {
        height: 2px;
        background: linear-gradient(90deg, transparent 0%, var(--gold-dark) 40%, var(--gold) 50%, var(--gold-dark) 60%, transparent 100%);
        border: none;
        margin: 2rem 0;
        position: relative;
    }

    .hr-kolam::before {
        content: '✦';
        position: absolute;
        left: 50%; top: 50%;
        transform: translate(-50%, -50%);
        color: var(--gold);
        font-size: 1.2rem;
        background: var(--background);
        padding: 0 1rem;
    }

    /* ── Kural Card — book page aesthetic ── */
    .kural-card {
        background: var(--crimson-mid);
        padding: 2rem 2.5rem;
        border-radius: 4px;
        color: var(--cream);
        margin: 1.5rem 0;
        border: 1px solid var(--border);
        border-top: 3px solid var(--gold);
        box-shadow:
            0 4px 20px rgba(0, 0, 0, 0.5),
            inset 0 1px 0 rgba(212, 175, 55, 0.1);
        position: relative;
    }

    /* Decorative corner mark */
    .kural-card::after {
        content: '❧';
        position: absolute;
        bottom: 0.8rem; right: 1.2rem;
        color: var(--border-gold);
        font-size: 1rem;
        opacity: 0.6;
    }

    .kural-number {
        font-family: 'EB Garamond', serif;
        font-size: 0.9rem;
        color: var(--gold);
        font-weight: 600;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        margin-bottom: 1rem;
        border-bottom: 1px solid var(--border);
        padding-bottom: 0.5rem;
    }

    .kural-card p {
        color: var(--cream) !important;
        margin-bottom: 0.8rem;
        line-height: 1.8;
    }

    .kural-card strong {
        color: var(--gold-light) !important;
    }

    /* ── Tamil text ── */
    .tamil-text {
        font-family: 'Noto Serif Tamil', serif;
        font-size: 1.15rem;
        line-height: 2;
        color: var(--cream);
    }

    /* ── Callout blocks (st.info, st.success, st.warning) ── */
    div[data-testid="stInfo"] {
        background: rgba(212, 175, 55, 0.08) !important;
        border-left: 4px solid var(--gold) !important;
        border-radius: 0 4px 4px 0 !important;
        color: var(--cream) !important;
    }

    div[data-testid="stSuccess"] {
        background: rgba(74, 21, 21, 0.6) !important;
        border-left: 4px solid #6DAF6D !important;
        color: var(--cream) !important;
    }

    div[data-testid="stWarning"] {
        background: rgba(90, 50, 10, 0.6) !important;
        border-left: 4px solid var(--gold) !important;
        color: var(--cream) !important;
    }

    div[data-testid="stError"] {
        background: rgba(80, 10, 10, 0.8) !important;
        border-left: 4px solid #CC3333 !important;
        color: var(--cream) !important;
    }

    /* ── Buttons ── */
    .stButton > button {
        background: linear-gradient(135deg, var(--gold-dark), var(--gold));
        color: var(--crimson-darker) !important;
        border: none;
        border-radius: 4px;
        padding: 10px 24px;
        font-family: 'EB Garamond', serif;
        font-weight: 700;
        font-size: 1rem;
        letter-spacing: 0.04em;
        transition: all 0.2s ease;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.4);
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, var(--gold), var(--gold-light));
        transform: translateY(-1px);
        box-shadow: 0 4px 16px rgba(212, 175, 55, 0.3);
    }

    .stButton > button:active {
        transform: translateY(0);
    }

    /* ── Search / Text inputs ── */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background: var(--crimson-mid) !important;
        color: var(--cream) !important;
        border: 1px solid var(--border) !important;
        border-radius: 4px !important;
        font-family: 'EB Garamond', serif !important;
        font-size: 1.05rem !important;
        padding: 10px 14px !important;
    }

    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: var(--gold) !important;
        box-shadow: 0 0 0 2px rgba(212, 175, 55, 0.2) !important;
    }

    .stTextInput > div > div > input::placeholder,
    .stTextArea > div > div > textarea::placeholder {
        color: var(--cream-muted) !important;
    }

    /* ── Selectbox ── */
    .stSelectbox > div > div {
        background: var(--crimson-mid) !important;
        color: var(--cream) !important;
        border: 1px solid var(--border) !important;
        border-radius: 4px !important;
        font-family: 'EB Garamond', serif !important;
    }

    /* ── Expanders ── */
    details {
        background: var(--crimson-mid) !important;
        border: 1px solid var(--border) !important;
        border-radius: 4px !important;
    }

    summary {
        color: var(--cream-dim) !important;
        font-family: 'EB Garamond', serif !important;
    }

    summary:hover {
        color: var(--gold) !important;
    }

    /* ── Tabs ── */
    .stTabs [data-baseweb="tab-list"] {
        background: var(--crimson-darker) !important;
        border-bottom: 2px solid var(--border-gold) !important;
        gap: 0 !important;
    }

    .stTabs [data-baseweb="tab"] {
        background: transparent !important;
        color: var(--cream-dim) !important;
        border-bottom: 2px solid transparent !important;
        font-family: 'EB Garamond', serif !important;
        font-size: 1.05rem !important;
        padding: 10px 20px !important;
        transition: all 0.2s ease !important;
    }

    .stTabs [data-baseweb="tab"]:hover {
        color: var(--gold) !important;
    }

    .stTabs [aria-selected="true"] {
        color: var(--gold) !important;
        border-bottom: 2px solid var(--gold) !important;
        background: rgba(212, 175, 55, 0.07) !important;
    }

    .stTabs [data-baseweb="tab-panel"] {
        background: var(--background) !important;
        padding-top: 1rem !important;
    }

    /* ── Radio & Checkbox ── */
    .stRadio label, .stCheckbox label {
        color: var(--cream) !important;
        font-family: 'EB Garamond', serif !important;
        font-size: 1rem !important;
    }

    /* ── Metrics (About page) ── */
    [data-testid="stMetricValue"] {
        color: var(--gold) !important;
        font-family: 'EB Garamond', serif !important;
        font-size: 2rem !important;
    }

    [data-testid="stMetricLabel"] {
        color: var(--cream-dim) !important;
    }

    /* ── Markdown headings ── */
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        font-family: 'EB Garamond', serif !important;
        color: var(--gold) !important;
    }

    .stMarkdown p, .stMarkdown li {
        color: var(--cream) !important;
        line-height: 1.8 !important;
        font-family: 'EB Garamond', serif !important;
        font-size: 1.05rem !important;
    }

    /* ── Theme badges ── */
    .theme-badge {
        display: inline-block;
        padding: 0.4rem 1rem;
        border-radius: 2px;
        font-weight: 600;
        margin: 0.3rem;
        font-family: 'EB Garamond', serif;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        background: var(--crimson-light);
        border: 1px solid var(--gold-dark);
        color: var(--gold-light);
    }

    /* ── Tamil quote block ── */
    .tamil-quote {
        font-family: 'Noto Serif Tamil', serif;
        font-size: 1.3rem;
        line-height: 2;
        color: var(--cream);
        text-align: center;
        margin: 2rem 0;
        padding: 2rem;
        background: var(--crimson-mid);
        border-radius: 4px;
        border: 1px solid var(--border);
        border-top: 3px solid var(--gold);
    }

    /* ── Section header ── */
    .section-header {
        font-family: 'EB Garamond', serif;
        font-size: 2.2rem;
        color: var(--gold);
        margin: 2rem 0 1rem 0;
        padding-left: 2.5rem;
        position: relative;
    }

    .section-header::before {
        content: '§';
        position: absolute;
        left: 0; top: 0;
        font-size: 1.8rem;
        color: var(--gold-dark);
        opacity: 0.8;
    }

    /* ── Scrollbar ── */
    ::-webkit-scrollbar { width: 8px; }
    ::-webkit-scrollbar-track { background: var(--crimson-darker); }
    ::-webkit-scrollbar-thumb { background: var(--border-gold); border-radius: 2px; }
    ::-webkit-scrollbar-thumb:hover { background: var(--gold); }

    /* ── Responsive ── */
    @media (max-width: 768px) {
        .main-header { font-size: 2.2rem; }
        .sub-header { font-size: 1.2rem; }
        .kural-card { padding: 1.2rem 1.5rem; }
    }

    /* ── Spinner ── */
    .stSpinner > div {
        border-top-color: var(--gold) !important;
    }

    /* ── Caption text ── */
    .stCaption, caption {
        color: var(--cream-muted) !important;
        font-style: italic !important;
    }
</style>
"""
