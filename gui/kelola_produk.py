from PySide6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout,
    QHBoxLayout, QFrame, QLineEdit, QComboBox,
    QTableWidget, QTableWidgetItem, QHeaderView,
    QMessageBox, QScrollArea, QDialog, QDialogButtonBox,
    QStackedWidget,
)
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QSortFilterProxyModel
from PySide6.QtGui  import QColor, QCursor

from utils.styles import (
    PAGE_STYLE, CARD_STYLE, INPUT_STYLE, COMBO_STYLE,
    TABLE_STYLE, BTN_PRIMARY_STYLE, BTN_SECONDARY_STYLE,
    COLOR_TEXT_DARK, COLOR_TEXT_MUTED, COLOR_PRIMARY,
)
from database.db import (
    produk_get_all, produk_insert, produk_update,
    produk_delete, produk_search, pembelian_get_all,
)
from utils.storage import format_rupiah

# DIALOG — Tambah / Edit Produk
class ProdukDialog(QDialog):
    KATEGORI = ["Makanan", "Minuman", "Snack", "Lainnya"]

    def __init__(self, parent=None, produk: dict | None = None):
        super().__init__(parent)
        self._produk = produk
        self.setWindowTitle("Edit Produk" if produk else "Tambah Produk Baru")
        self.setFixedWidth(520)
        self.setModal(True)
        self.setStyleSheet(f"""
            QDialog  {{ background:#f8fafc; font-family:'Segoe UI'; }}
            QLabel   {{ color:{COLOR_TEXT_DARK}; background:transparent; border:none; }}
        """)
        self._setup_ui()
        if produk:
            self._fill(produk)

    # ----------------------------------------------------------
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 28, 28, 24)
        layout.setSpacing(14)

        title = QLabel("Edit Produk" if self._produk else "Tambah Produk Baru")
        title.setStyleSheet(f"font-size:20px; font-weight:800; color:{COLOR_TEXT_DARK};")
        layout.addWidget(title)

        # Field-field
        self._nama_inp     = self._field(layout, "Nama Produk",   "Nama produk")
        self._harga_inp    = self._field(layout, "Harga (Rp)",    "Contoh: 15000")
        self._modal_inp    = self._field(layout, "Modal (Rp)",    "Contoh: 8000")
        self._stok_inp     = self._field(layout, "Stok",          "Jumlah stok")
        self._satuan_inp   = self._field(layout, "Satuan",        "pcs / kg / liter")

        # Kategori combo
        cat_lbl = QLabel("Kategori")
        cat_lbl.setStyleSheet(f"font-size:13px; font-weight:600; color:{COLOR_TEXT_DARK};")
        layout.addWidget(cat_lbl)
        self._kat_inp = QComboBox()
        self._kat_inp.addItems(self.KATEGORI)
        self._kat_inp.setFixedHeight(44)
        self._kat_inp.setStyleSheet(COMBO_STYLE)
        layout.addWidget(self._kat_inp)

        # Tombol OK / Batal
        layout.addSpacing(6)
        btns = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        btns.button(QDialogButtonBox.Ok).setText("💾  Simpan")
        btns.button(QDialogButtonBox.Cancel).setText("Batal")
        btns.button(QDialogButtonBox.Ok).setStyleSheet(BTN_PRIMARY_STYLE)
        btns.button(QDialogButtonBox.Cancel).setStyleSheet(BTN_SECONDARY_STYLE)
        btns.accepted.connect(self._validate_and_accept)
        btns.rejected.connect(self.reject)
        layout.addWidget(btns)

    def _field(self, layout: QVBoxLayout, label: str, placeholder: str) -> QLineEdit:
        lbl = QLabel(label)
        lbl.setStyleSheet(f"font-size:13px; font-weight:600; color:{COLOR_TEXT_DARK};")
        layout.addWidget(lbl)
        inp = QLineEdit()
        inp.setPlaceholderText(placeholder)
        inp.setFixedHeight(44)
        inp.setStyleSheet(INPUT_STYLE)
        layout.addWidget(inp)
        return inp

    def _fill(self, p: dict):
        self._nama_inp.setText(p.get("nama", ""))
        self._harga_inp.setText(str(p.get("harga", "")))
        self._modal_inp.setText(str(p.get("modal", "")))
        self._stok_inp.setText(str(p.get("stok", "")))
        self._satuan_inp.setText(p.get("satuan", ""))
        kat = p.get("kategori", "")
        if kat in self.KATEGORI:
            self._kat_inp.setCurrentText(kat)

    # Validasi data produk
    def _validate_and_accept(self):
        nama   = self._nama_inp.text().strip()
        harga_t = self._harga_inp.text().strip()
        modal_t = self._modal_inp.text().strip()
        stok_t  = self._stok_inp.text().strip()
        satuan  = self._satuan_inp.text().strip()

        if not all([nama, harga_t, modal_t, stok_t, satuan]):
            QMessageBox.warning(self, "Tidak Lengkap", "Semua field wajib diisi.")
            return
        try:
            harga = int(harga_t)
            modal = int(modal_t)
            stok  = int(stok_t)
        except ValueError:
            QMessageBox.warning(self, "Format Salah",
                                "Harga, modal, dan stok harus berupa angka bulat.")
            return
        if harga <= 0 or modal <= 0:
            QMessageBox.warning(self, "Nilai Tidak Valid",
                                "Harga dan modal harus lebih dari 0.")
            return
        if stok < 0:
            QMessageBox.warning(self, "Nilai Tidak Valid", "Stok tidak boleh negatif.")
            return
        if modal > harga:
            if QMessageBox.question(
                self, "Peringatan",
                "Modal lebih besar dari harga jual. Lanjutkan?",
                QMessageBox.Yes | QMessageBox.No,
            ) == QMessageBox.No:
                return
        self.accept()

    # Ambil nilai yang sudah divalidasi
    def get_data(self) -> dict:
        return {
            "nama":     self._nama_inp.text().strip(),
            "kategori": self._kat_inp.currentText(),
            "harga":    int(self._harga_inp.text()),
            "modal":    int(self._modal_inp.text()),
            "stok":     int(self._stok_inp.text()),
            "satuan":   self._satuan_inp.text().strip(),
        }

