from PySide6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout,
    QHBoxLayout, QFrame, QTableWidget, QTableWidgetItem,
    QHeaderView, QComboBox, QDateEdit, QScrollArea,
)
from PySide6.QtCore import Qt, QDate, QPropertyAnimation, QEasingCurve, QMargins
from PySide6.QtGui import QPainter, QColor, QPen

from PySide6.QtCharts import (
    QChart, QChartView, QLineSeries, QValueAxis,
)

from utils.styles import (
    PAGE_STYLE, CARD_STYLE, TABLE_STYLE, COMBO_STYLE,
    DATE_STYLE, BTN_PRIMARY_STYLE,
    COLOR_TEXT_DARK, COLOR_TEXT_MUTED,
)
from utils.storage import format_rupiah
from database.db   import penjualan_filter
from utils.exporter import export_laporan_pdf, export_penjualan_csv
from gui.detail_transaksi import DetailTransaksiDialog
from utils.kategori import KATEGORI_TRANSAKSI

class LaporanPenjualanPage(QWidget):
    def __init__(self, data_penjualan: list):
        super().__init__()
        self.data_penjualan = data_penjualan
        self._setup_ui()

    # UI
    def _setup_ui(self):
        self.setStyleSheet(PAGE_STYLE)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setStyleSheet("QScrollArea { border: none; background: #f4f7fb; }")

        self._scroll = scroll
        self._anim   = QPropertyAnimation(scroll.verticalScrollBar(), b"value")
        self._anim.setDuration(350)
        self._anim.setEasingCurve(QEasingCurve.OutCubic)
        scroll.wheelEvent = self._smooth_wheel

        main_layout.addWidget(scroll)

        container = QWidget()
        scroll.setWidget(container)

        root = QVBoxLayout(container)
        root.setContentsMargins(28, 24, 28, 24)
        root.setSpacing(22)

        # Header
        h1  = QLabel("Laporan Penjualan")
        h1.setStyleSheet(f"font-size: 36px; font-weight: 800; color: {COLOR_TEXT_DARK}; background: transparent;")
        sub = QLabel("Lihat dan analisis laporan penjualan bisnis Anda")
        sub.setStyleSheet(f"color: {COLOR_TEXT_MUTED}; font-size: 14px; background: transparent;")
        root.addWidget(h1)
        root.addWidget(sub)

        # Kartu statistik
        cards_row = QHBoxLayout()
        cards_row.setSpacing(14)
        self._card_pendapatan, self._val_pendapatan = self._make_card("Total Pendapatan", "Rp 0",  "💰", "#14b8a6")
        self._card_transaksi,  self._val_transaksi  = self._make_card("Total Transaksi",  "0",     "🛒", "#3b82f6")
        self._card_item,       self._val_item        = self._make_card("Item Terjual",     "0",     "📦", "#84cc16")
        self._card_untung,     self._val_untung      = self._make_card("Keuntungan",       "Rp 0",  "📈", "#f59e0b")
        for c in [self._card_pendapatan, self._card_transaksi, self._card_item, self._card_untung]:
            cards_row.addWidget(c)
        root.addLayout(cards_row)

        # Filter
        root.addWidget(self._build_filter_card())

        # Grafik
        root.addWidget(self._build_chart_card())

        # Tabel
        root.addWidget(self._build_table_card())

        self.refresh_table()

    # ----------------------------------------------------------
    def _make_card(self, title, value, icon, color):
        card = QFrame()
        card.setMinimumHeight(110)
        card.setStyleSheet(f"""
            QFrame {{
                background: white;
                border-radius: 18px;
                border: 1px solid #e5e7eb;
            }}
        """)
        layout = QHBoxLayout(card)
        layout.setContentsMargins(16, 16, 16, 16)

        icon_lbl = QLabel(icon)
        icon_lbl.setAlignment(Qt.AlignCenter)
        icon_lbl.setStyleSheet(f"""
            QLabel {{
                background: {color}22;
                color: {color};
                font-size: 22px;
                min-width: 54px; max-width: 54px;
                min-height: 54px; max-height: 54px;
                border-radius: 27px;
            }}
        """)

        text = QVBoxLayout()
        text.setSpacing(4)

        t_lbl = QLabel(title)
        t_lbl.setStyleSheet(f"color: {COLOR_TEXT_MUTED}; font-size: 12px; font-weight: 600; background: transparent;")
        v_lbl = QLabel(value)
        v_lbl.setStyleSheet(f"color: {color}; font-size: 22px; font-weight: 800; background: transparent;")
        text.addWidget(t_lbl)
        text.addWidget(v_lbl)

        layout.addWidget(icon_lbl)
        layout.addSpacing(12)
        layout.addLayout(text)
        return card, v_lbl

    # ----------------------------------------------------------
    def _build_filter_card(self) -> QFrame:
        card = QFrame()
        card.setFixedHeight(76)
        card.setStyleSheet(CARD_STYLE)
        layout = QHBoxLayout(card)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(12)

        # Label
        filter_lbl = QLabel("Filter:")
        filter_lbl.setStyleSheet(f"font-size: 14px; font-weight: bold; color: {COLOR_TEXT_DARK}; background: transparent;")
        layout.addWidget(filter_lbl)

        # Filter tanggal MULAI
        self._date_dari = QDateEdit()
        self._date_dari.setDate(QDate.currentDate().addDays(-30))
        self._date_dari.setCalendarPopup(True)
        self._date_dari.setFixedSize(140, 38)
        self._date_dari.setStyleSheet(DATE_STYLE)
        self._date_dari.dateChanged.connect(self.refresh_table)

        sd_lbl = QLabel("s/d")
        sd_lbl.setStyleSheet(f"color: {COLOR_TEXT_MUTED}; background: transparent;")

        # Filter tanggal SAMPAI
        self._date_sampai = QDateEdit()
        self._date_sampai.setDate(QDate.currentDate())
        self._date_sampai.setCalendarPopup(True)
        self._date_sampai.setFixedSize(140, 38)
        self._date_sampai.setStyleSheet(DATE_STYLE)
        self._date_sampai.dateChanged.connect(self.refresh_table)

        # Filter kategori
        self._combo_filter = QComboBox()
        self._combo_filter.addItems(["Semua Kategori"] + KATEGORI_TRANSAKSI)
        self._combo_filter.setFixedSize(180, 38)
        self._combo_filter.setStyleSheet(COMBO_STYLE)
        self._combo_filter.currentIndexChanged.connect(self.refresh_table)

        # Tombol reset filter
        reset_btn = QPushButton("🔄 Reset")
        reset_btn.setFixedHeight(38)
        reset_btn.setStyleSheet("""
            QPushButton {
                background: #f3f4f6;
                color: #111827;
                border: 1px solid #e5e7eb;
                border-radius: 8px;
                padding: 0 16px;
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton:hover { background: #e5e7eb; }
        """)
        reset_btn.clicked.connect(self._reset_filter)

        layout.addWidget(self._date_dari)
        layout.addWidget(sd_lbl)
        layout.addWidget(self._date_sampai)
        layout.addSpacing(8)
        layout.addWidget(self._combo_filter)
        layout.addWidget(reset_btn)
        layout.addStretch()
        return card

    # ----------------------------------------------------------
    def _build_chart_card(self) -> QFrame:
        card = QFrame()
        card.setFixedHeight(320)
        card.setStyleSheet(CARD_STYLE)
        layout = QVBoxLayout(card)
        layout.setContentsMargins(22, 22, 22, 22)
        layout.setSpacing(14)

        title = QLabel("📈 Grafik Pendapatan")
        title.setStyleSheet(f"font-size: 20px; font-weight: 800; color: {COLOR_TEXT_DARK}; background: transparent;")
        layout.addWidget(title)

        self._series = QLineSeries()
        pen = QPen(QColor("#14b8a6"))
        pen.setWidth(3)
        self._series.setPen(pen)

        chart = QChart()
        chart.addSeries(self._series)
        chart.setBackgroundVisible(False)
        chart.legend().hide()
        chart.setMargins(QMargins(8, 8, 8, 8))

        self._axis_x = QValueAxis()
        self._axis_y = QValueAxis()
        self._axis_x.setLabelFormat("%d")
        self._axis_y.setLabelFormat("%d")
        self._axis_x.setGridLineVisible(False)
        self._axis_y.setGridLineVisible(True)
        self._axis_x.setLabelsColor(QColor("#374151"))
        self._axis_y.setLabelsColor(QColor("#374151"))

        chart.addAxis(self._axis_x, Qt.AlignBottom)
        chart.addAxis(self._axis_y, Qt.AlignLeft)
        self._series.attachAxis(self._axis_x)
        self._series.attachAxis(self._axis_y)

        self._chart_view = QChartView(chart)
        self._chart_view.setRenderHint(QPainter.Antialiasing)
        self._chart_view.setStyleSheet("background: white; border: none;")
        layout.addWidget(self._chart_view)
        return card

    # ----------------------------------------------------------
    def _build_table_card(self) -> QFrame:
        card = QFrame()
        card.setStyleSheet(CARD_STYLE)
        layout = QVBoxLayout(card)
        layout.setContentsMargins(26, 26, 26, 26)
        layout.setSpacing(16)

        title_row = QHBoxLayout()
        title = QLabel("📋 Riwayat Penjualan")
        title.setStyleSheet(f"font-size: 22px; font-weight: 800; color: {COLOR_TEXT_DARK}; background: transparent;")
        title_row.addWidget(title)
        title_row.addStretch()

        csv_btn = QPushButton("📄  Export CSV")
        csv_btn.setFixedHeight(38)
        csv_btn.setStyleSheet("""
            QPushButton {
                background: #f3f4f6; color: #111827;
                border: 1px solid #e5e7eb; border-radius: 8px;
                padding: 0 16px; font-size: 13px; font-weight: bold;
            }
            QPushButton:hover { background: #e5e7eb; }
        """)
        csv_btn.clicked.connect(self._export_csv)
        title_row.addWidget(csv_btn)

        pdf_btn = QPushButton("📑  Export PDF")
        pdf_btn.setFixedHeight(38)
        pdf_btn.setStyleSheet("""
            QPushButton {
                background: #14b8a6; color: white;
                border: none; border-radius: 8px;
                padding: 0 16px; font-size: 13px; font-weight: bold;
            }
            QPushButton:hover { background: #0f766e; }
        """)
        pdf_btn.clicked.connect(self._export_pdf)
        title_row.addWidget(pdf_btn)
        layout.addLayout(title_row)

        self._table = QTableWidget(0, 7)
        self._table.setHorizontalHeaderLabels([
            "No Transaksi", "Tanggal", "Kategori", "Total", "Keuntungan", "Status", "Detail"
        ])
        self._table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self._table.horizontalHeader().setSectionResizeMode(6, QHeaderView.Fixed)
        self._table.setColumnWidth(6, 90)
        self._table.verticalHeader().setVisible(False)
        self._table.verticalHeader().setDefaultSectionSize(48)
        self._table.setAlternatingRowColors(True)
        self._table.setEditTriggers(QTableWidget.NoEditTriggers)
        self._table.setSelectionMode(QTableWidget.NoSelection)
        self._table.setShowGrid(False)
        self._table.setMinimumHeight(380)
        self._table.setSortingEnabled(True)
        self._table.setStyleSheet(TABLE_STYLE)
        layout.addWidget(self._table)
        return card

    # REFRESH TABLE
    def refresh_table(self):
        self._table.setSortingEnabled(False)
        self._table.setRowCount(0)
        self._series.clear()

        tanggal_dari   = self._date_dari.date()
        tanggal_sampai = self._date_sampai.date()
        kat_filter     = self._combo_filter.currentText()

        filtered = []
        for t in self.data_penjualan:
            # Filter kategori
            if kat_filter != "Semua Kategori" and t.get("kategori", "-") != kat_filter:
                continue

            # Filter tanggal
            tanggal_str = t.get("tanggal", "")
            tgl = QDate.fromString(tanggal_str, "yyyy-MM-dd")
            if tgl.isValid():
                if tgl < tanggal_dari or tgl > tanggal_sampai:
                    continue

            filtered.append(t)

        chart_data = sorted(
            filtered,
            key=lambda t: QDate.fromString(t.get("tanggal", ""), "yyyy-MM-dd"),
        )

        # Update grafik
        for i, t in enumerate(chart_data):
            self._series.append(i, t.get("total", 0))

        if chart_data:
            max_total = max(t.get("total", 0) for t in chart_data)
            self._axis_x.setRange(0, max(len(chart_data), 1))
            self._axis_y.setRange(0, max_total + 10000)
        else:
            self._axis_x.setRange(0, 1)
            self._axis_y.setRange(0, 100000)

        # Update tabel
        total_pendapatan = 0
        total_keuntungan = 0
        total_item       = 0

        for t in reversed(filtered):
            row = self._table.rowCount()
            self._table.insertRow(row)

            total_val   = t.get("total", 0)
            untung_val  = t.get("keuntungan", 0)
            total_pendapatan += total_val
            total_keuntungan += untung_val

            # Hitung item dari data transaksi
            total_item += sum(i.get("qty", 0) for i in t.get("items", []))

            for col, val in enumerate([
                t.get("no_transaksi") or t.get("transaksi", "-"),
                t.get("tanggal", "-"),
                t.get("kategori", "-"),
                format_rupiah(total_val),
                format_rupiah(untung_val),
                t.get("status", "-"),
            ]):
                item = QTableWidgetItem(str(val))
                item.setTextAlignment(Qt.AlignCenter)
                item.setForeground(QColor(COLOR_TEXT_DARK))
                if col == 5 and val == "Selesai":
                    item.setForeground(QColor("#16a34a"))
                self._table.setItem(row, col, item)

            self._table.setCellWidget(row, 6, self._make_detail_btn(t))

        # Update kartu statistik
        self._val_pendapatan.setText(format_rupiah(total_pendapatan))
        self._val_transaksi.setText(str(len(filtered)))
        self._val_item.setText(str(total_item))
        self._val_untung.setText(format_rupiah(total_keuntungan))

        self._table.setSortingEnabled(True)

    # ----------------------------------------------------------
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

    # ----------------------------------------------------------
    def _reset_filter(self):
        self._date_dari.setDate(QDate.currentDate().addDays(-30))
        self._date_sampai.setDate(QDate.currentDate())
        self._combo_filter.setCurrentIndex(0)
        self.refresh_table()

    # SMOOTH SCROLL
    def _smooth_wheel(self, event):
        bar   = self._scroll.verticalScrollBar()
        delta = event.angleDelta().y()
        step  = 200
        new_val = bar.value() + (-step if delta > 0 else step)
        self._anim.stop()
        self._anim.setStartValue(bar.value())
        self._anim.setEndValue(new_val)
        self._anim.start()
        event.accept()

    # EXPORT
    def _export_csv(self):
        from PySide6.QtWidgets import QMessageBox
        dari   = self._date_dari.date().toString("yyyy-MM-dd")
        sampai = self._date_sampai.date().toString("yyyy-MM-dd")
        kat    = self._combo_filter.currentText()
        try:
            path = export_penjualan_csv(
                self.data_penjualan, dari=dari, sampai=sampai, kategori=kat
            )
            QMessageBox.information(self, "Export Berhasil",
                                    f"File CSV disimpan di:\n{path}")
        except Exception as e:
            QMessageBox.critical(self, "Export Gagal", str(e))

    def _export_pdf(self):
        from PySide6.QtWidgets import QMessageBox
        from utils.auth import load_credentials
        dari   = self._date_dari.date().toString("yyyy-MM-dd")
        sampai = self._date_sampai.date().toString("yyyy-MM-dd")
        kat    = self._combo_filter.currentText()
        creds  = load_credentials()
        try:
            path = export_laporan_pdf(
                self.data_penjualan,
                dari=dari, sampai=sampai, kategori=kat,
                nama_toko=creds.get("nama_toko", "UMKM Stock"),
            )
            QMessageBox.information(self, "Export Berhasil",
                                    f"File PDF disimpan di:\n{path}")
        except Exception as e:
            QMessageBox.critical(self, "Export Gagal", str(e))