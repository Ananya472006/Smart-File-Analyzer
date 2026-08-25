import streamlit as st

def get_theme_css(theme_mode="Dark"):
    """
    Returns custom CSS based on the chosen theme mode: 'Dark', 'Light', or 'System'.
    """
    if theme_mode == "Light":
        bg_color = "#f8fafc"
        card_bg = "#ffffff"
        card_border = "#e2e8f0"
        text_primary = "#0f172a"
        text_secondary = "#475569"
        accent_color = "#2563eb"
        shadow_style = "0 4px 15px rgba(0, 0, 0, 0.05)"
    else: # Dark mode / System fallback
        bg_color = "#0f172a"
        card_bg = "rgba(30, 41, 59, 0.7)"
        card_border = "rgba(255, 255, 255, 0.1)"
        text_primary = "#f8fafc"
        text_secondary = "#94a3b8"
        accent_color = "#38bdf8"
        shadow_style = "0 8px 32px 0 rgba(0, 0, 0, 0.37)"

    css = f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Plus Jakarta Sans', sans-serif;
    }}

    /* Top Header Banner */
    .app-header {{
        background: linear-gradient(135deg, #1e1e38 0%, #0f172a 100%);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 16px;
        padding: 24px 30px;
        margin-bottom: 24px;
        box-shadow: {shadow_style};
        position: relative;
        overflow: hidden;
    }}
    .app-header::before {{
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(56, 189, 248, 0.08) 0%, transparent 60%);
        pointer-events: none;
    }}
    .app-title {{
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(90deg, #38bdf8, #818cf8, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        letter-spacing: -0.02em;
    }}
    .app-subtitle {{
        color: #94a3b8;
        font-size: 1.05rem;
        margin-top: 6px;
    }}

    /* Card Styling */
    .feature-card {{
        background: {card_bg};
        border: 1px solid {card_border};
        border-radius: 14px;
        padding: 22px;
        color: {text_primary};
        box-shadow: {shadow_style};
        transition: all 0.3s ease;
        height: 100%;
    }}
    .feature-card:hover {{
        transform: translateY(-4px);
        border-color: {accent_color};
        box-shadow: 0 10px 25px rgba(56, 189, 248, 0.2);
    }}
    .card-icon {{
        font-size: 2rem;
        margin-bottom: 12px;
    }}
    .card-title {{
        font-size: 1.25rem;
        font-weight: 700;
        color: {text_primary};
        margin-bottom: 8px;
    }}
    .card-desc {{
        font-size: 0.92rem;
        color: {text_secondary};
        line-height: 1.5;
    }}

    /* User Profile Badge */
    .user-badge {{
        display: inline-flex;
        align-items: center;
        background: rgba(56, 189, 248, 0.15);
        border: 1px solid rgba(56, 189, 248, 0.3);
        color: #38bdf8;
        padding: 6px 14px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.9rem;
    }}

    /* AI Insight Box */
    .ai-box {{
        background: linear-gradient(135deg, rgba(129, 140, 248, 0.1) 0%, rgba(192, 132, 252, 0.1) 100%);
        border: 1px solid rgba(129, 140, 248, 0.3);
        border-radius: 14px;
        padding: 20px;
        margin: 15px 0;
    }}
    </style>
    """
    return css

def apply_theme(theme_mode="Dark"):
    """Injects CSS for selected theme mode."""
    css = get_theme_css(theme_mode)
    st.markdown(css, unsafe_allow_html=True)
