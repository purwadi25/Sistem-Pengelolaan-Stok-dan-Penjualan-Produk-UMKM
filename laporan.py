from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QComboBox,
    QDateEdit,
    QScrollArea
)

from PySide6.QtCore import Qt, QDate


class LaporanPenjualanPage(QWidget):
    def __init__(self, data_penjualan):
        super().__init__()

        self.data_penjualan = data_penjualan

        self.setup_ui()

    # =====================================================
    # UI
    # =====================================================
    def setup_ui(self):

        self.setStyleSheet("""
            QWidget{
                background:#f5f7fb;
                font-family:'Segoe UI';
            }
        """)

        main_layout = QVBoxLayout(self)

        # =====================================================
        # SCROLL
        # =====================================================
        scroll = QScrollArea()

        scroll.setWidgetResizable(True)

        scroll.setHorizontalScrollBarPolicy(
            Qt.ScrollBarAlwaysOff
        )

        scroll.setStyleSheet("""
            QScrollArea{
                border:none;
                background:#f5f7fb;
            }
        """)

        main_layout.addWidget(scroll)

        # =====================================================
        # CONTAINER
        # =====================================================
        container = QWidget()

        scroll.setWidget(container)

        root = QVBoxLayout(container)

        root.setContentsMargins(30, 25, 30, 25)
        root.setSpacing(25)

        # =====================================================
        # HEADER
        # =====================================================
        title = QLabel("Laporan Penjualan")

        title.setStyleSheet("""
            font-size:34px;
            font-weight:bold;
            color:#111827;
        """)

        subtitle = QLabel(
            "Lihat dan analisis laporan penjualan bisnis Anda"
        )

        subtitle.setStyleSheet("""
            color:#6b7280;
            font-size:14px;
        """)

        root.addWidget(title)
        root.addWidget(subtitle)

        # =====================================================
        # CARD STATISTIK
        # =====================================================
        cards_layout = QHBoxLayout()

        cards_layout.setSpacing(15)

        def create_card(title, value, icon, color):

            card = QFrame()

            card.setStyleSheet("""
                QFrame{
                    background:white;
                    border-radius:18px;
                    border:1px solid #e5e7eb;
                }
            """)

            layout = QHBoxLayout(card)

            layout.setContentsMargins(20, 20, 20, 20)

            icon_label = QLabel(icon)

            icon_label.setAlignment(Qt.AlignCenter)

            icon_label.setStyleSheet(f"""
                QLabel{{
                    background:{color}20;
                    color:{color};
                    font-size:28px;

                    min-width:60px;
                    max-width:60px;

                    min-height:60px;
                    max-height:60px;

                    border-radius:30px;
                }}
            """)

            text_layout = QVBoxLayout()

            title_label = QLabel(title)

            title_label.setStyleSheet("""
                color:#6b7280;
                font-size:13px;
            """)

            value_label = QLabel(value)

            value_label.setStyleSheet(f"""
                color:{color};
                font-size:28px;
                font-weight:bold;
            """)

            text_layout.addWidget(title_label)
            text_layout.addWidget(value_label)

            layout.addWidget(icon_label)
            layout.addSpacing(15)
            layout.addLayout(text_layout)

            return card, value_label

        self.card_pendapatan, self.pendapatan_value = create_card(
            "Total Pendapatan",
            "Rp 0",
            "💰",
            "#14b8a6"
        )

        self.card_transaksi, self.transaksi_value = create_card(
            "Total Transaksi",
            "0",
            "🛒",
            "#3b82f6"
        )

        self.card_produk, self.produk_value = create_card(
            "Produk Terjual",
            "0",
            "📦",
            "#a855f7"
        )

        self.card_keuntungan, self.keuntungan_value = create_card(
            "Keuntungan",
            "Rp 0",
            "📈",
            "#f59e0b"
        )

        cards_layout.addWidget(self.card_pendapatan)
        cards_layout.addWidget(self.card_transaksi)
        cards_layout.addWidget(self.card_produk)
        cards_layout.addWidget(self.card_keuntungan)

        root.addLayout(cards_layout)

        # =====================================================
        # FILTER
        # =====================================================
        filter_card = QFrame()

        filter_card.setStyleSheet("""
            QFrame{
                background:white;
                border-radius:18px;
                border:1px solid #e5e7eb;
            }
        """)

        filter_layout = QHBoxLayout(filter_card)

        filter_layout.setContentsMargins(
            20, 20, 20, 20
        )

        self.date_filter = QDateEdit()

        self.date_filter.setDate(QDate.currentDate())

        self.date_filter.setCalendarPopup(True)

        self.date_filter.setStyleSheet("""
            QDateEdit{
                border:1px solid #d1d5db;
                border-radius:10px;
                padding:10px;
                background:white;
                font-size:13px;
            }
        """)

        self.combo_filter = QComboBox()

        self.combo_filter.addItems([
            "Semua Produk",
            "Makanan",
            "Minuman",
            "Snack"
        ])

        self.combo_filter.setStyleSheet("""
            QComboBox{
                border:1px solid #d1d5db;
                border-radius:10px;
                padding:10px;
                background:white;
                font-size:13px;
            }
        """)

        export_btn = QPushButton(
            "📄 Export PDF"
        )

        export_btn.setStyleSheet("""
            QPushButton{
                background:#14b8a6;
                color:white;
                border:none;
                padding:12px 18px;
                border-radius:10px;
                font-size:13px;
                font-weight:bold;
            }

            QPushButton:hover{
                background:#0f766e;
            }
        """)

        print_btn = QPushButton(
            "🖨 Print"
        )

        print_btn.setStyleSheet("""
            QPushButton{
                background:#3b82f6;
                color:white;
                border:none;
                padding:12px 18px;
                border-radius:10px;
                font-size:13px;
                font-weight:bold;
            }
        """)

        filter_layout.addWidget(self.date_filter)
        filter_layout.addWidget(self.combo_filter)
        filter_layout.addStretch()
        filter_layout.addWidget(export_btn)
        filter_layout.addWidget(print_btn)

        root.addWidget(filter_card)

        # =====================================================
        # GRAFIK PLACEHOLDER
        # =====================================================
        grafik_card = QFrame()

        grafik_card.setFixedHeight(300)

        grafik_card.setStyleSheet("""
            QFrame{
                background:white;
                border-radius:18px;
                border:1px solid #e5e7eb;
            }
        """)

        grafik_layout = QVBoxLayout(grafik_card)

        grafik_title = QLabel(
            "📈 Grafik Penjualan"
        )

        grafik_title.setStyleSheet("""
            font-size:24px;
            font-weight:bold;
            color:#111827;
        """)

        grafik_placeholder = QLabel(
            "Area Grafik Penjualan"
        )

        grafik_placeholder.setAlignment(
            Qt.AlignCenter
        )

        grafik_placeholder.setStyleSheet("""
            QLabel{
                background:#f9fafb;
                border:2px dashed #d1d5db;
                border-radius:14px;
                font-size:18px;
                color:#9ca3af;
            }
        """)

        grafik_layout.addWidget(grafik_title)
        grafik_layout.addWidget(grafik_placeholder)

        root.addWidget(grafik_card)

        # =====================================================
        # TABLE LAPORAN
        # =====================================================
        table_card = QFrame()

        table_card.setStyleSheet("""
            QFrame{
                background:white;
                border-radius:18px;
                border:1px solid #e5e7eb;
            }
        """)

        table_layout = QVBoxLayout(table_card)

        title_table = QLabel(
            "📋 Riwayat Penjualan"
        )

        title_table.setStyleSheet("""
            font-size:24px;
            font-weight:bold;
            color:#111827;
        """)

        table_layout.addWidget(title_table)

        self.table = QTableWidget(0, 5)

        self.table.setHorizontalHeaderLabels([
            "No Transaksi",
            "Tanggal",
            "Pelanggan",
            "Total",
            "Status"
        ])

        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        self.table.verticalHeader().setVisible(False)

        self.table.setStyleSheet("""
            QTableWidget{
                border:none;
                background:white;
                font-size:13px;
            }

            QHeaderView::section{
                background:#f3f4f6;
                padding:12px;
                border:none;
                font-weight:bold;
            }
        """)

        table_layout.addWidget(self.table)

        root.addWidget(table_card)

        self.refresh_table()

    # =====================================================
    # REFRESH TABLE
    # =====================================================
    def refresh_table(self):

        self.table.setRowCount(0)

        total_pendapatan = 0

        for data in reversed(self.data_penjualan):

            row = self.table.rowCount()

            self.table.insertRow(row)

            isi = [
                data["transaksi"],
                data["tanggal"],
                data["pelanggan"],
                data["total"],
                data["status"]
            ]

            for col, value in enumerate(isi):

                item = QTableWidgetItem(value)

                if (
                    col == 4 and
                    value == "Selesai"
                ):
                    item.setForeground(Qt.green)

                self.table.setItem(
                    row,
                    col,
                    item
                )

            angka = (
                data["total"]
                .replace("Rp ", "")
                .replace(".", "")
            )

            total_pendapatan += int(angka)

        # =====================================================
        # UPDATE CARD
        # =====================================================
        self.pendapatan_value.setText(
            f"Rp {total_pendapatan:,}".replace(",", ".")
        )

        self.transaksi_value.setText(
            str(len(self.data_penjualan))
        )

        self.produk_value.setText(
            str(len(self.data_penjualan) * 2)
        )

        keuntungan = int(total_pendapatan * 0.35)

        self.keuntungan_value.setText(
            f"Rp {keuntungan:,}".replace(",", ".")
        )