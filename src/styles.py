"""
CSS styling module for SwarSatya Public Safety UI Prototype.
Enforces Indian public-sector portal visual identity (Navy #0B3A66, Green #138808, Saffron #E77817).
System font stack: Arial, Helvetica, sans-serif.
"""

def get_custom_css(font_scale: str = "normal") -> str:
    """
    Generate custom CSS string based on accessibility font_scale choice:
    - 'small' (A-)
    - 'normal' (A)
    - 'large' (A+)
    """
    base_font_size = "14px"
    h1_size = "26px"
    h2_size = "20px"
    h3_size = "16px"

    if font_scale == "small":
        base_font_size = "12px"
        h1_size = "22px"
        h2_size = "18px"
        h3_size = "14px"
    elif font_scale == "large":
        base_font_size = "16px"
        h1_size = "30px"
        h2_size = "24px"
        h3_size = "18px"

    return f"""
    <style>
        /* Base page styling */
        html, body, [data-testid="stAppViewContainer"] {{
            background-color: #F4F7FA !important;
            color: #1F2937 !important;
            font-family: Arial, Helvetica, sans-serif !important;
            font-size: {base_font_size} !important;
        }}

        /* Center container max-width 1280px */
        .main .block-container {{
            max-width: 1280px !important;
            padding-top: 0rem !important;
            padding-bottom: 2rem !important;
            padding-left: 1.5rem !important;
            padding-right: 1.5rem !important;
        }}

        /* Hide Streamlit default header and footer elements */
        header[data-testid="stHeader"] {{
            visibility: hidden;
            height: 0px;
        }}
        footer {{
            visibility: hidden;
        }}

        /* Typography */
        h1 {{
            font-size: {h1_size} !important;
            font-weight: 700 !important;
            color: #0B3A66 !important;
            margin-bottom: 0.5rem !important;
            font-family: Arial, Helvetica, sans-serif !important;
        }}
        h2 {{
            font-size: {h2_size} !important;
            font-weight: 700 !important;
            color: #0B3A66 !important;
            margin-top: 1rem !important;
            margin-bottom: 0.5rem !important;
            font-family: Arial, Helvetica, sans-serif !important;
        }}
        h3 {{
            font-size: {h3_size} !important;
            font-weight: 600 !important;
            color: #0B3A66 !important;
            margin-top: 0.75rem !important;
            font-family: Arial, Helvetica, sans-serif !important;
        }}

        /* Top Accessibility Bar */
        .access-bar {{
            background-color: #0B3A66;
            color: #FFFFFF;
            padding: 6px 16px;
            font-size: 12px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 2px solid #E77817;
            margin-left: -1.5rem;
            margin-right: -1.5rem;
            margin-top: 0;
        }}
        .access-bar-left {{
            font-weight: bold;
            letter-spacing: 0.3px;
        }}
        .access-bar-right {{
            display: flex;
            gap: 12px;
            align-items: center;
        }}
        .access-btn {{
            color: #FFFFFF;
            text-decoration: none;
            background: rgba(255, 255, 255, 0.15);
            padding: 2px 8px;
            border-radius: 3px;
            font-weight: bold;
            cursor: pointer;
        }}

        /* Main Masthead */
        .masthead-container {{
            background-color: #FFFFFF;
            border-bottom: 1px solid #D8E1EA;
            padding: 16px 20px;
            margin-left: -1.5rem;
            margin-right: -1.5rem;
            margin-bottom: 0px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .masthead-brand {{
            display: flex;
            align-items: center;
            gap: 14px;
        }}
        .shield-mark {{
            font-size: 34px;
            line-height: 1;
            background: #0B3A66;
            color: #FFFFFF;
            padding: 8px 12px;
            border-radius: 6px;
            border-bottom: 3px solid #E77817;
        }}
        .brand-title-box {{
            display: flex;
            flex-direction: column;
        }}
        .brand-name {{
            font-size: 24px;
            font-weight: 800;
            color: #0B3A66;
            line-height: 1.1;
            letter-spacing: -0.5px;
        }}
        .brand-hindi {{
            font-size: 16px;
            font-weight: 600;
            color: #E77817;
        }}
        .brand-tagline {{
            font-size: 12px;
            color: #64748B;
            margin-top: 2px;
        }}
        .masthead-status {{
            text-align: right;
            background-color: #F4F7FA;
            padding: 8px 14px;
            border-radius: 6px;
            border: 1px solid #D8E1EA;
        }}
        .status-pill {{
            color: #138808;
            font-weight: bold;
            font-size: 12px;
            display: inline-block;
        }}
        .status-caption {{
            font-size: 11px;
            color: #64748B;
            margin-top: 2px;
        }}

        /* Horizontal Menu Navigation Bar */
        .nav-container {{
            background-color: #0B3A66;
            margin-left: -1.5rem;
            margin-right: -1.5rem;
            margin-bottom: 16px;
            padding: 0px 20px;
            display: flex;
            gap: 4px;
            border-top: 1px solid rgba(255,255,255,0.1);
        }}

        /* Breadcrumb Bar */
        .breadcrumb-bar {{
            font-size: 12px;
            color: #64748B;
            margin-bottom: 16px;
            padding: 6px 12px;
            background-color: #FFFFFF;
            border: 1px solid #D8E1EA;
            border-radius: 4px;
        }}
        .breadcrumb-bar span {{
            color: #0B3A66;
            font-weight: bold;
        }}

        /* Formal Cards */
        .gov-card {{
            background-color: #FFFFFF;
            border: 1px solid #D8E1EA;
            border-radius: 6px;
            padding: 20px;
            margin-bottom: 16px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.04);
        }}
        .gov-card-title {{
            font-size: 16px;
            font-weight: bold;
            color: #0B3A66;
            margin-bottom: 10px;
            border-bottom: 2px solid #F4F7FA;
            padding-bottom: 6px;
        }}

        /* Custom Alert Boxes */
        .alert-saffron {{
            background-color: #FFFBEB;
            border-left: 5px solid #E77817;
            border-top: 1px solid #FDE68A;
            border-right: 1px solid #FDE68A;
            border-bottom: 1px solid #FDE68A;
            padding: 14px 18px;
            border-radius: 4px;
            margin-bottom: 16px;
            color: #92400E;
            font-size: 13px;
        }}
        .alert-blue {{
            background-color: #EFF6FF;
            border-left: 5px solid #1D4ED8;
            border-top: 1px solid #BFDBFE;
            border-right: 1px solid #BFDBFE;
            border-bottom: 1px solid #BFDBFE;
            padding: 14px 18px;
            border-radius: 4px;
            margin-bottom: 16px;
            color: #1E40AF;
            font-size: 13px;
        }}
        .alert-safe {{
            background-color: #F0FDF4;
            border-left: 5px solid #15803D;
            border-top: 1px solid #BBF7D0;
            border-right: 1px solid #BBF7D0;
            border-bottom: 1px solid #BBF7D0;
            padding: 16px 20px;
            border-radius: 4px;
            margin-bottom: 16px;
            color: #166534;
        }}
        .alert-warning {{
            background-color: #FFFBEB;
            border-left: 5px solid #B45309;
            border-top: 1px solid #FDE68A;
            border-right: 1px solid #FDE68A;
            border-bottom: 1px solid #FDE68A;
            padding: 16px 20px;
            border-radius: 4px;
            margin-bottom: 16px;
            color: #92400E;
        }}
        .alert-critical {{
            background-color: #FEF2F2;
            border-left: 5px solid #B91C1C;
            border-top: 1px solid #FCA5A5;
            border-right: 1px solid #FCA5A5;
            border-bottom: 1px solid #FCA5A5;
            padding: 16px 20px;
            border-radius: 4px;
            margin-bottom: 16px;
            color: #991B1B;
        }}

        /* Trust Strip */
        .trust-strip {{
            background-color: #E2E8F0;
            border: 1px solid #CBD5E1;
            padding: 12px 20px;
            border-radius: 6px;
            display: flex;
            justify-content: space-around;
            align-items: center;
            margin-top: 24px;
            margin-bottom: 24px;
        }}
        .trust-item {{
            font-size: 12px;
            font-weight: bold;
            color: #334155;
        }}

        /* Metric Box Container */
        .metric-card-gov {{
            background: #FFFFFF;
            border: 1px solid #D8E1EA;
            border-radius: 6px;
            padding: 14px;
            text-align: center;
        }}
        .metric-card-label {{
            font-size: 12px;
            color: #64748B;
            font-weight: bold;
        }}
        .metric-card-val {{
            font-size: 24px;
            font-weight: 800;
            color: #0B3A66;
            margin: 4px 0;
        }}
        .metric-card-cap {{
            font-size: 11px;
            color: #475569;
        }}

        /* Footer */
        .gov-footer {{
            background-color: #FFFFFF;
            border-top: 3px solid #0B3A66;
            padding: 20px 24px;
            margin-left: -1.5rem;
            margin-right: -1.5rem;
            margin-top: 32px;
            text-align: center;
            font-size: 12px;
            color: #64748B;
        }}
        .gov-footer-links {{
            margin-top: 8px;
            font-weight: bold;
            color: #0B3A66;
        }}
        .gov-footer-links span {{
            margin: 0 8px;
            color: #94A3B8;
        }}

        /* Button override styling */
        div.stButton > button {{
            border-radius: 4px !important;
            font-family: Arial, Helvetica, sans-serif !important;
            font-weight: bold !important;
        }}
    </style>
    """
