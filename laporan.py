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

from PySide6.QtCore import (
    Qt,
    QDate,
    QPropertyAnimation,
    QEasingCurve,
    QMargins
)

from PySide6.QtGui import (
    QPainter,
    QColor,
    QPen
)

from PySide6.QtCharts import (
    QChart,
    QChartView,
    QLineSeries,
    QValueAxis
)


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
                background:#f4f7fb;
                font-family:'Segoe UI';
            }
        """)

        main_layout = QVBoxLayout(self)

        main_layout.setContentsMargins(
            0, 0, 0, 0
        )

        # =====================================================
        # SCROLL
        # =====================================================
        scroll = QScrollArea()

        scroll.setWidgetResizable(True)

        scroll.setHorizontalScrollBarPolicy(
            Qt.ScrollBarAlwaysOff
        )

        scroll.setVerticalScrollBarPolicy(
            Qt.ScrollBarAsNeeded
        )

        scroll.verticalScrollBar().setSingleStep(20)

        scroll.setStyleSheet("""
            QScrollArea{
                border:none;
                background:#f4f7fb;
            }
        """)

        main_layout.addWidget(scroll)

        # =====================================================
        # SMOOTH SCROLL
        # =====================================================
        self.scroll = scroll

        self.scroll_animation = QPropertyAnimation(
            scroll.verticalScrollBar(),
            b"value"
        )

        self.scroll_animation.setDuration(350)

        self.scroll_animation.setEasingCurve(
            QEasingCurve.OutCubic
        )

        scroll.wheelEvent = self.smooth_wheel_event

        # =====================================================
        # CONTAINER
        # =====================================================
        container = QWidget()

        scroll.setWidget(container)

        root = QVBoxLayout(container)

        root.setContentsMargins(
            30, 25, 30, 25
        )

        root.setSpacing(24)

        # =====================================================
        # HEADER
        # =====================================================
        title = QLabel("Laporan Penjualan")

        title.setStyleSheet("""
            font-size:40px;
            font-weight:800;
            color:#111827;
        """)

        subtitle = QLabel(
            "Lihat dan analisis laporan penjualan bisnis Anda"
        )

        subtitle.setStyleSheet("""
            color:#6b7280;
            font-size:15px;
        """)

        root.addWidget(title)
        root.addWidget(subtitle)

        # =====================================================
        # CARD STATISTIK
        # =====================================================
        cards_layout = QHBoxLayout()

        cards_layout.setSpacing(14)

        def create_card(title, value, icon, color):

            card = QFrame()

            card.setMinimumHeight(120)
            card.setMaximumHeight(120)

            card.setStyleSheet("""
                QFrame{
                    background:white;
                    border-radius:22px;
                    border:1px solid #e5e7eb;
                }
            """)

            layout = QHBoxLayout(card)

            layout.setContentsMargins(
                18, 18, 18, 18
            )

            icon_label = QLabel(icon)

            icon_label.setAlignment(
                Qt.AlignCenter
            )

            icon_label.setStyleSheet(f"""
                QLabel{{
                    background:{color}20;
                    color:{color};
                    font-size:24px;

                    min-width:58px;
                    max-width:58px;

                    min-height:58px;
                    max-height:58px;

                    border-radius:29px;
                    font-weight:bold;
                }}
            """)

            text_layout = QVBoxLayout()

            text_layout.setSpacing(5)

            title_label = QLabel(title)

            title_label.setStyleSheet("""
                color:#6b7280;
                font-size:13px;
                font-weight:600;
            """)

            value_label = QLabel(value)

            value_label.setStyleSheet(f"""
                color:{color};
                font-size:24px;
                font-weight:800;
            """)

            text_layout.addWidget(title_label)
            text_layout.addWidget(value_label)

            layout.addWidget(icon_label)
            layout.addSpacing(12)
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
            "#84cc16"
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
        # FILTER CARD
        # =====================================================
        filter_card = QFrame()

        filter_card.setFixedHeight(78)

        filter_card.setStyleSheet("""
            QFrame{
                background:white;
                border-radius:18px;
                border:1px solid #e5e7eb;
            }
        """)

        filter_layout = QHBoxLayout(filter_card)

        filter_layout.setContentsMargins(
            16, 14, 16, 14
        )

        filter_layout.setSpacing(10)

        # =====================================================
        # DATE FILTER
        # =====================================================
        self.date_filter = QDateEdit()

        self.date_filter.setDate(
            QDate.currentDate()
        )

        self.date_filter.setCalendarPopup(True)

        self.date_filter.setFixedSize(
            135,
            38
        )

        self.date_filter.setStyleSheet("""
            QDateEdit{
                border:1px solid #d1d5db;
                border-radius:10px;
                padding:6px 10px;
                background:white;
                font-size:13px;
                color:#111827;
            }

            QDateEdit:focus{
                border:1px solid #14b8a6;
            }
        """)

        # =====================================================
        # COMBO FILTER
        # =====================================================
        self.combo_filter = QComboBox()

        self.combo_filter.addItems([
            "Semua Produk",
            "Makanan",
            "Minuman",
            "Snack"
        ])

        self.combo_filter.currentIndexChanged.connect(
            self.refresh_table
        )

        self.combo_filter.setFixedSize(
            170,
            38
        )

        self.combo_filter.setStyleSheet("""
            QComboBox{
                border:1px solid #d1d5db;
                border-radius:10px;
                padding-left:10px;
                background:white;
                font-size:13px;
                color:#111827;
            }

            QComboBox:focus{
                border:1px solid #14b8a6;
            }

            QComboBox::drop-down{
                border:none;
                width:28px;
            }
        """)

        filter_layout.addWidget(
            self.date_filter
        )

        filter_layout.addWidget(
            self.combo_filter
        )

        filter_layout.addStretch()

        root.addWidget(filter_card)

        # =====================================================
        # GRAFIK CARD
        # =====================================================
        grafik_card = QFrame()

        grafik_card.setFixedHeight(340)

        grafik_card.setStyleSheet("""
            QFrame{
                background:white;
                border-radius:22px;
                border:1px solid #e5e7eb;
            }
        """)

        grafik_layout = QVBoxLayout(grafik_card)

        grafik_layout.setContentsMargins(
            24, 24, 24, 24
        )

        grafik_layout.setSpacing(18)

        grafik_title = QLabel(
            "📈 Grafik Penjualan"
        )

        grafik_title.setStyleSheet("""
            font-size:26px;
            font-weight:800;
            color:#111827;
        """)

        # =====================================================
        # CHART
        # =====================================================
        self.series = QLineSeries()

        pen = QPen(
            QColor("#14b8a6")
        )

        pen.setWidth(4)

        self.series.setPen(pen)

        chart = QChart()

        chart.addSeries(self.series)

        chart.setBackgroundVisible(False)

        chart.legend().hide()

        chart.setMargins(
            QMargins(10, 10, 10, 10)
        )

        axis_x = QValueAxis()
        axis_y = QValueAxis()

        axis_x.setLabelFormat("%d")
        axis_y.setLabelFormat("%d")

        axis_x.setGridLineVisible(False)
        axis_y.setGridLineVisible(True)

        axis_x.setLabelsColor(
            QColor("#6b7280")
        )

        axis_y.setLabelsColor(
            QColor("#6b7280")
        )

        chart.addAxis(
            axis_x,
            Qt.AlignBottom
        )

        chart.addAxis(
            axis_y,
            Qt.AlignLeft
        )

        self.series.attachAxis(axis_x)
        self.series.attachAxis(axis_y)

        self.axis_x = axis_x
        self.axis_y = axis_y

        self.chart_view = QChartView(chart)

        self.chart_view.setRenderHint(
            QPainter.Antialiasing
        )

        self.chart_view.setStyleSheet("""
            background:#ffffff;
            border:none;
        """)

        grafik_layout.addWidget(grafik_title)
        grafik_layout.addWidget(self.chart_view)

        root.addWidget(grafik_card)

        # =====================================================
        # TABLE CARD
        # =====================================================
        table_card = QFrame()

        table_card.setStyleSheet("""
            QFrame{
                background:white;
                border-radius:22px;
                border:1px solid #e5e7eb;
            }
        """)

        table_layout = QVBoxLayout(table_card)

        table_layout.setContentsMargins(
            28, 28, 28, 28
        )

        table_layout.setSpacing(20)

        title_table = QLabel(
            "📋 Riwayat Penjualan"
        )

        title_table.setStyleSheet("""
            font-size:26px;
            font-weight:800;
            color:#111827;
        """)

        table_layout.addWidget(title_table)

        # =====================================================
        # TABLE
        # =====================================================
        self.table = QTableWidget(0, 5)

        self.table.setHorizontalHeaderLabels([
            "No Transaksi",
            "Tanggal",
            "Kategori",
            "Total",
            "Status"
        ])

        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        self.table.verticalHeader().setVisible(False)

        self.table.setAlternatingRowColors(True)

        self.table.setMinimumHeight(420)

        self.table.setStyleSheet("""
            QTableWidget{
                border:none;
                background:white;
                font-size:14px;
                gridline-color:#f3f4f6;
                alternate-background-color:#f9fafb;
            }

            QTableWidget::item{
                padding:14px;
            }

            QTableWidget::item:selected{
                background:#dbeafe;
                color:#111827;
            }

            QHeaderView::section{
                background:#f3f4f6;
                color:#111827;
                padding:16px;
                border:none;
                font-size:14px;
                font-weight:700;
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
        total_keuntungan = 0

        kategori_filter = (
            self.combo_filter.currentText()
        )

        filtered_data = []

        # =====================================================
        # FILTER DATA
        # =====================================================
        for transaksi in self.data_penjualan:

            if (
                kategori_filter != "Semua Produk"
                and
                transaksi.get("kategori")
                != kategori_filter
            ):
                continue

            filtered_data.append(
                transaksi
            )

        # =====================================================
        # UPDATE CHART
        # =====================================================
        self.series.clear()

        for i, data in enumerate(filtered_data):

            angka = (
                data["total"]
                .replace("Rp ", "")
                .replace(".", "")
            )

            nilai = int(angka)

            self.series.append(
                i,
                nilai
            )

        # =====================================================
        # UPDATE AXIS
        # =====================================================
        if len(filtered_data) > 0:

            self.axis_x.setRange(
                0,
                len(filtered_data)
            )

            nilai_terbesar = max([
                int(
                    data["total"]
                    .replace("Rp ", "")
                    .replace(".", "")
                )
                for data in filtered_data
            ])

            self.axis_y.setRange(
                0,
                nilai_terbesar + 50000
            )

        else:

            self.axis_x.setRange(0, 1)

            self.axis_y.setRange(
                0,
                100000
            )

        # =====================================================
        # UPDATE TABLE
        # =====================================================
        for data in reversed(filtered_data):

            row = self.table.rowCount()

            self.table.insertRow(row)

            isi = [
                data["transaksi"],
                data["tanggal"],
                data.get("kategori", "-"),
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

                if (
                    col == 4 and
                    value == "Selesai"
                ):
                    item.setForeground(
                        QColor("#16a34a")
                    )

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

            if "keuntungan" in data:

                total_keuntungan += data["keuntungan"]

        # =====================================================
        # UPDATE CARD
        # =====================================================
        self.pendapatan_value.setText(
            f"Rp {total_pendapatan:,}".replace(",", ".")
        )

        self.transaksi_value.setText(
            str(len(filtered_data))
        )

        self.produk_value.setText(
            str(len(filtered_data))
        )

        self.keuntungan_value.setText(
            f"Rp {total_keuntungan:,}".replace(",", ".")
        )

    # =====================================================
    # SMOOTH SCROLL
    # =====================================================
    def smooth_wheel_event(self, event):

        scrollbar = (
            self.scroll.verticalScrollBar()
        )

        current_value = scrollbar.value()

        delta = event.angleDelta().y()

        scroll_amount = 180

        if delta > 0:

            new_value = (
                current_value - scroll_amount
            )

        else:

            new_value = (
                current_value + scroll_amount
            )

        self.scroll_animation.stop()

        self.scroll_animation.setDuration(350)

        self.scroll_animation.setStartValue(
            current_value
        )

        self.scroll_animation.setEndValue(
            new_value
        )

        self.scroll_animation.start()

        event.accept()