# HALAMAN KELOLA PRODUK
class KelolaProdukPage(QWidget):
    IDX_PRODUK   = 0
    IDX_RIWAYAT  = 1

    def __init__(self, data_produk: list, dashboard):
        super().__init__()
        self.data_produk   = data_produk
        self.dashboard     = dashboard
        self.filtered_data = []
        self._setup_ui()

    # ==========================================================
    def _setup_ui(self):
        self.setStyleSheet(PAGE_STYLE)

        main = QVBoxLayout(self)
        main.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setStyleSheet("QScrollArea { border:none; background:#f4f7fb; }")

        self._scroll = scroll
        self._anim   = QPropertyAnimation(scroll.verticalScrollBar(), b"value")
        self._anim.setDuration(250)
        self._anim.setEasingCurve(QEasingCurve.OutCubic)
        scroll.wheelEvent = self._smooth_wheel
        main.addWidget(scroll)

        container = QWidget()
        scroll.setWidget(container)

        root = QVBoxLayout(container)
        root.setContentsMargins(30, 28, 30, 28)
        root.setSpacing(24)

        h1 = QLabel("Kelola Produk")
        h1.setStyleSheet(f"font-size:36px; font-weight:800; color:{COLOR_TEXT_DARK};")
        sub = QLabel("Kelola data produk, stok, dan informasi produk Anda")
        sub.setStyleSheet(f"color:{COLOR_TEXT_MUTED}; font-size:14px;")

        root.addWidget(h1)
        root.addWidget(sub)
        root.addWidget(self._build_tab_bar())

        self._stack = QStackedWidget()
        self._stack.addWidget(self._build_table_card())
        self._stack.addWidget(self._build_riwayat_card())
        root.addWidget(self._stack)

        self._refresh_table()
        self._refresh_riwayat_pembelian()

    # ----------------------------------------------------------
    def _build_tab_bar(self) -> QFrame:
        bar = QFrame()
        bar.setFixedHeight(54)
        bar.setStyleSheet("""
            QFrame { background:white; border-radius:14px; border:1px solid #e5e7eb; }
            QLabel { background:transparent; border:none; }
            QPushButton { border:none; }
        """)
        layout = QHBoxLayout(bar)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(6)

        self._tab_produk  = QPushButton("📦  Daftar Produk")
        self._tab_riwayat = QPushButton("🧾  Riwayat Pembelian Stok")

        for btn in [self._tab_produk, self._tab_riwayat]:
            btn.setMinimumHeight(36)
            btn.setCursor(QCursor(Qt.PointingHandCursor))

        self._tab_produk.clicked.connect(lambda: self._show_tab(self.IDX_PRODUK))
        self._tab_riwayat.clicked.connect(lambda: self._show_tab(self.IDX_RIWAYAT))

        layout.addWidget(self._tab_produk)
        layout.addWidget(self._tab_riwayat)
        layout.addStretch()

        self._refresh_tab_style(self.IDX_PRODUK)
        return bar

    def _tab_style(self, active: bool) -> str:
        if active:
            return f"""
                QPushButton {{
                    background:{COLOR_PRIMARY}; color:white; border-radius:10px;
                    font-size:14px; font-weight:bold; padding:0 22px;
                }}
            """
        return f"""
            QPushButton {{
                background:transparent; color:{COLOR_TEXT_MUTED}; border-radius:10px;
                font-size:14px; padding:0 22px;
            }}
            QPushButton:hover {{ background:#f3f4f6; color:{COLOR_TEXT_DARK}; }}
        """

    def _refresh_tab_style(self, active_idx: int):
        self._tab_produk.setStyleSheet(self._tab_style(active_idx == self.IDX_PRODUK))
        self._tab_riwayat.setStyleSheet(self._tab_style(active_idx == self.IDX_RIWAYAT))

    def _show_tab(self, idx: int):
        self._stack.setCurrentIndex(idx)
        self._refresh_tab_style(idx)
        if idx == self.IDX_RIWAYAT:
            self._refresh_riwayat_pembelian()

    # ==========================================================
    def _build_table_card(self) -> QFrame:
        card = QFrame()
        card.setStyleSheet(CARD_STYLE)
        layout = QVBoxLayout(card)
        layout.setContentsMargins(28, 28, 28, 28)
        layout.setSpacing(16)

        # Header baris: judul + tombol Tambah
        top_row = QHBoxLayout()
        title = QLabel("📦 Daftar Produk")
        title.setStyleSheet(f"font-size:22px; font-weight:700; color:{COLOR_TEXT_DARK};")
        top_row.addWidget(title)
        top_row.addStretch()

        refresh_btn = QPushButton("🔄  Refresh")
        refresh_btn.setFixedHeight(42)
        refresh_btn.setCursor(QCursor(Qt.PointingHandCursor))
        refresh_btn.setStyleSheet(BTN_SECONDARY_STYLE)
        refresh_btn.clicked.connect(self._refresh_from_db)
        top_row.addWidget(refresh_btn)

        tambah_btn = QPushButton("➕  Tambah Produk")
        tambah_btn.setFixedHeight(42)
        tambah_btn.setStyleSheet(BTN_PRIMARY_STYLE)
        tambah_btn.clicked.connect(self._dialog_tambah)
        top_row.addWidget(tambah_btn)
        layout.addLayout(top_row)

        # Search
        self._search_inp = QLineEdit()
        self._search_inp.setPlaceholderText("🔍 Cari nama produk...")
        self._search_inp.setFixedHeight(44)
        self._search_inp.setMaximumWidth(320)
        self._search_inp.setStyleSheet(INPUT_STYLE)
        self._search_inp.textChanged.connect(self._refresh_table)
        layout.addWidget(self._search_inp)

        # Tabel dengan sorting
        self._table = QTableWidget(0, 10)
        self._table.setHorizontalHeaderLabels([
            "No", "Nama Produk", "Kategori",
            "Harga", "Modal", "Stok", "Satuan", "Status",
            "Edit", "Hapus",
        ])
        hh = self._table.horizontalHeader()
        for col in range(8):
            hh.setSectionResizeMode(col, QHeaderView.Stretch)
        for col in (8, 9):
            hh.setSectionResizeMode(col, QHeaderView.Fixed)
        self._table.setColumnWidth(8, 100)
        self._table.setColumnWidth(9, 100)

        self._table.verticalHeader().setVisible(False)
        self._table.verticalHeader().setDefaultSectionSize(52)
        self._table.setAlternatingRowColors(True)
        self._table.setEditTriggers(QTableWidget.NoEditTriggers)
        self._table.setSelectionMode(QTableWidget.NoSelection)
        self._table.setShowGrid(False)
        self._table.setMinimumHeight(420)
        self._table.setStyleSheet(TABLE_STYLE)

        # SORTING
        self._table.setSortingEnabled(True)
        hh.setSortIndicatorShown(True)

        layout.addWidget(self._table)
        return card

    # ==========================================================
    def _refresh_table(self):
        keyword = self._search_inp.text().strip()

        # Ambil dari DB (search atau semua)
        if keyword:
            self.filtered_data = produk_search(keyword)
        else:
            self.filtered_data = list(self.data_produk)

        # Nonaktifkan sementara agar sorting tidak mengacaukan setCellWidget
        self._table.setSortingEnabled(False)
        self._table.setRowCount(0)

        for i, produk in enumerate(self.filtered_data):
            stok = produk["stok"]
            if stok <= 5:
                status, sc = "⚠ Hampir Habis", "#dc2626"
            elif stok <= 20:
                status, sc = "🟡 Stok Rendah", "#d97706"
            else:
                status, sc = "✅ Stok Aman",   "#16a34a"

            row = self._table.rowCount()
            self._table.insertRow(row)

            data_cols = [
                str(i + 1),
                produk["nama"],
                produk["kategori"],
                f"Rp {produk['harga']:,}".replace(",", "."),
                f"Rp {produk['modal']:,}".replace(",", "."),
                str(stok),
                produk["satuan"],
                status,
            ]
            for col, val in enumerate(data_cols):
                item = QTableWidgetItem(val)
                item.setTextAlignment(Qt.AlignCenter)
                item.setForeground(QColor(sc if col == 7 else COLOR_TEXT_DARK))
                item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                self._table.setItem(row, col, item)

            self._table.setCellWidget(row, 8, self._make_btn(
                "✏  Edit", "#3b82f6", "#2563eb",
                lambda _, r=i: self._dialog_edit(r),
            ))
            self._table.setCellWidget(row, 9, self._make_btn(
                "🗑  Hapus", "#ef4444", "#dc2626",
                lambda _, r=i: self._hapus_produk(r),
            ))

        self._table.setSortingEnabled(True)

    # ----------------------------------------------------------
    def _make_btn(self, text, bg, hover, slot) -> QWidget:
        container = QWidget()
        container.setStyleSheet("background:transparent;")
        lay = QHBoxLayout(container)
        lay.setContentsMargins(6, 6, 6, 6)
        lay.setSpacing(0)
        btn = QPushButton(text)
        btn.setFixedHeight(32)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setStyleSheet(f"""
            QPushButton {{
                background:{bg}; color:white; border:none;
                border-radius:7px; font-size:12px; font-weight:bold; padding:0 8px;
            }}
            QPushButton:hover {{ background:{hover}; }}
        """)
        btn.clicked.connect(slot)
        lay.addWidget(btn)
        return container

    # DIALOG TAMBAH PRODUK
    def _dialog_tambah(self):
        dlg = ProdukDialog(self)
        if dlg.exec() != QDialog.Accepted:
            return
        d = dlg.get_data()
        new_id = produk_insert(d["nama"], d["kategori"], d["harga"],
                               d["modal"], d["stok"], d["satuan"])
        # Sinkronisasi list in-memory
        from database.db import produk_get_by_id
        self.data_produk.append(produk_get_by_id(new_id))
        self._after_change()
        QMessageBox.information(self, "Berhasil", f"Produk '{d['nama']}' berhasil ditambahkan.")

    # DIALOG EDIT PRODUK
    def _dialog_edit(self, row: int):
        if row >= len(self.filtered_data):
            return
        produk = self.filtered_data[row]
        dlg = ProdukDialog(self, produk=produk)
        if dlg.exec() != QDialog.Accepted:
            return
        d = dlg.get_data()
        produk_update(produk["id"], d["nama"], d["kategori"], d["harga"],
                      d["modal"], d["stok"], d["satuan"])
        # Sinkronisasi list in-memory
        from database.db import produk_get_by_id
        updated = produk_get_by_id(produk["id"])
        idx = next((i for i, p in enumerate(self.data_produk)
                    if p["id"] == produk["id"]), None)
        if idx is not None:
            self.data_produk[idx] = updated
        self._after_change()
        QMessageBox.information(self, "Berhasil", f"Produk '{d['nama']}' berhasil diperbarui.")

    # HAPUS PRODUK
    def _hapus_produk(self, row: int):
        if row >= len(self.filtered_data):
            return
        produk = self.filtered_data[row]
        if QMessageBox.question(
            self, "Konfirmasi Hapus",
            f"Yakin ingin menghapus produk '{produk['nama']}'?\nAksi ini tidak dapat dibatalkan.",
            QMessageBox.Yes | QMessageBox.No,
        ) == QMessageBox.No:
            return
        produk_delete(produk["id"])
        self.data_produk[:] = [p for p in self.data_produk if p["id"] != produk["id"]]
        self._after_change()

    # ==========================================================
    def _after_change(self):
        self._refresh_table()
        self._refresh_riwayat_pembelian()
        self.dashboard.refresh_dashboard()
        win = self.window()
        if hasattr(win, "penjualan_page"):
            win.penjualan_page.refresh_produk()

    # TOMBOL REFRESH
    def _refresh_from_db(self):
        self.data_produk[:] = produk_get_all()
        self._search_inp.clear()
        self._refresh_table()
        self.dashboard.refresh_dashboard()
        win = self.window()
        if hasattr(win, "penjualan_page"):
            win.penjualan_page.refresh_produk()

    # RIWAYAT PEMBELIAN STOK
    def _build_riwayat_card(self) -> QFrame:
        card = QFrame()
        card.setStyleSheet(CARD_STYLE)
        layout = QVBoxLayout(card)
        layout.setContentsMargins(28, 28, 28, 28)
        layout.setSpacing(16)

        top_row = QHBoxLayout()
        title = QLabel("🧾 Riwayat Pembelian Stok")
        title.setStyleSheet(f"font-size:22px; font-weight:700; color:{COLOR_TEXT_DARK};")
        top_row.addWidget(title)
        top_row.addStretch()

        refresh_btn = QPushButton("🔄  Refresh")
        refresh_btn.setFixedHeight(42)
        refresh_btn.setCursor(QCursor(Qt.PointingHandCursor))
        refresh_btn.setStyleSheet(BTN_SECONDARY_STYLE)
        refresh_btn.clicked.connect(self._refresh_riwayat_pembelian)
        top_row.addWidget(refresh_btn)
        layout.addLayout(top_row)

        desc = QLabel(
            "Mencatat setiap kali stok produk bertambah — baik saat produk "
            "baru ditambahkan maupun saat stok produk lama ditambah (restock)."
        )
        desc.setStyleSheet(f"color:{COLOR_TEXT_MUTED}; font-size:13px;")
        desc.setWordWrap(True)
        layout.addWidget(desc)

        self._riwayat_table = QTableWidget(0, 8)
        self._riwayat_table.setHorizontalHeaderLabels([
            "Tanggal", "Nama Produk", "Jenis", "Stok Lama",
            "Jumlah Ditambah", "Stok Baru", "Harga Modal", "Total Modal",
        ])
        hh = self._riwayat_table.horizontalHeader()
        hh.setSectionResizeMode(QHeaderView.Stretch)

        self._riwayat_table.verticalHeader().setVisible(False)
        self._riwayat_table.verticalHeader().setDefaultSectionSize(44)
        self._riwayat_table.setAlternatingRowColors(True)
        self._riwayat_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self._riwayat_table.setSelectionMode(QTableWidget.NoSelection)
        self._riwayat_table.setShowGrid(False)
        self._riwayat_table.setSortingEnabled(True)
        self._riwayat_table.setMinimumHeight(420)
        self._riwayat_table.setStyleSheet(TABLE_STYLE)
        layout.addWidget(self._riwayat_table)
        return card

    def _refresh_riwayat_pembelian(self):
        self._riwayat_table.setSortingEnabled(False)
        self._riwayat_table.setRowCount(0)

        for p in pembelian_get_all():
            row = self._riwayat_table.rowCount()
            self._riwayat_table.insertRow(row)

            jenis = p.get("jenis", "-")
            jenis_color = "#3b82f6" if jenis == "Baru" else "#f59e0b"

            cols = [
                p.get("dibuat_pada", "-"),
                p.get("nama_produk", "-"),
                jenis,
                str(p.get("stok_lama", 0)),
                f"+{p.get('jumlah_tambah', 0)}",
                str(p.get("stok_baru", 0)),
                format_rupiah(p.get("harga_modal", 0)),
                format_rupiah(p.get("total_modal", 0)),
            ]
            for col, val in enumerate(cols):
                item = QTableWidgetItem(val)
                item.setTextAlignment(Qt.AlignCenter)
                if col == 2:
                    item.setForeground(QColor(jenis_color))
                elif col == 4:
                    item.setForeground(QColor("#16a34a"))
                else:
                    item.setForeground(QColor(COLOR_TEXT_DARK))
                self._riwayat_table.setItem(row, col, item)

        self._riwayat_table.setSortingEnabled(True)

    # ==========================================================
    def _smooth_wheel(self, event):
        bar = self._scroll.verticalScrollBar()
        delta = event.angleDelta().y()
        target = bar.value() + (-200 if delta > 0 else 200)
        self._anim.stop()
        self._anim.setStartValue(bar.value())
        self._anim.setEndValue(target)
        self._anim.start()