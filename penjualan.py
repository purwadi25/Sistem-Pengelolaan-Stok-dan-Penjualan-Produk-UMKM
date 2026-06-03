# =========================================================
# PENJUALAN PAGE
# =========================================================
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
    QLineEdit,
    QMessageBox,
    QScrollArea,
)

from PySide6.QtCore import (
    Qt,
    QDate
)

from PySide6.QtGui import QColor


class PenjualanPage(QWidget):

    def __init__(
        self,
        app_data,
        data_penjualan,
        dashboard
    ):
        super().__init__()

        self.app_data = app_data
        self.data_penjualan = data_penjualan
        self.dashboard = dashboard

        self.keranjang = []

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
        # SCROLL AREA
        # =====================================================
        scroll = QScrollArea()

        scroll.setWidgetResizable(True)

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

        root.setContentsMargins(
            30,
            25,
            30,
            25
        )

        root.setSpacing(25)

        # =====================================================
        # HEADER
        # =====================================================
        title = QLabel("Penjualan")

        title.setStyleSheet("""
            font-size:34px;
            font-weight:bold;
            color:#111827;
        """)

        subtitle = QLabel(
            "Kelola transaksi penjualan produk"
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

            layout.setContentsMargins(
                20,
                20,
                20,
                20
            )

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

            value_label = QLabel(str(value))

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

        self.card_transaksi, self.transaksi_value = create_card(
            "Total Transaksi",
            0,
            "🛒",
            "#14b8a6"
        )

        self.card_penjualan, self.penjualan_value = create_card(
            "Total Penjualan",
            "Rp 0",
            "💰",
            "#3b82f6"
        )

        self.card_produk, self.produk_value = create_card(
            "Produk Terjual",
            0,
            "📦",
            "#a855f7"
        )

        cards_layout.addWidget(self.card_transaksi)
        cards_layout.addWidget(self.card_penjualan)
        cards_layout.addWidget(self.card_produk)

        root.addLayout(cards_layout)

        # =====================================================
        # CONTENT ROW
        # =====================================================
        content_row = QHBoxLayout()

        content_row.setSpacing(20)

        # =====================================================
        # PRODUK
        # =====================================================
        produk_card = QFrame()

        produk_card.setStyleSheet("""
            QFrame{
                background:white;
                border-radius:18px;
                border:1px solid #e5e7eb;
            }
        """)

        produk_layout = QVBoxLayout(produk_card)

        produk_layout.setContentsMargins(
            20,
            20,
            20,
            20
        )

        produk_title = QLabel("Daftar Produk")

        produk_title.setStyleSheet("""
            font-size:24px;
            font-weight:bold;
            color:#111827;
        """)

        produk_layout.addWidget(produk_title)

        # =====================================================
        # SEARCH
        # =====================================================
        self.search_input = QLineEdit()

        self.search_input.setPlaceholderText(
            "🔍 Cari produk..."
        )

        self.search_input.textChanged.connect(
            self.refresh_produk
        )

        self.search_input.setStyleSheet("""
            QLineEdit{
                border:1px solid #d1d5db;
                border-radius:10px;
                padding:12px;
                background:white;
                font-size:13px;
            }
        """)

        produk_layout.addWidget(
            self.search_input
        )

        # =====================================================
        # TABLE PRODUK
        # =====================================================
        self.table_produk = QTableWidget(0, 5)

        self.table_produk.setHorizontalHeaderLabels([
            "Nama Produk",
            "Kategori",
            "Harga",
            "Stok",
            "Aksi"
        ])

        self.table_produk.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        self.table_produk.verticalHeader().setVisible(False)

        self.table_produk.setMinimumHeight(280)

        self.table_produk.setStyleSheet("""
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

        self.table_produk.cellClicked.connect(
            self.handle_produk_click
        )

        produk_layout.addWidget(
            self.table_produk
        )

        # =====================================================
        # KERANJANG
        # =====================================================
        keranjang_card = QFrame()

        keranjang_card.setFixedWidth(450)

        keranjang_card.setStyleSheet("""
            QFrame{
                background:white;
                border-radius:18px;
                border:1px solid #e5e7eb;
            }
        """)

        keranjang_layout = QVBoxLayout(
            keranjang_card
        )

        keranjang_layout.setContentsMargins(
            20,
            20,
            20,
            20
        )

        keranjang_title = QLabel(
            "Keranjang Penjualan"
        )

        keranjang_title.setStyleSheet("""
            font-size:24px;
            font-weight:bold;
            color:#111827;
        """)

        keranjang_layout.addWidget(
            keranjang_title
        )

        # =====================================================
        # TABLE KERANJANG
        # =====================================================
        self.table_keranjang = QTableWidget(0, 4)

        self.table_keranjang.setHorizontalHeaderLabels([
            "Produk",
            "Qty",
            "Subtotal",
            "Aksi"
        ])

        self.table_keranjang.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        self.table_keranjang.verticalHeader().setVisible(False)

        self.table_keranjang.setMinimumHeight(180)

        self.table_keranjang.setAlternatingRowColors(True)

        self.table_keranjang.setShowGrid(False)

        self.table_keranjang.setStyleSheet("""
            QTableWidget{
                border:none;
                background:white;
                font-size:13px;
                alternate-background-color:#f9fafb;
            }

            QHeaderView::section{
                background:#f3f4f6;
                padding:12px;
                border:none;
                font-weight:bold;
            }

            QTableWidget::item{
                padding:10px;
            }
        """)

        self.table_keranjang.cellClicked.connect(
            self.handle_keranjang_click
        )

        keranjang_layout.addWidget(
            self.table_keranjang
        )

        # =====================================================
        # TOTAL
        # =====================================================
        total_frame = QFrame()

        total_frame.setStyleSheet("""
            QFrame{
                background:#f9fafb;
                border-radius:14px;
            }
        """)

        total_layout = QVBoxLayout(total_frame)

        total_label = QLabel("Total Bayar")

        total_label.setStyleSheet("""
            font-size:15px;
            color:#6b7280;
        """)

        self.total_bayar = QLabel("Rp 0")

        self.total_bayar.setStyleSheet("""
            font-size:34px;
            font-weight:bold;
            color:#14b8a6;
        """)

        total_layout.addWidget(total_label)
        total_layout.addWidget(self.total_bayar)

        keranjang_layout.addWidget(total_frame)

        # =====================================================
        # BUTTON BAYAR
        # =====================================================
        bayar_btn = QPushButton("🛒 Bayar")

        bayar_btn.setStyleSheet("""
            QPushButton{
                background:#14b8a6;
                color:white;
                border:none;
                padding:16px;
                border-radius:12px;
                font-size:15px;
                font-weight:bold;
            }

            QPushButton:hover{
                background:#0f766e;
            }
        """)

        bayar_btn.clicked.connect(
            self.proses_pembayaran
        )

        keranjang_layout.addWidget(
            bayar_btn
        )

        # =====================================================
        # ADD CONTENT
        # =====================================================
        content_row.addWidget(produk_card)
        content_row.addWidget(keranjang_card)

        root.addLayout(content_row)

        # =====================================================
        # RIWAYAT
        # =====================================================
        riwayat_card = QFrame()

        riwayat_card.setStyleSheet("""
            QFrame{
                background:white;
                border-radius:18px;
                border:1px solid #e5e7eb;
            }
        """)

        riwayat_layout = QVBoxLayout(
            riwayat_card
        )

        riwayat_layout.setContentsMargins(
            20,
            20,
            20,
            20
        )

        riwayat_title = QLabel(
            "Riwayat Transaksi"
        )

        riwayat_title.setStyleSheet("""
            font-size:24px;
            font-weight:bold;
        """)

        riwayat_layout.addWidget(
            riwayat_title
        )

        self.table_riwayat = QTableWidget(0, 6)

        self.table_riwayat.setHorizontalHeaderLabels([
            "No Transaksi",
            "Tanggal",
            "Kategori",
            "Pelanggan",
            "Total",
            "Status"
        ])

        self.table_riwayat.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        self.table_riwayat.verticalHeader().setVisible(False)

        self.table_riwayat.setMinimumHeight(250)

        self.table_riwayat.setStyleSheet("""
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

        riwayat_layout.addWidget(
            self.table_riwayat
        )

        root.addWidget(riwayat_card)

        self.refresh_produk()
        self.refresh_riwayat()

    # =====================================================
    # REFRESH PRODUK
    # =====================================================
    def refresh_produk(self):

        keyword = (
            self.search_input.text()
            .lower()
        )

        self.filtered_produk = []

        self.table_produk.setRowCount(0)

        for produk in self.app_data:

            if keyword not in produk["nama"].lower():
                continue

            self.filtered_produk.append(produk)

            row = self.table_produk.rowCount()

            self.table_produk.insertRow(row)

            data = [
                produk["nama"],
                produk["kategori"],
                f"Rp {produk['harga']:,}".replace(",", "."),
                str(produk["stok"]),
                "➕ Tambah"
            ]

            for col, value in enumerate(data):

                item = QTableWidgetItem(value)

                item.setTextAlignment(
                    Qt.AlignCenter
                )

                self.table_produk.setItem(
                    row,
                    col,
                    item
                )

    # =====================================================
    # TAMBAH KE KERANJANG
    # =====================================================
    def handle_produk_click(
        self,
        row,
        column
    ):

        if column != 4:
            return

        produk = self.filtered_produk[row]

        if produk["stok"] <= 0:

            QMessageBox.warning(
                self,
                "Error",
                "Stok habis!"
            )

            return

        for keranjang_item in self.keranjang:

            if keranjang_item["nama"] == produk["nama"]:

                if keranjang_item["qty"] >= produk["stok"]:

                    QMessageBox.warning(
                        self,
                        "Error",
                        "Jumlah melebihi stok!"
                    )

                    return

                keranjang_item["qty"] += 1

                self.refresh_keranjang()

                return

        item = {
            "nama": produk["nama"],
            "kategori": produk["kategori"],
            "modal": produk["modal"],
            "harga": produk["harga"],
            "qty": 1
        }

        self.keranjang.append(item)

        self.refresh_keranjang()

    # =====================================================
    # REFRESH KERANJANG
    # =====================================================
    def refresh_keranjang(self):

        self.table_keranjang.setRowCount(0)

        total = 0

        for item in self.keranjang:

            row = self.table_keranjang.rowCount()

            self.table_keranjang.insertRow(row)

            subtotal = (
                item["harga"]
                * item["qty"]
            )

            total += subtotal

            data = [
                item["nama"],
                str(item["qty"]),
                f"Rp {subtotal:,}".replace(",", "."),
                "➖"
            ]

            for col, value in enumerate(data):

                item_widget = QTableWidgetItem(value)

                item_widget.setTextAlignment(
                    Qt.AlignCenter
                )

                if col == 3:

                    item_widget.setForeground(
                        QColor("#ef4444")
                    )

                    font = item_widget.font()

                    font.setBold(True)

                    item_widget.setFont(font)

                self.table_keranjang.setItem(
                    row,
                    col,
                    item_widget
                )

        self.total_bayar.setText(
            f"Rp {total:,}".replace(",", ".")
        )

    # =====================================================
    # HAPUS / KURANGI QTY
    # =====================================================
    def handle_keranjang_click(
        self,
        row,
        column
    ):

        if column == 3:

            item = self.keranjang[row]

            if item["qty"] > 1:

                item["qty"] -= 1

            else:

                self.keranjang.pop(row)

            self.refresh_keranjang()

    # =====================================================
    # PEMBAYARAN
    # =====================================================
    def proses_pembayaran(self):

        if len(self.keranjang) == 0:

            QMessageBox.warning(
                self,
                "Error",
                "Keranjang kosong!"
            )

            return

        total = 0
        total_keuntungan = 0

        kategori_transaksi = "Umum"

        for item in self.keranjang:

            kategori_transaksi = item["kategori"]

            subtotal = (
                item["harga"]
                * item["qty"]
            )

            total += subtotal

            keuntungan_item = (
                (
                    item["harga"]
                    - item["modal"]
                )
                * item["qty"]
            )

            total_keuntungan += keuntungan_item

            # =================================================
            # KURANGI STOK
            # =================================================
            for produk in self.app_data:

                if produk["nama"] == item["nama"]:

                    produk["stok"] -= item["qty"]

        transaksi = {
            "tanggal": QDate.currentDate().toString(
                "dd MMMM yyyy"
            ),
            "transaksi": f"TRX{len(self.data_penjualan)+1:03}",
            "pelanggan": "Umum",
            "kategori": kategori_transaksi,
            "total": f"Rp {total:,}".replace(",", "."),
            "status": "Selesai",
            "keuntungan": total_keuntungan
        }

        self.data_penjualan.append(
            transaksi
        )

        QMessageBox.information(
            self,
            "Berhasil",
            "Transaksi berhasil!"
        )

        self.keranjang.clear()

        self.refresh_produk()
        self.refresh_keranjang()
        self.refresh_riwayat()

        self.dashboard.refresh_dashboard()

        if hasattr(
            self.window(),
            "laporan_page"
        ):

            self.window().laporan_page.refresh_table()

        self.window().save_data()

        self.update_statistik()

    # =====================================================
    # RIWAYAT
    # =====================================================
    def refresh_riwayat(self):

        self.table_riwayat.setRowCount(0)

        for data in reversed(
            self.data_penjualan
        ):

            row = self.table_riwayat.rowCount()

            self.table_riwayat.insertRow(row)

            isi = [
                data["transaksi"],
                data["tanggal"],
                data.get("kategori", "-"),
                data["pelanggan"],
                data["total"],
                data["status"]
            ]

            for col, value in enumerate(isi):

                item = QTableWidgetItem(
                    str(value)
                )

                item.setTextAlignment(
                    Qt.AlignCenter
                )

                self.table_riwayat.setItem(
                    row,
                    col,
                    item
                )

        self.update_statistik()

    # =====================================================
    # UPDATE CARD
    # =====================================================
    def update_statistik(self):

        total_transaksi = len(
            self.data_penjualan
        )

        total_penjualan = 0

        for data in self.data_penjualan:

            angka = (
                data["total"]
                .replace("Rp ", "")
                .replace(".", "")
            )

            total_penjualan += int(angka)

        total_produk = len(
            self.data_penjualan
        )

        self.transaksi_value.setText(
            str(total_transaksi)
        )

        self.penjualan_value.setText(
            f"Rp {total_penjualan:,}".replace(",", ".")
        )

        self.produk_value.setText(
            str(total_produk)
        )