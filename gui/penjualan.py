from PySide6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout,
    QHBoxLayout, QFrame, QTableWidget, QTableWidgetItem,
    QHeaderView, QLineEdit, QMessageBox, QScrollArea,
)
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QColor

from utils.styles import (
    PAGE_STYLE, CARD_STYLE, INPUT_STYLE, TABLE_STYLE,
    BTN_PRIMARY_STYLE, COLOR_TEXT_DARK, COLOR_TEXT_MUTED,
)
from utils.storage import format_rupiah
from database.db   import (
    penjualan_insert, produk_update_stok, produk_get_all,
    penjualan_get_all,
)
from gui.detail_transaksi import DetailTransaksiDialog
from utils.kategori import hitung_kategori_gabungan

class PenjualanPage(QWidget):
    def __init__(self, data_produk: list, data_penjualan: list, dashboard):
        super().__init__()
        self.data_produk    = data_produk
        self.data_penjualan = data_penjualan
        self.dashboard      = dashboard
        self.keranjang: list = []
        self.filtered_produk: list = []
        self._setup_ui()

    # ==========================================================
    def _setup_ui(self):
        self.setStyleSheet(PAGE_STYLE)
        main = QVBoxLayout(self)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border:none; background:#f4f7fb; }")
        main.addWidget(scroll)

        container = QWidget()
        scroll.setWidget(container)

        root = QVBoxLayout(container)
        root.setContentsMargins(28, 24, 28, 24)
        root.setSpacing(22)

        h1  = QLabel("Penjualan")
        h1.setStyleSheet(f"font-size:32px; font-weight:bold; color:{COLOR_TEXT_DARK};")
        sub = QLabel("Kelola transaksi penjualan produk")
        sub.setStyleSheet(f"color:{COLOR_TEXT_MUTED}; font-size:14px;")
        root.addWidget(h1)
        root.addWidget(sub)

        # Stat cards
        cards_row = QHBoxLayout()
        cards_row.setSpacing(14)
        self._card_trx,  self._val_trx  = self._stat_card("Total Transaksi", "0",    "🛒", "#14b8a6")
        self._card_pend, self._val_pend = self._stat_card("Total Pendapatan", "Rp 0", "💰", "#3b82f6")
        self._card_item, self._val_item = self._stat_card("Item Terjual",     "0",    "📦", "#a855f7")
        for c in [self._card_trx, self._card_pend, self._card_item]:
            cards_row.addWidget(c)
        root.addLayout(cards_row)

        content_row = QHBoxLayout()
        content_row.setSpacing(18)
        content_row.addWidget(self._build_produk_card())
        content_row.addWidget(self._build_keranjang_card())
        root.addLayout(content_row)
        root.addWidget(self._build_riwayat_card())

        self.refresh_produk()
        self._refresh_riwayat()
        self._update_statistik()

    # ----------------------------------------------------------
    def _stat_card(self, title, value, icon, color):
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{ background:white; border-radius:16px; border:1px solid #e5e7eb; }}
            QLabel {{ background:transparent; border:none; }}
        """)
        lay = QHBoxLayout(card)
        lay.setContentsMargins(18, 18, 18, 18)
        icon_lbl = QLabel(icon)
        icon_lbl.setAlignment(Qt.AlignCenter)
        icon_lbl.setStyleSheet(f"""
            QLabel {{
                background:{color}22; color:{color}; font-size:26px;
                min-width:58px; max-width:58px; min-height:58px; max-height:58px;
                border-radius:29px;
            }}
        """)
        txt = QVBoxLayout()
        t = QLabel(title); t.setStyleSheet(f"color:{COLOR_TEXT_MUTED}; font-size:13px;")
        v = QLabel(value); v.setStyleSheet(f"color:{color}; font-size:26px; font-weight:bold;")
        txt.addWidget(t); txt.addWidget(v)
        lay.addWidget(icon_lbl); lay.addSpacing(12); lay.addLayout(txt)
        return card, v

    # ----------------------------------------------------------
    def _build_produk_card(self) -> QFrame:
        card = QFrame()
        card.setStyleSheet(CARD_STYLE)
        lay = QVBoxLayout(card)
        lay.setContentsMargins(20, 20, 20, 20)
        lay.setSpacing(12)

        title = QLabel("Daftar Produk")
        title.setStyleSheet(f"font-size:20px; font-weight:bold; color:{COLOR_TEXT_DARK};")
        lay.addWidget(title)

        self._search_inp = QLineEdit()
        self._search_inp.setPlaceholderText("🔍 Cari produk...")
        self._search_inp.setStyleSheet(INPUT_STYLE)
        self._search_inp.textChanged.connect(self.refresh_produk)
        lay.addWidget(self._search_inp)

        self._table_produk = QTableWidget(0, 5)
        self._table_produk.setHorizontalHeaderLabels(
            ["Nama Produk", "Kategori", "Harga", "Stok", "Aksi"])
        self._table_produk.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self._table_produk.setSortingEnabled(True)
        self._table_produk.verticalHeader().setVisible(False)
        self._table_produk.setEditTriggers(QTableWidget.NoEditTriggers)
        self._table_produk.setShowGrid(False)
        self._table_produk.setMinimumHeight(280)
        self._table_produk.setStyleSheet(TABLE_STYLE)
        self._table_produk.cellClicked.connect(self._handle_produk_click)
        lay.addWidget(self._table_produk)
        return card

    # ----------------------------------------------------------
    def _build_keranjang_card(self) -> QFrame:
        card = QFrame()
        card.setFixedWidth(420)
        card.setStyleSheet(CARD_STYLE)
        lay = QVBoxLayout(card)
        lay.setContentsMargins(20, 20, 20, 20)
        lay.setSpacing(12)

        title = QLabel("Keranjang Penjualan")
        title.setStyleSheet(f"font-size:20px; font-weight:bold; color:{COLOR_TEXT_DARK};")
        lay.addWidget(title)

        self._table_keranjang = QTableWidget(0, 4)
        self._table_keranjang.setHorizontalHeaderLabels(["Produk", "Qty", "Subtotal", "Hapus"])
        self._table_keranjang.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self._table_keranjang.verticalHeader().setVisible(False)
        self._table_keranjang.setEditTriggers(QTableWidget.NoEditTriggers)
        self._table_keranjang.setShowGrid(False)
        self._table_keranjang.setMinimumHeight(180)
        self._table_keranjang.setStyleSheet(TABLE_STYLE)
        self._table_keranjang.cellClicked.connect(self._handle_keranjang_click)
        lay.addWidget(self._table_keranjang)

        total_frame = QFrame()
        total_frame.setStyleSheet("QFrame { background:#f9fafb; border-radius:12px; border:none; } QLabel { border:none; }")
        tfl = QVBoxLayout(total_frame)
        tfl.setContentsMargins(14, 12, 14, 12)
        tl = QLabel("Total Bayar"); tl.setStyleSheet(f"font-size:13px; color:{COLOR_TEXT_MUTED};")
        self._total_bayar_lbl = QLabel("Rp 0")
        self._total_bayar_lbl.setStyleSheet("font-size:30px; font-weight:bold; color:#14b8a6;")
        tfl.addWidget(tl); tfl.addWidget(self._total_bayar_lbl)
        lay.addWidget(total_frame)

        bayar_btn = QPushButton("🛒 Proses Pembayaran")
        bayar_btn.setMinimumHeight(46)
        bayar_btn.setStyleSheet(BTN_PRIMARY_STYLE)
        bayar_btn.clicked.connect(self._proses_pembayaran)
        lay.addWidget(bayar_btn)
        return card

    # ----------------------------------------------------------
    def _build_riwayat_card(self) -> QFrame:
        card = QFrame()
        card.setStyleSheet(CARD_STYLE)
        lay = QVBoxLayout(card)
        lay.setContentsMargins(20, 20, 20, 20)
        lay.setSpacing(12)

        title = QLabel("Riwayat Transaksi")
        title.setStyleSheet(f"font-size:20px; font-weight:bold; color:{COLOR_TEXT_DARK};")
        lay.addWidget(title)

        self._table_riwayat = QTableWidget(0, 7)
        self._table_riwayat.setHorizontalHeaderLabels(
            ["No Transaksi", "Tanggal", "Kategori", "Pelanggan", "Total", "Status", "Detail"])
        self._table_riwayat.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self._table_riwayat.horizontalHeader().setSectionResizeMode(6, QHeaderView.Fixed)
        self._table_riwayat.setColumnWidth(6, 90)
        self._table_riwayat.setSortingEnabled(True)
        self._table_riwayat.verticalHeader().setVisible(False)
        self._table_riwayat.verticalHeader().setDefaultSectionSize(48)
        self._table_riwayat.setEditTriggers(QTableWidget.NoEditTriggers)
        self._table_riwayat.setSelectionMode(QTableWidget.NoSelection)
        self._table_riwayat.setShowGrid(False)
        self._table_riwayat.setMinimumHeight(220)
        self._table_riwayat.setStyleSheet(TABLE_STYLE)
        lay.addWidget(self._table_riwayat)
        return card

    # ==========================================================
    def refresh_produk(self):
        keyword = self._search_inp.text().lower()
        self.filtered_produk = [p for p in self.data_produk if keyword in p["nama"].lower()]
        self._table_produk.setSortingEnabled(False)
        self._table_produk.setRowCount(0)
        for produk in self.filtered_produk:
            row = self._table_produk.rowCount()
            self._table_produk.insertRow(row)
            for col, val in enumerate([
                produk["nama"], produk["kategori"],
                format_rupiah(produk["harga"]), str(produk["stok"]), "➕ Tambah",
            ]):
                item = QTableWidgetItem(val)
                item.setTextAlignment(Qt.AlignCenter)
                item.setForeground(QColor("#14b8a6" if col == 4 else COLOR_TEXT_DARK))
                self._table_produk.setItem(row, col, item)
        self._table_produk.setSortingEnabled(True)

    # ----------------------------------------------------------
    def _handle_produk_click(self, row, col):
        if col != 4:
            return
        # Perlu cari produk aktual dari baris terpilih (mungkin sudah disort)
        nama_item = self._table_produk.item(row, 0)
        if not nama_item:
            return
        nama = nama_item.text()
        produk = next((p for p in self.filtered_produk if p["nama"] == nama), None)
        if not produk:
            return
        if produk["stok"] <= 0:
            QMessageBox.warning(self, "Stok Habis", f"Stok '{produk['nama']}' sudah habis!")
            return
        for item in self.keranjang:
            if item["nama"] == produk["nama"]:
                if item["qty"] >= produk["stok"]:
                    QMessageBox.warning(self, "Melebihi Stok", f"Stok maksimal: {produk['stok']}.")
                    return
                item["qty"] += 1
                self._refresh_keranjang()
                return
        self.keranjang.append({
            "id": produk["id"], "nama": produk["nama"],
            "kategori": produk["kategori"], "harga": produk["harga"],
            "modal": produk["modal"], "qty": 1,
        })
        self._refresh_keranjang()

    # ----------------------------------------------------------
    def _refresh_keranjang(self):
        self._table_keranjang.setRowCount(0)
        total = 0
        for item in self.keranjang:
            subtotal = item["harga"] * item["qty"]
            total   += subtotal
            row = self._table_keranjang.rowCount()
            self._table_keranjang.insertRow(row)
            for col, val in enumerate([item["nama"], str(item["qty"]),
                                        format_rupiah(subtotal), "➖"]):
                cell = QTableWidgetItem(val)
                cell.setTextAlignment(Qt.AlignCenter)
                cell.setForeground(QColor("#ef4444" if col == 3 else COLOR_TEXT_DARK))
                self._table_keranjang.setItem(row, col, cell)
        self._total_bayar_lbl.setText(format_rupiah(total))

    def _handle_keranjang_click(self, row, col):
        if col != 3 or row >= len(self.keranjang):
            return
        item = self.keranjang[row]
        if item["qty"] > 1:
            item["qty"] -= 1
        else:
            self.keranjang.pop(row)
        self._refresh_keranjang()

    # ----------------------------------------------------------
    def _proses_pembayaran(self):
        if not self.keranjang:
            QMessageBox.warning(self, "Kosong", "Tambahkan produk ke keranjang dahulu.")
            return

        total = 0; total_untung = 0; items_db = []
        kategori_utama = hitung_kategori_gabungan(
            [item["kategori"] for item in self.keranjang]
        )

        for item in self.keranjang:
            subtotal = item["harga"] * item["qty"]
            untung   = (item["harga"] - item["modal"]) * item["qty"]
            total        += subtotal
            total_untung += untung
            items_db.append({
                "produk_id":   item["id"],
                "nama_produk": item["nama"],
                "harga_satuan":item["harga"],
                "qty":         item["qty"],
                "subtotal":    subtotal,
            })
            # Kurangi stok di DB
            for p in self.data_produk:
                if p["id"] == item["id"]:
                    new_stok = p["stok"] - item["qty"]
                    produk_update_stok(p["id"], new_stok)
                    p["stok"] = new_stok

        no_trx  = f"TRX{len(self.data_penjualan) + 1:04d}"
        tgl_iso = QDate.currentDate().toString("yyyy-MM-dd")

        pjl_id = penjualan_insert(
            no_trx, tgl_iso, "Umum", kategori_utama,
            total, total_untung, "Selesai", items_db,
        )
        # Sinkronisasi list in-memory
        self.data_penjualan[:] = penjualan_get_all()

        QMessageBox.information(self, "Berhasil",
                                f"Transaksi {no_trx} berhasil!\nTotal: {format_rupiah(total)}")
        self.keranjang.clear()
        self._refresh_keranjang()
        self.refresh_produk()
        self._refresh_riwayat()
        self._update_statistik()
        self.dashboard.refresh_dashboard()
        win = self.window()
        if hasattr(win, "laporan_page"):
            win.laporan_page.refresh_table()

    # ----------------------------------------------------------
    def _refresh_riwayat(self):
        self._table_riwayat.setSortingEnabled(False)
        self._table_riwayat.setRowCount(0)
        for t in self.data_penjualan:
            row = self._table_riwayat.rowCount()
            self._table_riwayat.insertRow(row)
            for col, val in enumerate([
                t.get("no_transaksi") or t.get("transaksi", "-"),
                t.get("tanggal", "-"),
                t.get("kategori", "-"),
                t.get("pelanggan", "-"),
                format_rupiah(t.get("total", 0)),
                t.get("status", "-"),
            ]):
                item = QTableWidgetItem(str(val))
                item.setTextAlignment(Qt.AlignCenter)
                item.setForeground(QColor("#16a34a" if (col == 5 and val == "Selesai")
                                          else COLOR_TEXT_DARK))
                self._table_riwayat.setItem(row, col, item)
            self._table_riwayat.setCellWidget(row, 6, self._make_detail_btn(t))
        self._table_riwayat.setSortingEnabled(True)

    def _make_detail_btn(self, transaksi: dict) -> QWidget:
        container = QWidget()
        container.setStyleSheet("background:transparent;")
        lay = QHBoxLayout(container)
        lay.setContentsMargins(6, 5, 6, 5)
        lay.setSpacing(0)

        btn = QPushButton("🔍 Detail")
        btn.setFixedHeight(34)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setStyleSheet("""
            QPushButton {
                background:#3b82f6; color:white; border:none;
                border-radius:7px; font-size:11px; font-weight:bold; padding:0 6px;
            }
            QPushButton:hover { background:#2563eb; }
        """)
        btn.clicked.connect(lambda _, t=transaksi: self._open_detail(t))
        lay.addWidget(btn)
        return container

    def _open_detail(self, transaksi: dict):
        dlg = DetailTransaksiDialog(self, transaksi=transaksi)
        dlg.exec()

    def _update_statistik(self):
        total_item = sum(
            sum(i.get("qty", 0) for i in t.get("items", []))
            for t in self.data_penjualan
        )
        self._val_trx.setText(str(len(self.data_penjualan)))
        self._val_pend.setText(format_rupiah(sum(t.get("total", 0) for t in self.data_penjualan)))
        self._val_item.setText(str(total_item))