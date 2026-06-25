from PySide6.QtWidgets import (
    QWidget, QFrame, QLabel, QPushButton,
    QVBoxLayout, QHBoxLayout, QTableWidget,
    QTableWidgetItem, QHeaderView, QScrollArea, QMenu,
)
from PySide6.QtCore import Qt, QPoint
from PySide6.QtGui import QColor, QCursor

from utils.styles import (
    PAGE_STYLE, CARD_STYLE, TABLE_STYLE,
    POPUP_MENU_STYLE, COLOR_TEXT_DARK, COLOR_TEXT_MUTED,
)
from utils.storage import format_rupiah

# STAT CARD
class StatCard(QFrame):
    def __init__(self, title: str, value: str, subtitle: str, color: str, icon: str):
        super().__init__()
        self.setFixedHeight(100)
        self.setStyleSheet(f"""
            QFrame {{
                background: white;
                border: 1px solid #e5e7eb;
                border-radius: 14px;
            }}
            QLabel {{ background: transparent; border: none; }}
        """)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 14, 16, 14)
        layout.setSpacing(14)

        icon_lbl = QLabel(icon)
        icon_lbl.setAlignment(Qt.AlignCenter)
        icon_lbl.setFixedSize(52, 52)
        icon_lbl.setStyleSheet(f"""
            QLabel {{
                background: {color}22;
                color: {color};
                font-size: 22px;
                border-radius: 26px;
            }}
        """)

        text_layout = QVBoxLayout()
        text_layout.setSpacing(2)

        title_lbl = QLabel(title)
        title_lbl.setStyleSheet(f"color: {COLOR_TEXT_MUTED}; font-size: 12px;")

        self.value_lbl = QLabel(value)
        self.value_lbl.setStyleSheet(f"color: {color}; font-size: 24px; font-weight: bold;")

        subtitle_lbl = QLabel(subtitle)
        subtitle_lbl.setStyleSheet("color: #9ca3af; font-size: 11px;")

        text_layout.addWidget(title_lbl)
        text_layout.addWidget(self.value_lbl)
        text_layout.addWidget(subtitle_lbl)

        layout.addWidget(icon_lbl)
        layout.addLayout(text_layout)
        layout.addStretch()

    def set_value(self, val: str):
        self.value_lbl.setText(val)

