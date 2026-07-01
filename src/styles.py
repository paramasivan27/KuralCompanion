"""App CSS styles — Burnt Crimson Literature Theme."""


def get_app_css():
    """Return the full CSS string for the app theme."""
    return """
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;0,600;0,700;1,400&family=Libre+Baskerville:ital,wght@0,400;0,700;1,400&family=Noto+Sans+Tamil:wght@300;400;500;600;700&family=Noto+Serif+Tamil:ital,wght@0,400;0,500;0,600;0,700;1,400&display=swap');

    /* ── Burnt Crimson + Parchment Theme Variables ── */
    :root {
        --parchment:     #E8D5A3;
        --parchment-dim: #D9C892;
        --crimson-deep:  #3A0D0D;
        --crimson-darker:#2B0A0A;
        --crimson-mid:   #5C1A1A;
        --crimson-light: #8B3A1A;
        --burnt-gold:    #8B6914;
        --gold:          #B8860B;
        --border:        #C4A870;
        --border-dark:   #8B7040;

        --primary:    var(--crimson-light);
        --accent:     var(--burnt-gold);
        --surface:    var(--parchment-dim);
        --background: var(--parchment);
        --text:       var(--crimson-deep);
        --text-light: var(--crimson-mid);
    }

    /* ── Global base ── */
    .stApp {
        background: var(--parchment) !important;
        color: var(--text) !important;
        font-family: 'EB Garamond', 'Libre Baskerville', Georgia, serif !important;
    }

    /* ── Sidebar ── */
    section[data-testid="stSidebar"] {
        background: var(--crimson-darker) !important;
        border-right: 2px solid var(--border-gold) !important;
    }

    section[data-testid="stSidebar"] * {
        color: #FDF5E6 !important;
        font-family: 'EB Garamond', serif !important;
    }

    /* Sidebar brand heading — gold, more specific than wildcard */
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #D4AF37 !important;
    }

    /* Sidebar subtitle / small text — warm cream */
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] small,
    section[data-testid="stSidebar"] span {
        color: #C9B99A !important;
    }

    /* option_menu inside sidebar */
    section[data-testid="stSidebar"] .nav-link {
        color: #C9B99A !important;
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
        color: var(--crimson-deep) !important;
        margin-bottom: 0.5rem;
        letter-spacing: 0.02em;
        text-shadow: 0 1px 3px rgba(58, 13, 13, 0.2);
    }

    .sub-header {
        font-family: 'Noto Serif Tamil', serif;
        font-size: 1.5rem;
        text-align: center;
        color: var(--crimson-mid);
        margin-bottom: 2rem;
        font-style: italic;
        font-weight: 400;
    }

    /* ── Section divider ── */
    .hr-kolam {
        height: 2px;
        background: linear-gradient(90deg, transparent 0%, var(--border-dark) 40%, var(--burnt-gold) 50%, var(--border-dark) 60%, transparent 100%);
        border: none;
        margin: 2rem 0;
        position: relative;
    }

    .hr-kolam::before {
        content: '✦';
        position: absolute;
        left: 50%; top: 50%;
        transform: translate(-50%, -50%);
        color: var(--burnt-gold);
        font-size: 1.2rem;
        background: var(--parchment);
        padding: 0 1rem;
    }

    /* ── Kural Card — parchment page aesthetic ── */
    .kural-card {
        background: #E8D5A3;
        padding: 2rem 2.5rem;
        border-radius: 4px;
        color: var(--crimson-deep);
        margin: 1.5rem 0;
        border: 1px solid var(--border);
        border-top: 3px solid var(--crimson-light);
        box-shadow:
            0 4px 16px rgba(58, 13, 13, 0.2),
            inset 0 1px 0 rgba(255, 255, 255, 0.4);
        position: relative;
    }

    /* Decorative corner mark */
    .kural-card::after {
        content: '❧';
        position: absolute;
        bottom: 0.8rem; right: 1.2rem;
        color: var(--border-dark);
        font-size: 1rem;
        opacity: 0.5;
    }

    .kural-number {
        font-family: 'EB Garamond', serif;
        font-size: 0.9rem;
        color: var(--crimson-light);
        font-weight: 600;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        margin-bottom: 1rem;
        border-bottom: 1px solid var(--border);
        padding-bottom: 0.5rem;
    }

    .kural-card p {
        color: var(--crimson-deep) !important;
        margin-bottom: 0.8rem;
        line-height: 1.8;
    }

    .kural-card strong {
        color: var(--crimson-mid) !important;
    }

    /* ── Tamil text ── */
    .tamil-text {
        font-family: 'Noto Serif Tamil', serif;
        font-size: 1.15rem;
        line-height: 2;
        color: var(--crimson-deep);
    }

    /* ── Callout blocks (st.info, st.success, st.warning) ── */
    div[data-testid="stInfo"] {
        background: rgba(139, 58, 26, 0.08) !important;
        border-left: 4px solid var(--crimson-light) !important;
        border-radius: 0 4px 4px 0 !important;
        color: var(--crimson-deep) !important;
    }

    div[data-testid="stSuccess"] {
        background: rgba(50, 100, 50, 0.1) !important;
        border-left: 4px solid #3D7A3D !important;
        color: var(--crimson-deep) !important;
    }

    div[data-testid="stWarning"] {
        background: rgba(139, 105, 20, 0.1) !important;
        border-left: 4px solid var(--burnt-gold) !important;
        color: var(--crimson-deep) !important;
    }

    div[data-testid="stError"] {
        background: rgba(139, 20, 20, 0.1) !important;
        border-left: 4px solid #8B1A1A !important;
        color: var(--crimson-deep) !important;
    }

    /* ── Buttons ── */
    .stButton > button {
        background: linear-gradient(135deg, var(--crimson-deep), var(--crimson-mid));
        color: var(--parchment) !important;
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
        background: linear-gradient(135deg, var(--crimson-mid), var(--crimson-light));
        transform: translateY(-1px);
        box-shadow: 0 4px 16px rgba(58, 13, 13, 0.3);
    }

    .stButton > button:active {
        transform: translateY(0);
    }

    /* ── Search / Text inputs ── */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background: var(--parchment-dim) !important;
        color: var(--crimson-deep) !important;
        border: 1px solid var(--border) !important;
        border-radius: 4px !important;
        font-family: 'EB Garamond', serif !important;
        font-size: 1.05rem !important;
        padding: 10px 14px !important;
    }

    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: var(--crimson-light) !important;
        box-shadow: 0 0 0 2px rgba(139, 58, 26, 0.2) !important;
    }

    .stTextInput > div > div > input::placeholder,
    .stTextArea > div > div > textarea::placeholder {
        color: var(--text-light) !important;
    }

    /* ── Selectbox ── */
    .stSelectbox > div > div {
        background: var(--parchment-dim) !important;
        color: var(--crimson-deep) !important;
        border: 1px solid var(--border) !important;
        border-radius: 4px !important;
        font-family: 'EB Garamond', serif !important;
    }

    /* ── Expanders ── */
    details {
        background: var(--parchment-dim) !important;
        border: 1px solid var(--border) !important;
        border-radius: 4px !important;
    }

    summary {
        color: var(--crimson-mid) !important;
        font-family: 'EB Garamond', serif !important;
    }

    summary:hover {
        color: var(--crimson-deep) !important;
    }

    /* ── Tabs ── */
    .stTabs [data-baseweb="tab-list"] {
        background: var(--parchment-dim) !important;
        border-bottom: 2px solid var(--border-dark) !important;
        gap: 0 !important;
    }

    .stTabs [data-baseweb="tab"] {
        background: transparent !important;
        color: var(--crimson-mid) !important;
        border-bottom: 2px solid transparent !important;
        font-family: 'EB Garamond', serif !important;
        font-size: 1.05rem !important;
        padding: 10px 20px !important;
        transition: all 0.2s ease !important;
    }

    .stTabs [data-baseweb="tab"]:hover {
        color: var(--crimson-deep) !important;
    }

    .stTabs [aria-selected="true"] {
        color: var(--crimson-deep) !important;
        border-bottom: 2px solid var(--crimson-light) !important;
        background: rgba(58, 13, 13, 0.07) !important;
    }

    .stTabs [data-baseweb="tab-panel"] {
        background: var(--parchment) !important;
        padding-top: 1rem !important;
    }

    /* ── Radio & Checkbox ── */
    .stRadio label, .stCheckbox label {
        color: var(--crimson-deep) !important;
        font-family: 'EB Garamond', serif !important;
        font-size: 1rem !important;
    }

    /* ── Metrics (About page) ── */
    [data-testid="stMetricValue"] {
        color: var(--crimson-deep) !important;
        font-family: 'EB Garamond', serif !important;
        font-size: 2rem !important;
    }

    [data-testid="stMetricLabel"] {
        color: var(--crimson-mid) !important;
    }

    /* ── Markdown headings ── */
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        font-family: 'EB Garamond', serif !important;
        color: var(--crimson-deep) !important;
    }

    .stMarkdown p, .stMarkdown li {
        color: var(--crimson-deep) !important;
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
        background: var(--parchment-dim);
        border: 1px solid var(--border-dark);
        color: var(--crimson-deep);
    }

    /* ── Tamil quote block ── */
    .tamil-quote {
        font-family: 'Noto Serif Tamil', serif;
        font-size: 1.3rem;
        line-height: 2;
        color: var(--crimson-deep);
        text-align: center;
        margin: 2rem 0;
        padding: 2rem;
        background: var(--parchment-dim);
        border-radius: 4px;
        border: 1px solid var(--border);
        border-top: 3px solid var(--crimson-light);
    }

    /* ── Section header ── */
    .section-header {
        font-family: 'EB Garamond', serif;
        font-size: 2.2rem;
        color: var(--crimson-deep);
        margin: 2rem 0 1rem 0;
        padding-left: 2.5rem;
        position: relative;
    }

    .section-header::before {
        content: '§';
        position: absolute;
        left: 0; top: 0;
        font-size: 1.8rem;
        color: var(--crimson-mid);
        opacity: 0.8;
    }

    /* ── Scrollbar ── */
    ::-webkit-scrollbar { width: 8px; }
    ::-webkit-scrollbar-track { background: var(--parchment-dim); }
    ::-webkit-scrollbar-thumb { background: var(--border-dark); border-radius: 2px; }
    ::-webkit-scrollbar-thumb:hover { background: var(--crimson-mid); }

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
        color: var(--crimson-mid) !important;
        font-style: italic !important;
    }

    /* ── Sidebar collapse button — show << / >> instead of arrow SVG ── */
    /* Hide the default SVG chevron */
    section[data-testid="stSidebar"] button[data-testid="baseButton-headerNoPadding"] svg,
    [data-testid="collapsedControl"] button[data-testid="baseButton-headerNoPadding"] svg {
        display: none !important;
    }

    /* << when sidebar is open (collapse action) */
    section[data-testid="stSidebar"] button[data-testid="baseButton-headerNoPadding"]::after {
        content: '<<';
        color: #D4AF37;
        font-family: 'EB Garamond', serif;
        font-size: 1rem;
        font-weight: bold;
        letter-spacing: -0.1em;
    }

    /* >> when sidebar is collapsed (expand action) */
    [data-testid="collapsedControl"] button[data-testid="baseButton-headerNoPadding"]::after {
        content: '>>';
        color: #D4AF37;
        font-family: 'EB Garamond', serif;
        font-size: 1rem;
        font-weight: bold;
        letter-spacing: -0.1em;
    }
</style>
"""
