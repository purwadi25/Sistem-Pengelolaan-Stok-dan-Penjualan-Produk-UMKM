COLOR_PRIMARY       = "#14b8a6"
COLOR_PRIMARY_DARK  = "#0f766e"
COLOR_BG_PAGE       = "#f4f7fb"
COLOR_BG_CARD       = "#ffffff"
COLOR_BORDER        = "#e5e7eb"
COLOR_TEXT_DARK     = "#111827"
COLOR_TEXT_MUTED    = "#6b7280"
COLOR_TEXT_HINT     = "#9ca3af"
COLOR_SIDEBAR_BG    = "#0f172a"
COLOR_SIDEBAR_HOVER = "#1e293b"

# PAGE
PAGE_STYLE = f"""
    QWidget {{
        background: {COLOR_BG_PAGE};
        font-family: 'Segoe UI';
        color: {COLOR_TEXT_DARK};
    }}
    QLabel {{
        color: {COLOR_TEXT_DARK};
        background: transparent;
        border: none;
    }}
    QScrollArea {{
        border: none;
        background: {COLOR_BG_PAGE};
    }}
"""

# CARD
CARD_STYLE = f"""
    QFrame {{
        background: {COLOR_BG_CARD};
        border-radius: 16px;
        border: 1px solid {COLOR_BORDER};
    }}
    QLabel {{
        background: transparent;
        border: none;
        color: {COLOR_TEXT_DARK};
    }}
"""

# INPUT FIELD
INPUT_STYLE = f"""
    QLineEdit {{
        border: 1.5px solid {COLOR_BORDER};
        border-radius: 10px;
        padding: 10px 14px;
        background: {COLOR_BG_CARD};
        font-size: 14px;
        color: {COLOR_TEXT_DARK};
        selection-background-color: {COLOR_PRIMARY};
        selection-color: white;
    }}
    QLineEdit:focus {{
        border: 2px solid {COLOR_PRIMARY};
        background: {COLOR_BG_CARD};
    }}
    QLineEdit:disabled {{
        background: #f9fafb;
        color: {COLOR_TEXT_MUTED};
    }}
"""

# COMBOBOX
COMBO_STYLE = f"""
    QComboBox {{
        border: 1.5px solid {COLOR_BORDER};
        border-radius: 10px;
        padding-left: 12px;
        padding-right: 8px;
        background: {COLOR_BG_CARD};
        font-size: 14px;
        color: {COLOR_TEXT_DARK};
    }}
    QComboBox:focus {{
        border: 2px solid {COLOR_PRIMARY};
    }}
    QComboBox::drop-down {{
        border: none;
        width: 28px;
    }}
    QComboBox::down-arrow {{
        width: 12px;
        height: 12px;
    }}
    QComboBox QAbstractItemView {{
        background: {COLOR_BG_CARD};
        color: {COLOR_TEXT_DARK};
        border: 1px solid {COLOR_BORDER};
        outline: none;
        selection-background-color: {COLOR_PRIMARY};
        selection-color: white;
    }}
"""

# TOMBOL PRIMER
BTN_PRIMARY_STYLE = f"""
    QPushButton {{
        background: {COLOR_PRIMARY};
        color: white;
        border: none;
        border-radius: 10px;
        padding: 12px 24px;
        font-size: 14px;
        font-weight: bold;
    }}
    QPushButton:hover   {{ background: {COLOR_PRIMARY_DARK}; }}
    QPushButton:pressed {{ background: #0d6861; }}
    QPushButton:disabled {{ background: #a7f3d0; color: #d1fae5; }}
"""

# TOMBOL SEKUNDER
BTN_SECONDARY_STYLE = f"""
    QPushButton {{
        background: #f3f4f6;
        color: {COLOR_TEXT_DARK};
        border: 1px solid {COLOR_BORDER};
        border-radius: 10px;
        padding: 12px 24px;
        font-size: 14px;
        font-weight: bold;
    }}
    QPushButton:hover {{ background: #e5e7eb; }}
"""

# TOMBOL BAHAYA
BTN_DANGER_STYLE = f"""
    QPushButton {{
        background: #ef4444;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 8px 16px;
        font-size: 13px;
        font-weight: bold;
    }}
    QPushButton:hover {{ background: #dc2626; }}
"""

# TABEL
TABLE_STYLE = f"""
    QTableWidget {{
        border: none;
        background: {COLOR_BG_CARD};
        font-size: 13px;
        gridline-color: #f3f4f6;
        color: {COLOR_TEXT_DARK};
        alternate-background-color: #f9fafb;
        outline: none;
    }}
    QTableWidget::item {{
        padding: 4px 10px;
        color: {COLOR_TEXT_DARK};
        border: none;
    }}
    QTableWidget::item:selected {{
        background: #dbeafe;
        color: {COLOR_TEXT_DARK};
    }}
    QHeaderView::section {{
        background: #f3f4f6;
        color: {COLOR_TEXT_DARK};
        padding: 12px;
        border: none;
        border-bottom: 1px solid {COLOR_BORDER};
        font-size: 13px;
        font-weight: bold;
    }}
    QHeaderView::section:checked {{
        background: #f3f4f6;
    }}
    QTableCornerButton::section {{
        background: #f3f4f6;
        border: none;
    }}
"""

# DATE EDIT
DATE_STYLE = f"""
    QDateEdit {{
        border: 1.5px solid {COLOR_BORDER};
        border-radius: 8px;
        padding: 6px 10px;
        background: {COLOR_BG_CARD};
        font-size: 13px;
        color: {COLOR_TEXT_DARK};
    }}
    QDateEdit:focus {{
        border: 2px solid {COLOR_PRIMARY};
    }}
    QDateEdit::drop-down {{
        border: none;
        width: 24px;
    }}
"""

# POPUP MENU
POPUP_MENU_STYLE = f"""
    QMenu {{
        background: {COLOR_BG_CARD};
        border: 1px solid {COLOR_BORDER};
        border-radius: 12px;
        padding: 6px;
        color: {COLOR_TEXT_DARK};
        font-size: 14px;
        font-family: 'Segoe UI';
    }}
    QMenu::item {{
        padding: 10px 20px 10px 14px;
        border-radius: 8px;
        color: {COLOR_TEXT_DARK};
    }}
    QMenu::item:selected {{
        background: #f0fdf4;
        color: {COLOR_PRIMARY_DARK};
    }}
    QMenu::separator {{
        height: 1px;
        background: {COLOR_BORDER};
        margin: 4px 10px;
    }}
"""