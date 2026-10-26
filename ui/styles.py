"""
TTK styles for the modern dark dashboard theme.
"""

from tkinter import ttk
from config import *


def setup_styles(root):
    """Configure dark theme styles for ttk widgets."""
    style = ttk.Style(root)
    style.theme_use("clam")

    # Treeview – clean modern look
    style.configure(
        "Dark.Treeview",
        background=CARD,
        foreground=TEXT,
        fieldbackground=CARD,
        borderwidth=0,
        rowheight=32,
        font=("Segoe UI", 10)
    )
    style.configure(
        "Dark.Treeview.Heading",
        background=CARD_ALT,
        foreground=TEXT_DIM,
        borderwidth=0,
        font=("Segoe UI", 9, "bold"),
        relief="flat"
    )
    style.map(
        "Dark.Treeview",
        background=[("selected", ACCENT)],
        foreground=[("selected", TEXT)]
    )
    style.map(
        "Dark.Treeview.Heading",
        background=[("active", HOVER)]
    )

    # Scrollbar
    style.configure(
        "Dark.Vertical.TScrollbar",
        background=CARD_ALT,
        troughcolor=BG,
        borderwidth=0,
        arrowcolor=TEXT_MUTED
    )