# DASHBOARD PAGE
class DashboardPage(QWidget):
    BATAS_STOK_RENDAH = 5

    def __init__(self, data_produk: list, data_penjualan: list):
        super().__init__()
        self.data_produk    = data_produk
        self.data_penjualan = data_penjualan
        self._navigate_cb   = None
        self._setup_ui()

    def set_navigate_callback(self, cb):
        self._navigate_cb = cb

    # ----------------------------------------------------------
    def _setup_ui(self):
        self.setStyleSheet(PAGE_STYLE)
        main = QVBoxLayout(self)
        main.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setStyleSheet("QScrollArea { border: none; background: #f4f7fb; }")
        main.addWidget(scroll)

        container = QWidget()
        scroll.setWidget(container)

        root = QVBoxLayout(container)
        root.setContentsMargins(24, 24, 24, 24)
        root.setSpacing(20)

        root.addWidget(self._build_header())

        welcome = QLabel("Selamat datang 👋")
        welcome.setStyleSheet(
            f"font-size: 22px; font-weight: bold; color: {COLOR_TEXT_DARK};"
        )
        self._welcome_lbl = welcome

        sub = QLabel("Berikut ringkasan informasi usaha Anda hari ini.")
        sub.setStyleSheet(f"color: {COLOR_TEXT_MUTED}; font-size: 13px;")

        root.addWidget(welcome)
        root.addWidget(sub)

        # Stat cards
        cards_row = QHBoxLayout()
        cards_row.setSpacing(14)
        self.card_produk    = StatCard("Total Produk",      "0", "Produk",    "#3b82f6", "📦")
        self.card_stok      = StatCard("Total Stok",        "0", "Unit",      "#22c55e", "🧊")
        self.card_habis     = StatCard("Stok Hampir Habis", "0", "Produk",    "#f59e0b", "⚠")
        self.card_penjualan = StatCard("Total Penjualan",   "0", "Transaksi", "#a855f7", "🛒")
        for c in [self.card_produk, self.card_stok, self.card_habis, self.card_penjualan]:
            cards_row.addWidget(c)
        root.addLayout(cards_row)

        tables_row = QHBoxLayout()
        tables_row.setSpacing(18)
        tables_row.addWidget(self._build_stok_table())
        tables_row.addWidget(self._build_riwayat_table())
        root.addLayout(tables_row)

        self.refresh_dashboard()

    # ----------------------------------------------------------
    def _build_header(self) -> QFrame:
        frame = QFrame()
        frame.setFixedHeight(62)
        frame.setStyleSheet("""
            QFrame {
                background: white;
                border-radius: 12px;
                border: 1px solid #e5e7eb;
            }
            QLabel { background: transparent; border: none; }
            QPushButton { border: none; background: transparent; }
        """)
        layout = QHBoxLayout(frame)
        layout.setContentsMargins(16, 0, 16, 0)

        menu_icon = QLabel("☰")
        menu_icon.setStyleSheet(f"font-size: 18px; color: {COLOR_TEXT_DARK};")

        title = QLabel("Sistem Pengelolaan Stok dan Penjualan UMKM")
        title.setStyleSheet(
            f"font-size: 16px; font-weight: bold; color: {COLOR_TEXT_DARK};"
        )

        # Tombol profil
        self._profile_btn = QPushButton("👤  ...")
        self._profile_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self._profile_btn.setStyleSheet(f"""
            QPushButton {{
                font-size: 13px;
                color: {COLOR_TEXT_DARK};
                padding: 6px 14px;
                border-radius: 20px;
                border: 1px solid #e5e7eb;
                background: #f9fafb;
            }}
            QPushButton:hover {{ background: #f3f4f6; border-color: #d1d5db; }}
        """)
        self._profile_btn.clicked.connect(self._show_profile_menu)

        layout.addWidget(menu_icon)
        layout.addSpacing(10)
        layout.addWidget(title)
        layout.addStretch()
        layout.addWidget(self._profile_btn)
        return frame

    # ----------------------------------------------------------
    def _show_profile_menu(self):
        menu = QMenu(self)
        menu.setStyleSheet(POPUP_MENU_STYLE)

        # menu.addAction("👤  Profil / Akun",  lambda: self._navigate_cb and self._navigate_cb(4, "akun"))
        # menu.addAction("🏪  Kelola Toko",    lambda: self._navigate_cb and self._navigate_cb(4, "toko"))
        menu.addAction("⚙️  Pengaturan",    lambda: self._navigate_cb and self._navigate_cb(4, "pengaturan"))
        menu.addSeparator()
        menu.addAction("⏻  Logout",          lambda: self._navigate_cb and self._navigate_cb("logout"))

        btn_rect = self._profile_btn.rect()
        pos      = self._profile_btn.mapToGlobal(
            QPoint(0, btn_rect.height() + 4)
        )
        menu.exec(pos)

    # ----------------------------------------------------------
    def update_user_display(self, username: str):
        self._profile_btn.setText(f"👤  {username}  ▾")
        self._welcome_lbl.setText(f"Selamat datang, {username} 👋")

    # ----------------------------------------------------------
    def _build_stok_table(self) -> QFrame:
        frame = QFrame()
        frame.setStyleSheet(CARD_STYLE)
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(18, 18, 18, 18)

        t = QLabel("📦 Stok Hampir Habis")
        t.setStyleSheet(f"font-size: 16px; font-weight: bold; color: {COLOR_TEXT_DARK};")
        layout.addWidget(t)

        self.stok_table = QTableWidget(0, 4)
        self.stok_table.setHorizontalHeaderLabels(["Nama Produk", "Stok", "Batas", "Status"])
        self.stok_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.stok_table.verticalHeader().setVisible(False)
        self.stok_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.stok_table.setSelectionMode(QTableWidget.NoSelection)
        self.stok_table.setShowGrid(False)
        self.stok_table.setStyleSheet(TABLE_STYLE)
        layout.addWidget(self.stok_table)
        return frame

    # ----------------------------------------------------------
    def _build_riwayat_table(self) -> QFrame:
        frame = QFrame()
        frame.setStyleSheet(CARD_STYLE)
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(18, 18, 18, 18)

        t = QLabel("🛒 Penjualan Terakhir")
        t.setStyleSheet(f"font-size: 16px; font-weight: bold; color: {COLOR_TEXT_DARK};")
        layout.addWidget(t)

        self.jual_table = QTableWidget(0, 4)
        self.jual_table.setHorizontalHeaderLabels(["Tanggal", "No Transaksi", "Total", "Status"])
        self.jual_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.jual_table.verticalHeader().setVisible(False)
        self.jual_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.jual_table.setSelectionMode(QTableWidget.NoSelection)
        self.jual_table.setShowGrid(False)
        self.jual_table.setStyleSheet(TABLE_STYLE)
        layout.addWidget(self.jual_table)
        return frame

    # ----------------------------------------------------------
    def refresh_dashboard(self):
        self.card_produk.set_value(str(len(self.data_produk)))
        self.card_stok.set_value(str(sum(p["stok"] for p in self.data_produk)))
        self.card_habis.set_value(
            str(sum(1 for p in self.data_produk if p["stok"] <= self.BATAS_STOK_RENDAH))
        )
        self.card_penjualan.set_value(str(len(self.data_penjualan)))

        self.stok_table.setRowCount(0)
        for p in self.data_produk:
            if p["stok"] <= self.BATAS_STOK_RENDAH:
                row = self.stok_table.rowCount()
                self.stok_table.insertRow(row)
                for col, val in enumerate([p["nama"], str(p["stok"]),
                                           str(self.BATAS_STOK_RENDAH), "⚠ Hampir Habis"]):
                    item = QTableWidgetItem(val)
                    item.setForeground(QColor("#d97706" if col == 3 else COLOR_TEXT_DARK))
                    self.stok_table.setItem(row, col, item)

        self.jual_table.setRowCount(0)
        for t in reversed(self.data_penjualan[-5:]):
            row = self.jual_table.rowCount()
            self.jual_table.insertRow(row)
            for col, val in enumerate([
                t.get("tanggal", "-"), t.get("no_transaksi") or t.get("transaksi", "-"),
                format_rupiah(t.get("total", 0)), t.get("status", "-"),
            ]):
                item = QTableWidgetItem(val)
                item.setForeground(QColor("#16a34a" if (col == 3 and val == "Selesai") else COLOR_TEXT_DARK))
                self.jual_table.setItem(row, col, item)