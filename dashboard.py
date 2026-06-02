
# =========================================================
# DASHBOARD CARD
# =========================================================
from PySide6.QtWidgets import (
    QWidget,
    QFrame,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QLineEdit,
    QMessageBox,
    QScrollArea,
)

from PySide6.QtCore import Qt


class Card(QFrame):
    def __init__(self, title, value, subtitle, color, icon):
        super().__init__()

        self.setFixedHeight(95)

        self.setStyleSheet("""
            QFrame{
                background:white;
                border:1px solid #e5e7eb;
                border-radius:12px;
            }
        """)

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)

        # =================================================
        # ICON BULAT
        # =================================================
        icon_bg = QLabel(icon)

        icon_bg.setAlignment(Qt.AlignCenter)

        icon_bg.setStyleSheet(f"""
            QLabel{{
                background:{color}20;
                color:{color};

                font-size:22px;
                font-weight:bold;

                min-width:50px;
                max-width:50px;

                min-height:50px;
                max-height:50px;

                border-radius:25px;
            }}
        """)

        # =================================================
        # TEXT
        # =================================================
        text_layout = QVBoxLayout()
        text_layout.setSpacing(0)

        title_label = QLabel(title)

        title_label.setStyleSheet("""
            color:#6b7280;
            font-size:12px;
        """)

        self.value = QLabel(value)

        self.value.setStyleSheet(f"""
            color:{color};
            font-size:26px;
            font-weight:bold;
        """)

        subtitle_label = QLabel(subtitle)

        subtitle_label.setStyleSheet("""
            color:#9ca3af;
            font-size:11px;
        """)

        text_layout.addWidget(title_label)
        text_layout.addWidget(self.value)
        text_layout.addWidget(subtitle_label)

        # =================================================
        # ADD WIDGET
        # =================================================
        main_layout.addWidget(icon_bg)
        main_layout.addLayout(text_layout)
        main_layout.addStretch()


