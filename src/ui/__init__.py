"""
UI Package for SwarSatya Voice Security Desktop Application.
Provides modular views for Header, Scan, Ledger, Model Studio, and About tabs.
"""

from src.ui.header import build_header
from src.ui.tab_scan import build_tab_scan
from src.ui.tab_ledger import build_tab_ledger
from src.ui.tab_studio import build_tab_studio
from src.ui.tab_about import build_tab_about

__all__ = [
    "build_header",
    "build_tab_scan",
    "build_tab_ledger",
    "build_tab_studio",
    "build_tab_about"
]
