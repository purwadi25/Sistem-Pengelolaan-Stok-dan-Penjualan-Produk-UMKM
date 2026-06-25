from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QFrame, QTableWidget, QTableWidgetItem, QHeaderView,
    QPushButton,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor

from utils.styles import (
    TABLE_STYLE, BTN_PRIMARY_STYLE,
    COLOR_TEXT_DARK, COLOR_TEXT_MUTED,
)
from utils.storage import format_rupiah

class DetailTransaksiDialog(QDialog):
    def __init__(self, parent=None, transaksi: dict | None = None):
        super().__init__(parent)
        self._t = transaksi or {}
        no_trx = self._t.get("no_transaksi") or self._t.get("transaksi", "-")
        self.setWindowTitle(f"Detail Transaksi — {no_trx}")
        self.setFixedWidth(560)
        self.setModal(True)
        self.setStyleSheet(f"""
            QDialog {{ background:#f8fafc; font-family:'Segoe UI'; }}
            QLabel  {{ color:{COLOR_TEXT_DARK}; background:transparent; border:none; }}
        """)
        self._setup_ui()

    # ----------------------------------------------------------
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 28, 28, 24)
        layout.setSpacing(4)

        no_trx = self._t.get("no_transaksi") or self._t.get("transaksi", "-")
        title = QLabel(f"🧾  Detail Transaksi")
        title.setStyleSheet(f"font-size:20px; font-weight:800; color:{COLOR_TEXT_DARK};")
        layout.addWidget(title)
        layout.addSpacing(12)

        # Info header dalam kartu
        info_card = QFrame()
        info_card.setStyleSheet("""
            QFrame { background:white; border-radius:12px; border:1px solid #e5e7eb; }
            QLabel { border:none; background:transparent; }
        """)
        info_layout = QVBoxLayout(info_card)
        info_layout.setContentsMargins(18, 16, 18, 16)
        info_layout.setSpacing(8)

        self._info_row(info_layout, "No Transaksi", no_trx)
        self._info_row(info_layout, "Tanggal",      self._t.get("tanggal", "-"))
        self._info_row(info_layout, "Kategori",     self._t.get("kategori", "-"))
        self._info_row(info_layout, "Pelanggan",    self._t.get("pelanggan", "-"))
        self._info_row(info_layout, "Status",       self._t.get("status", "-"))

        layout.addWidget(info_card)
        layout.addSpacing(16)

        # Tabel item
        item_title = QLabel("📦  Rincian Item")
        item_title.setStyleSheet(f"font-size:15px; font-weight:700; color:{COLOR_TEXT_DARK};")
        layout.addWidget(item_title)
        layout.addSpacing(6)

        items = self._t.get("items", [])
        table = QTableWidget(0, 4)
        table.setHorizontalHeaderLabels(["Produk", "Harga Satuan", "Qty", "Subtotal"])
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.verticalHeader().setVisible(False)
        table.setEditTriggers(QTableWidget.NoEditTriggers)
        table.setSelectionMode(QTableWidget.NoSelection)
        table.setShowGrid(False)
        table.setAlternatingRowColors(True)
        table.setFixedHeight(min(220, 44 + len(items) * 38))
        table.setStyleSheet(TABLE_STYLE)

        for item in items:
            row = table.rowCount()
            table.insertRow(row)
            for col, val in enumerate([
                item.get("nama_produk", "-"),
                format_rupiah(item.get("harga_satuan", 0)),
                str(item.get("qty", 0)),
                format_rupiah(item.get("subtotal", 0)),
            ]):
                cell = QTableWidgetItem(val)
                cell.setTextAlignment(Qt.AlignCenter)
                cell.setForeground(QColor(COLOR_TEXT_DARK))
                table.setItem(row, col, cell)

        layout.addWidget(table)
        layout.addSpacing(16)

        # Ringkasan total
        total_card = QFrame()
        total_card.setStyleSheet("""
            QFrame { background:#f0fdfa; border-radius:12px; border:none; }
            QLabel { border:none; background:transparent; }
        """)
        total_layout = QHBoxLayout(total_card)
        total_layout.setContentsMargins(18, 14, 18, 14)

        total_lbl = QLabel("Total Pembayaran")
        total_lbl.setStyleSheet(f"font-size:14px; color:{COLOR_TEXT_MUTED};")
        total_val = QLabel(format_rupiah(self._t.get("total", 0)))
        total_val.setStyleSheet("font-size:20px; font-weight:800; color:#0f766e;")

        total_layout.addWidget(total_lbl)
        total_layout.addStretch()
        total_layout.addWidget(total_val)
        layout.addWidget(total_card)
        layout.addSpacing(16)

        # Tombol tutup
        close_btn = QPushButton("Tutup")
        close_btn.setFixedHeight(42)
        close_btn.setStyleSheet(BTN_PRIMARY_STYLE)
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)

    # ----------------------------------------------------------
    def _info_row(self, layout: QVBoxLayout, label: str, value: str):
        row = QHBoxLayout()
        lbl = QLabel(label)
        lbl.setStyleSheet(f"font-size:13px; color:{COLOR_TEXT_MUTED};")
        lbl.setFixedWidth(110)
        val = QLabel(str(value))
        val.setStyleSheet(f"font-size:13px; font-weight:600; color:{COLOR_TEXT_DARK};")
        row.addWidget(lbl)
        row.addWidget(val)
        row.addStretch()
        layout.addLayout(row)