# =========================================================
# DASHBOARD PAGE
# =========================================================
class DashboardPage(QWidget):
    def __init__(self, app_data, data_penjualan):
        super().__init__()

        self.app_data = app_data
        self.data_penjualan = data_penjualan

        self.setup_ui()

    def setup_ui(self):

        self.setStyleSheet("""
            QWidget{
                background:#f8fafc;
                font-family:'Segoe UI';
            }
        """)

        main_layout = QVBoxLayout(self)

        # =================================================
        # SCROLL AREA
        # =================================================
        scroll = QScrollArea()

        scroll.setWidgetResizable(True)

        scroll.setHorizontalScrollBarPolicy(
            Qt.ScrollBarAlwaysOff
        )

        scroll.setStyleSheet("""
            QScrollArea{
                border:none;
                background:#f8fafc;
            }
        """)

        main_layout.addWidget(scroll)

        # =================================================
        # CONTAINER
        # =================================================
        container = QWidget()

        scroll.setWidget(container)

        root = QVBoxLayout(container)

        root.setContentsMargins(20, 20, 20, 20)
        root.setSpacing(18)

        # =================================================
        # HEADER
        # =================================================
        header = QFrame()

        header.setFixedHeight(65)

        header.setStyleSheet("""
            QFrame{
                background:white;
                border-radius:12px;
                border:1px solid #e5e7eb;
            }
        """)

        header_layout = QHBoxLayout(header)

        menu_icon = QLabel("☰")

        menu_icon.setStyleSheet("""
            font-size:20px;
            font-weight:bold;
            color:#374151;
        """)

        title = QLabel(
            "Sistem Pengelolaan Stok dan Penjualan Produk UMKM"
        )

        title.setStyleSheet("""
            font-size:18px;
            font-weight:bold;
            color:#111827;
        """)

        profile = QLabel("👤 Pemilik UMKM")

        profile.setStyleSheet("""
            font-size:13px;
            color:#374151;
        """)

        header_layout.addWidget(menu_icon)
        header_layout.addSpacing(10)
        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(profile)

        root.addWidget(header)

        # =================================================
        # WELCOME
        # =================================================
        welcome = QLabel(
            "Selamat datang, Pemilik UMKM 👋"
        )

        welcome.setStyleSheet("""
            font-size:24px;
            font-weight:bold;
            color:#111827;
        """)

        subtitle = QLabel(
            "Berikut ringkasan informasi usaha Anda hari ini."
        )

        subtitle.setStyleSheet("""
            color:#6b7280;
            font-size:13px;
        """)

        root.addWidget(welcome)
        root.addWidget(subtitle)

        # =================================================
        # DASHBOARD CARD
        # =================================================
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(15)

        self.card_produk = Card(
            "Total Produk",
            "0",
            "Produk",
            "#3b82f6",
            "📦"
        )

        self.card_stok = Card(
            "Total Stok",
            "0",
            "Unit",
            "#22c55e",
            "🧊"
        )

        self.card_habis = Card(
            "Stok Hampir Habis",
            "0",
            "Produk",
            "#f59e0b",
            "⚠"
        )

        self.card_penjualan = Card(
            "Total Penjualan",
            "0",
            "Transaksi",
            "#a855f7",
            "🛒"
        )

        cards_layout.addWidget(self.card_produk)
        cards_layout.addWidget(self.card_stok)
        cards_layout.addWidget(self.card_habis)
        cards_layout.addWidget(self.card_penjualan)

        root.addLayout(cards_layout)

        # =================================================
        # 2 TABLE DASHBOARD
        # =================================================
        tables_layout = QHBoxLayout()
        tables_layout.setSpacing(20)

        # =================================================
        # STOK HAMPIR HABIS
        # =================================================
        stok_frame = QFrame()

        stok_frame.setStyleSheet("""
            QFrame{
                background:white;
                border-radius:12px;
                border:1px solid #e5e7eb;
            }
        """)

        stok_layout = QVBoxLayout(stok_frame)

        stok_title = QLabel("📦 Stok Hampir Habis")

        stok_title.setStyleSheet("""
            font-size:18px;
            font-weight:bold;
            color:#111827;
        """)

        stok_layout.addWidget(stok_title)

        self.stok_table = QTableWidget(0, 4)

        self.stok_table.setHorizontalHeaderLabels([
            "Nama Produk",
            "Stok",
            "Batas",
            "Status"
        ])

        self.stok_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        self.stok_table.setStyleSheet("""
            QTableWidget{
                border:none;
                background:white;
                font-size:13px;
            }

            QHeaderView::section{
                background:#f3f4f6;
                padding:10px;
                border:none;
                font-weight:bold;
            }
        """)

        stok_layout.addWidget(self.stok_table)

        # =================================================
        # PENJUALAN TERAKHIR
        # =================================================
        jual_frame = QFrame()

        jual_frame.setStyleSheet("""
            QFrame{
                background:white;
                border-radius:12px;
                border:1px solid #e5e7eb;
            }
        """)

        jual_layout = QVBoxLayout(jual_frame)

        jual_title = QLabel("🛒 Penjualan Terakhir")

        jual_title.setStyleSheet("""
            font-size:18px;
            font-weight:bold;
            color:#111827;
        """)

        jual_layout.addWidget(jual_title)

        self.jual_table = QTableWidget(0, 5)

        self.jual_table.setHorizontalHeaderLabels([
            "Tanggal",
            "Transaksi",
            "Pelanggan",
            "Total",
            "Status"
        ])

        self.jual_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        self.jual_table.setStyleSheet("""
            QTableWidget{
                border:none;
                background:white;
                font-size:13px;
            }

            QHeaderView::section{
                background:#f3f4f6;
                padding:10px;
                border:none;
                font-weight:bold;
            }
        """)

        jual_layout.addWidget(self.jual_table)

        # =================================================
        # MASUKKAN KE HORIZONTAL
        # =================================================
        tables_layout.addWidget(stok_frame)
        tables_layout.addWidget(jual_frame)

        root.addLayout(tables_layout)

        # =================================================
        # REFRESH
        # =================================================
        self.refresh_dashboard()

    # =====================================================
    # REFRESH DASHBOARD
    # =====================================================
    def refresh_dashboard(self):

        total_produk = len(self.app_data)

        total_stok = sum(
            p["stok"] for p in self.app_data
        )

        stok_habis = len([
            p for p in self.app_data
            if p["stok"] <= 5
        ])

        self.card_produk.value.setText(
            str(total_produk)
        )

        self.card_stok.value.setText(
            str(total_stok)
        )

        self.card_habis.value.setText(
            str(stok_habis)
        )

        self.card_penjualan.value.setText(
            str(len(self.data_penjualan))
        )

        # =================================================
        # STOK HAMPIR HABIS
        # =================================================
        self.stok_table.setRowCount(0)

        for p in self.app_data:

            if p["stok"] <= 5:

                row = self.stok_table.rowCount()

                self.stok_table.insertRow(row)

                self.stok_table.setItem(
                    row,
                    0,
                    QTableWidgetItem(p["nama"])
                )

                self.stok_table.setItem(
                    row,
                    1,
                    QTableWidgetItem(str(p["stok"]))
                )

                self.stok_table.setItem(
                    row,
                    2,
                    QTableWidgetItem("5")
                )

                self.stok_table.setItem(
                    row,
                    3,
                    QTableWidgetItem("Hampir Habis")
                )

        # =================================================
        # PENJUALAN TERAKHIR
        # =================================================
        self.jual_table.setRowCount(0)

        for data in reversed(self.data_penjualan[-5:]):

            row = self.jual_table.rowCount()

            self.jual_table.insertRow(row)

            self.jual_table.setItem(
                row,
                0,
                QTableWidgetItem(data["tanggal"])
            )

            self.jual_table.setItem(
                row,
                1,
                QTableWidgetItem(data["transaksi"])
            )

            self.jual_table.setItem(
                row,
                2,
                QTableWidgetItem(data["pelanggan"])
            )

            self.jual_table.setItem(
                row,
                3,
                QTableWidgetItem(data["total"])
            )

            self.jual_table.setItem(
                row,
                4,
                QTableWidgetItem(data["status"])
            )
