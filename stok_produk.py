# =========================================================
# STOK PRODUK PAGE
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
    QScrollArea
)

from PySide6.QtCore import Qt
from dashboard import Card
class StokProdukPage(QWidget):
    def __init__(self, app_data, dashboard):
        super().__init__()

        self.app_data = app_data
        self.dashboard = dashboard

        self.setup_ui()

    # =====================================================
    # UI
    # =====================================================
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
        root.setSpacing(15)

        # =================================================
        # HEADER
        # =================================================
        header_layout = QHBoxLayout()

        title = QLabel("Stok Produk")

        title.setStyleSheet("""
            font-size:28px;
            font-weight:bold;
            color:#111827;
        """)

        subtitle = QLabel(
            "Informasi stok seluruh produk UMKM"
        )

        subtitle.setStyleSheet("""
            color:#6b7280;
            font-size:13px;
        """)

        left_layout = QVBoxLayout()
        left_layout.addWidget(title)
        left_layout.addWidget(subtitle)

        header_layout.addLayout(left_layout)
        header_layout.addStretch()

        root.addLayout(header_layout)

        # =================================================
        # CARD INFO
        # =================================================
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(15)

        self.total_produk_card = Card(
            "Jumlah Produk",
            "0",
            "Produk",
            "#3b82f6",
            "📦"
        )

        self.total_stok_card = Card(
            "Total Stok",
            "0",
            "Unit",
            "#22c55e",
            "🧊"
        )

        self.stok_minim_card = Card(
            "Stok Menipis",
            "0",
            "Produk",
            "#f59e0b",
            "⚠"
        )

        cards_layout.addWidget(self.total_produk_card)
        cards_layout.addWidget(self.total_stok_card)
        cards_layout.addWidget(self.stok_minim_card)

        root.addLayout(cards_layout)

        # =================================================
        # TABLE FRAME
        # =================================================
        table_frame = QFrame()

        table_frame.setStyleSheet("""
            QFrame{
                background:white;
                border-radius:12px;
                border:1px solid #e5e7eb;
            }
        """)

        table_layout = QVBoxLayout(table_frame)

        table_title = QLabel("📦 Daftar Stok Produk")

        table_title.setStyleSheet("""
            font-size:18px;
            font-weight:bold;
            color:#111827;
        """)

        table_layout.addWidget(table_title)

        # =================================================
        # TABLE
        # =================================================
        self.table = QTableWidget(0, 5)

        self.table.setHorizontalHeaderLabels([
            "Nama Produk",
            "Kategori",
            "Stok",
            "Harga",
            "Status"
        ])

        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        self.table.setStyleSheet("""
            QTableWidget{
                border:none;
                background:white;
                font-size:13px;
                gridline-color:#f3f4f6;
            }

            QHeaderView::section{
                background:#f3f4f6;
                padding:12px;
                border:none;
                font-weight:bold;
                color:#111827;
            }

            QTableWidget::item{
                padding:10px;
            }
        """)

        table_layout.addWidget(self.table)

        root.addWidget(table_frame)

        # =================================================
        # REFRESH
        # =================================================
        self.refresh_table()

    # =====================================================
    # REFRESH TABLE
    # =====================================================
    def refresh_table(self):

        self.table.setRowCount(0)

        total_produk = len(self.app_data)

        total_stok = sum(
            p["stok"] for p in self.app_data
        )

        stok_minim = len([
            p for p in self.app_data
            if p["stok"] <= 5
        ])

        # UPDATE CARD
        self.total_produk_card.value.setText(
            str(total_produk)
        )

        self.total_stok_card.value.setText(
            str(total_stok)
        )

        self.stok_minim_card.value.setText(
            str(stok_minim)
        )

        # UPDATE TABLE
        for row, p in enumerate(self.app_data):

            self.table.insertRow(row)

            self.table.setItem(
                row,
                0,
                QTableWidgetItem(p["nama"])
            )

            self.table.setItem(
                row,
                1,
                QTableWidgetItem(p["kategori"])
            )

            self.table.setItem(
                row,
                2,
                QTableWidgetItem(str(p["stok"]))
            )

            self.table.setItem(
                row,
                3,
                QTableWidgetItem(
                    f"Rp {p['harga']}"
                )
            )

            # STATUS STOK
            if p["stok"] <= 5:
                status = "Hampir Habis"
            else:
                status = "Tersedia"

            status_item = QTableWidgetItem(status)

            self.table.setItem(
                row,
                4,
                status_item
            )