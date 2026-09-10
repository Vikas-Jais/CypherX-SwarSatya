"""
Reusable UI component builders for SwarSatya Public Safety Portal UI.
Includes accessibility header bar, main masthead, horizontal navigation bar,
breadcrumbs, cards, metric boxes, alerts, indicator bars, and footer.
"""

import streamlit as st
from typing import List, Dict, Any

# ------------------------------------------------------------------------------
# 1. ACCESSIBILITY TOP BAR
# ------------------------------------------------------------------------------
def render_accessibility_bar() -> None:
    """Render slim navy top accessibility bar with font scale & language controls."""
    col_left, col_right = st.columns([3, 2])

    with col_left:
        st.markdown(
            '<div style="background-color:#0B3A66; color:#FFFFFF; padding:6px 14px; border-bottom:2px solid #E77817; font-size:12px; font-weight:bold; font-family:Arial, sans-serif;">'
            'SwarSatya Public Safety Prototype | Smart India Hackathon 2026'
            '</div>',
            unsafe_allow_html=True
        )

    with col_right:
        # Font size adjustment buttons
        f_cols = st.columns([2, 1, 1, 1, 3])
        with f_cols[0]:
            st.markdown('<span style="font-size:11px; color:#FFFFFF; font-family:Arial;">Skip to main content</span>', unsafe_allow_html=True)
        with f_cols[1]:
            if st.button("A-", key="btn_font_small", help="Decrease font size"):
                st.session_state["font_scale"] = "small"
                st.rerun()
        with f_cols[2]:
            if st.button("A", key="btn_font_normal", help="Reset font size"):
                st.session_state["font_scale"] = "normal"
                st.rerun()
        with f_cols[3]:
            if st.button("A+", key="btn_font_large", help="Increase font size"):
                st.session_state["font_scale"] = "large"
                st.rerun()
        with f_cols[4]:
            st.markdown('<span style="font-size:11px; color:#E77817; font-weight:bold; font-family:Arial;">English | हिंदी</span>', unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# 2. MAIN MASTHEAD
# ------------------------------------------------------------------------------
def render_masthead() -> None:
    """Render two-column white header masthead with shield mark & local status badge."""
    col_left, col_right = st.columns([3, 1])

    with col_left:
        st.markdown(
            """
            <div style="display:flex; align-items:center; gap:14px; background-color:#FFFFFF; padding:12px 16px; border-radius:6px; border:1px solid #D8E1EA; margin-bottom:12px;">
                <div style="font-size:32px; background:#0B3A66; color:#FFFFFF; padding:6px 12px; border-radius:6px; border-bottom:3px solid #E77817; font-family:Arial;">
                    🛡️
                </div>
                <div style="display:flex; flex-direction:column;">
                    <div style="display:flex; align-items:baseline; gap:8px;">
                        <span style="font-size:24px; font-weight:800; color:#0B3A66; font-family:Arial;">SwarSatya</span>
                        <span style="font-size:18px; font-weight:600; color:#E77817; font-family:Arial;">स्वरसत्य</span>
                    </div>
                    <div style="font-size:13px; color:#64748B; font-weight:bold; font-family:Arial;">
                        सत्य की आवाज़ — The Voice of Truth
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col_right:
        st.markdown(
            """
            <div style="background-color:#F4F7FA; padding:10px 14px; border-radius:6px; border:1px solid #D8E1EA; text-align:right; margin-bottom:12px;">
                <div style="color:#138808; font-weight:bold; font-size:12px; font-family:Arial;">
                    ● LOCAL DEMO SYSTEM ACTIVE
                </div>
                <div style="font-size:11px; color:#64748B; font-family:Arial;">
                    Privacy-conscious simulated audio analysis
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

# ------------------------------------------------------------------------------
# 3. HORIZONTAL MENU NAVIGATION
# ------------------------------------------------------------------------------
def render_navigation() -> str:
    """Render horizontal navigation menu bar with active orange underline."""
    pages = [
        "Home",
        "Live Voice Scan",
        "Incident Register",
        "Threat Insights",
        "How It Works",
        "Help & Safety"
    ]

    if "current_page" not in st.session_state:
        st.session_state["current_page"] = "Home"

    cols = st.columns(len(pages))
    for i, page_name in enumerate(pages):
        is_active = (st.session_state["current_page"] == page_name)
        
        btn_label = f"▸ {page_name}" if is_active else page_name
        with cols[i]:
            if st.button(btn_label, key=f"nav_btn_{i}", use_container_width=True):
                st.session_state["current_page"] = page_name
                st.rerun()

    active_idx = pages.index(st.session_state["current_page"])
    underline_html = f"""
    <div style="background-color:#0B3A66; height:4px; margin-top:-6px; margin-bottom:16px; border-radius:2px; display:flex;">
        <div style="width:{active_idx * (100 / len(pages))}%;"></div>
        <div style="width:{100 / len(pages)}%; background-color:#E77817; height:4px; border-radius:2px;"></div>
    </div>
    """
    st.markdown(underline_html, unsafe_allow_html=True)
    return st.session_state["current_page"]

# ------------------------------------------------------------------------------
# 4. BREADCRUMB
# ------------------------------------------------------------------------------
def render_breadcrumb(current_page: str) -> None:
    """Render clean breadcrumb bar (e.g. Home / Live Voice Scan)."""
    st.markdown(
        f"""
        <div style="font-size:12px; color:#64748B; margin-bottom:14px; padding:6px 12px; background-color:#FFFFFF; border:1px solid #D8E1EA; border-radius:4px; font-family:Arial;">
            Home &nbsp;/&nbsp; <span style="color:#0B3A66; font-weight:bold;">{current_page}</span>
        </div>
        """,
        unsafe_allow_html=True
    )

# ------------------------------------------------------------------------------
# 5. METRIC CARDS & ALERT BOXES
# ------------------------------------------------------------------------------
def render_metric_card(label: str, value: str, caption: str) -> None:
    """Render formal government dashboard metric card."""
    st.markdown(
        f"""
        <div style="background:#FFFFFF; border:1px solid #D8E1EA; border-radius:6px; padding:14px; text-align:center; box-shadow:0 1px 2px rgba(0,0,0,0.03);">
            <div style="font-size:12px; color:#64748B; font-weight:bold; font-family:Arial;">{label}</div>
            <div style="font-size:24px; font-weight:800; color:#0B3A66; margin:4px 0; font-family:Arial;">{value}</div>
            <div style="font-size:11px; color:#475569; font-family:Arial;">{caption}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

def render_alert_box(title: str, text: str, level: str = "saffron") -> None:
    """
    Render custom alert box:
    level: 'saffron', 'blue', 'safe', 'warning', 'critical'
    """
    border_color = "#E77817"
    bg_color = "#FFFBEB"
    text_color = "#92400E"

    if level == "blue":
        border_color = "#1D4ED8"
        bg_color = "#EFF6FF"
        text_color = "#1E40AF"
    elif level == "safe":
        border_color = "#15803D"
        bg_color = "#F0FDF4"
        text_color = "#166534"
    elif level == "warning":
        border_color = "#B45309"
        bg_color = "#FFFBEB"
        text_color = "#92400E"
    elif level == "critical":
        border_color = "#B91C1C"
        bg_color = "#FEF2F2"
        text_color = "#991B1B"

    st.markdown(
        f"""
        <div style="background-color:{bg_color}; border-left:5px solid {border_color}; border-top:1px solid #D8E1EA; border-right:1px solid #D8E1EA; border-bottom:1px solid #D8E1EA; padding:14px 18px; border-radius:4px; margin-bottom:16px; font-family:Arial;">
            <div style="font-weight:bold; font-size:14px; color:{text_color}; margin-bottom:4px;">{title}</div>
            <div style="font-size:13px; color:{text_color};">{text}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# ------------------------------------------------------------------------------
# 6. SIGNAL OBSERVATION SUMMARY ROWS
# ------------------------------------------------------------------------------
def render_signal_observation_rows(
    speech_act: float,
    pitch_var: float,
    spec_var: float,
    timing_reg: float,
    noise_inf: float
) -> None:
    """Render 5 horizontal indicator rows for live scan analysis."""
    observations = [
        {"name": "Voice Activity", "val": int(speech_act), "desc": "Normal speech frame density" if speech_act > 70 else "Low speech frame density", "color": "#0B3A66"},
        {"name": "Pitch Variation", "val": int(pitch_var), "desc": "Natural pitch modulation" if pitch_var > 20 else "Unusually flat / static contour", "color": "#15803D" if pitch_var > 20 else "#B91C1C"},
        {"name": "Spectral Variation", "val": int(spec_var), "desc": "Natural formant shifts" if spec_var > 20 else "Over-smoothed vocoder spectral shape", "color": "#15803D" if spec_var > 20 else "#B91C1C"},
        {"name": "Timing Regularity", "val": int(timing_reg), "desc": "Natural human pause cadence" if timing_reg < 75 else "Sustained synthetic frame regularity", "color": "#15803D" if timing_reg < 75 else "#B45309"},
        {"name": "Noise Influence", "val": int(noise_inf), "desc": "Low acoustic background noise" if noise_inf < 30 else "High noise floor affecting confidence", "color": "#64748B" if noise_inf < 30 else "#B45309"}
    ]

    for item in observations:
        pct = max(0, min(100, item["val"]))
        st.markdown(
            f"""
            <div style="margin-bottom:10px; background:#FFFFFF; padding:10px 12px; border:1px solid #D8E1EA; border-radius:4px;">
                <div style="display:flex; justify-between; align-items:center; margin-bottom:4px; font-size:12px; font-family:Arial;">
                    <span style="font-weight:bold; color:#0B3A66;">{item['name']}</span>
                    <span style="font-weight:bold; color:{item['color']};">{pct}% · {item['desc']}</span>
                </div>
                <div style="background-color:#E2E8F0; height:8px; border-radius:4px; overflow:hidden;">
                    <div style="width:{pct}%; background-color:{item['color']}; height:8px;"></div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

# ------------------------------------------------------------------------------
# 7. FOOTER
# ------------------------------------------------------------------------------
def render_footer() -> None:
    """Render formal Indian public-sector portal footer with disclaimer."""
    st.markdown(
        """
        <div style="background-color:#FFFFFF; border-top:3px solid #0B3A66; padding:20px 24px; margin-top:32px; text-align:center; font-size:12px; color:#64748B; font-family:Arial;">
            <div style="font-weight:bold; color:#0B3A66; font-size:13px;">
                SwarSatya (स्वरसत्य) · Smart India Hackathon 2026 Prototype
            </div>
            <div style="margin-top:4px;">
                This interface is an educational demonstration and not an official government service.
            </div>
            <div style="margin-top:10px; font-weight:bold; color:#0B3A66;">
                Privacy Policy &nbsp;<span>|</span>&nbsp; Accessibility Statement &nbsp;<span>|</span>&nbsp; Prototype Scope & Limitations
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
