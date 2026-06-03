from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
    QLineEdit,
    QComboBox,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QMessageBox,
    QScrollArea
)

from PySide6.QtCore import (
    Qt,
    QPropertyAnimation,
    QEasingCurve,
    QDate
)
import sys


class KelolaProdukPage(QWidget):
    def __init__(self, app_data, dashboard):
        super().__init__()

        self.setWindowTitle("Kelola Produk UMKM")
        self.resize(1400, 850)

        self.data_produk = app_data
        self.dashboard = dashboard

        self.selected_row = None
        self.selected_produk = None
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
        main_layout.setContentsMargins(0,0,0,0)

        # =====================================================
        # SCROLL AREA
        # =====================================================
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

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

        self.scroll_animation.setDuration(250)

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
        root.setContentsMargins(0,0,0,0)

        # =====================================================
        # CONTENT
        # =====================================================
        content = QWidget()

        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(35, 30, 35, 30)
        content_layout.setSpacing(28)

        # =====================================================
        # HEADER
        # =====================================================
        title = QLabel("Kelola Produk")

        title.setStyleSheet("""
            font-size:42px;
            font-weight:800;
            color:#111827;
        """)

        subtitle = QLabel(
            "Kelola data produk, stok, dan informasi produk Anda"
        )

        subtitle.setStyleSheet("""
            color:#6b7280;
            font-size:16px;
        """)

        content_layout.addWidget(title)
        content_layout.addWidget(subtitle)

        # =====================================================
        # FORM CARD
        # =====================================================
        form_card = QFrame()

        form_card.setStyleSheet("""
            QFrame{
                background:white;
                border-radius:22px;
                border:1px solid #e5e7eb;
            }
        """)

        form_layout = QVBoxLayout(form_card)
        form_layout.setContentsMargins(30, 30, 30, 30)
        form_layout.setSpacing(22)

        form_title = QLabel("➕ Tambah / Edit Produk")

        form_title.setStyleSheet("""
            font-size:28px;
            font-weight:700;
            color:#111827;
        """)

        form_layout.addWidget(form_title)

        # =====================================================
        # INPUT STYLE
        # =====================================================
        def create_input(placeholder):

            inp = QLineEdit()
            inp.setPlaceholderText(placeholder)
            inp.setMinimumHeight(58)

            inp.setStyleSheet("""
                QLineEdit{
                    border:2px solid #e5e7eb;
                    border-radius:14px;
                    padding-left:16px;
                    padding-right:16px;
                    background:white;
                    font-size:14px;
                    color:#111827;
                }

                QLineEdit:focus{
                    border:2px solid #14b8a6;
                    background:#ffffff;
                }
            """)

            return inp

        # =====================================================
        # INPUTS
        # =====================================================
        self.nama_input = create_input("Nama Produk")
        self.harga_input = create_input("Harga")
        self.modal_input = create_input("Modal")
        self.stok_input = create_input("Stok")
        self.satuan_input = create_input("Satuan")

        self.kategori_input = QComboBox()

        self.kategori_input.addItems([
            "Pilih Kategori",
            "Makanan",
            "Minuman",
            "Snack",
            "Lainnya"
        ])

        self.kategori_input.setMinimumHeight(58)

        self.kategori_input.setStyleSheet("""
            QComboBox{
                border:2px solid #e5e7eb;
                border-radius:14px;
                padding-left:16px;
                background:white;
                font-size:14px;
                color:#111827;
            }

            QComboBox:focus{
                border:2px solid #14b8a6;
            }

            QComboBox::drop-down{
                border:none;
                width:35px;
            }
        """)

        # =====================================================
        # INPUT ROW
        # =====================================================
        input_row = QHBoxLayout()
        input_row.setSpacing(16)

        input_row.addWidget(self.nama_input)
        input_row.addWidget(self.kategori_input)
        input_row.addWidget(self.harga_input)
        input_row.addWidget(self.modal_input)
        input_row.addWidget(self.stok_input)
        input_row.addWidget(self.satuan_input)

        form_layout.addLayout(input_row)

        # =====================================================
        # BUTTON STYLE
        # =====================================================
        btn_row = QHBoxLayout()
        btn_row.setSpacing(14)

        self.simpan_btn = QPushButton("💾 Simpan Produk")

        self.simpan_btn.setMinimumHeight(52)

        self.simpan_btn.setStyleSheet("""
            QPushButton{
                background:#14b8a6;
                color:white;
                border:none;
                border-radius:14px;
                padding:0 28px;
                font-size:15px;
                font-weight:700;
            }

            QPushButton:hover{
                background:#0f766e;
            }
        """)

        self.simpan_btn.clicked.connect(
            self.simpan_produk
        )

        reset_btn = QPushButton("🔄 Bersihkan")

        reset_btn.setMinimumHeight(52)

        reset_btn.setStyleSheet("""
            QPushButton{
                background:#f3f4f6;
                color:#111827;
                border:none;
                border-radius:14px;
                padding:0 28px;
                font-size:15px;
                font-weight:700;
            }

            QPushButton:hover{
                background:#e5e7eb;
            }
        """)

        reset_btn.clicked.connect(
            self.reset_form
        )

        btn_row.addWidget(self.simpan_btn)
        btn_row.addWidget(reset_btn)
        btn_row.addStretch()

        form_layout.addLayout(btn_row)

        content_layout.addWidget(form_card)

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
        table_layout.setContentsMargins(30,30,30,30)
        table_layout.setSpacing(20)

        table_title = QLabel("📦 Daftar Produk")

        table_title.setStyleSheet("""
            font-size:28px;
            font-weight:700;
            color:#111827;
        """)

        table_layout.addWidget(table_title)

        # =====================================================
        # SEARCH
        # =====================================================
        self.search_input = QLineEdit()

        self.search_input.setPlaceholderText(
            "🔍 Cari produk..."
        )

        self.search_input.textChanged.connect(
            self.refresh_table
        )

        self.search_input.setMinimumHeight(54)
        self.search_input.setMaximumWidth(340)

        self.search_input.setStyleSheet("""
            QLineEdit{
                border:2px solid #e5e7eb;
                border-radius:14px;
                padding-left:16px;
                background:white;
                font-size:14px;
            }

            QLineEdit:focus{
                border:2px solid #14b8a6;
            }
        """)

        table_layout.addWidget(self.search_input)

        # =====================================================
        # TABLE
        # =====================================================
        self.table = QTableWidget(0, 8)

        self.table.setHorizontalHeaderLabels([
            "No",
            "Nama Produk",
            "Kategori",
            "Harga",
            "Stok",
            "Satuan",
            "Status",
            "Aksi"
        ])

        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        self.table.verticalHeader().setVisible(False)

        self.table.setAlternatingRowColors(True)

        self.table.setStyleSheet("""
            QTableWidget{
                border:none;
                background:white;
                font-size:14px;
                gridline-color:#f3f4f6;
                alternate-background-color:#f9fafb;
            }

            QTableWidget::item{
                padding:10px;
            }

            QHeaderView::section{
                background:#f3f4f6;
                color:#111827;
                padding:16px;
                border:none;
                font-size:14px;
                font-weight:700;
                border-radius:0px;
            }
        """)

        self.table.setMinimumHeight(420)

        self.table.cellClicked.connect(
            self.handle_table_click
        )

        table_layout.addWidget(self.table)

        content_layout.addWidget(table_card)

        root.addWidget(content)

        self.refresh_table()
    # =====================================================
    # SIMPAN PRODUK
    # =====================================================
    def simpan_produk(self):

        nama = self.nama_input.text()
        kategori = self.kategori_input.currentText()
        harga = self.harga_input.text()
        modal = self.modal_input.text()
        stok = self.stok_input.text()
        satuan = self.satuan_input.text()

        if (
            nama == "" or
            kategori == "Pilih Kategori" or
            harga == "" or
            modal == "" or
            stok == "" or
            satuan == ""
        ):

            QMessageBox.warning(
                self,
                "Error",
                "Semua field wajib diisi!"
            )

            return

        try:
            harga = int(harga)
            modal = int(modal)
            stok = int(stok)

        except:

            QMessageBox.warning(
                self,
                "Error",
                "Harga dan stok harus angka!"
            )

            return

        produk = {
            "nama": nama,
            "kategori": kategori,
            "harga": harga,
            "modal": modal,
            "stok": stok,
            "satuan": satuan
        }

        # EDIT
        if self.selected_row is not None:

            index_asli = self.data_produk.index(
                self.selected_produk
            )

            self.data_produk[index_asli] = produk

            QMessageBox.information(
                self,
                "Berhasil",
                "Produk berhasil diupdate!"
            )

            self.selected_row = None

            self.simpan_btn.setText(
                "💾 Simpan Produk"
            )

        # TAMBAH
        else:

            self.data_produk.append(produk)
            if hasattr(self.window(), "data_penjualan"):

                transaksi_baru = {
                    "transaksi": f"TRX{len(self.window().data_penjualan)+1:03}",
                    "tanggal": QDate.currentDate().toString("dd/MM/yyyy"),
                    "pelanggan": "Pelanggan Umum",
                    "total": f"Rp {harga}",
                    "status": "Selesai"
                }

                self.window().data_penjualan.append(
                    transaksi_baru
                )

            QMessageBox.information(
                self,
                "Berhasil",
                "Produk berhasil ditambahkan!"
            )

        self.refresh_table()

        self.dashboard.refresh_dashboard()

        self.window().save_data()

        self.reset_form()

   
    def refresh_table(self):

        keyword = self.search_input.text().lower()
        self.filtered_data = []
        self.table.setRowCount(0)

        for index, produk in enumerate(self.data_produk):

            if keyword not in produk["nama"].lower():
                continue
            self.filtered_data.append(produk)
            row = self.table.rowCount()

            self.table.insertRow(row)

            # STATUS
            if produk["stok"] <= 5:
                status = "Stok Habis"

            elif produk["stok"] <= 20:
                status = "Stok Rendah"

            else:
                status = "Stok Aman"

            data = [
                str(row + 1),
                produk["nama"],
                produk["kategori"],
                f"Rp {produk['harga']:,}".replace(",", "."),
                str(produk["stok"]),
                produk["satuan"],
                status,
                "✏ Hapus"
            ]

            for col, value in enumerate(data):

                item = QTableWidgetItem(value)

                if col == 6:

                    if status == "Stok Aman":
                        item.setForeground(Qt.green)

                    elif status == "Stok Rendah":
                        item.setForeground(Qt.darkYellow)

                    else:
                        item.setForeground(Qt.red)

                self.table.setItem(
                    row,
                    col,
                    item
                )

    # =====================================================
    # HANDLE CLICK
    # =====================================================
    def handle_table_click(self, row, column):

        # HAPUS
        if column == 7:

            produk = self.filtered_data[row]

            self.data_produk.remove(produk)

            self.refresh_table()

            self.dashboard.refresh_dashboard()

            if hasattr(self.window(), "penjualan_page"):

                self.window().penjualan_page.refresh_produk()

            if hasattr(self.window(), "save_data"):

                self.window().save_data()

            return

        # EDIT
        produk = self.filtered_data[row]

        self.selected_produk = produk

        self.nama_input.setText(
            produk["nama"]
        )

        self.kategori_input.setCurrentText(
            produk["kategori"]
        )

        self.harga_input.setText(
            str(produk["harga"])
        )

        self.modal_input.setText(
            str(produk["modal"])
        )

        self.stok_input.setText(
            str(produk["stok"])
        )

        self.satuan_input.setText(
            produk["satuan"]
        )

        self.selected_row = row

        self.simpan_btn.setText(
            "✏ Update Produk"
        )

    # =====================================================
    # RESET FORM
    # =====================================================
    def reset_form(self):

        self.nama_input.clear()
        self.harga_input.clear()
        self.modal_input.clear()
        self.stok_input.clear()
        self.satuan_input.clear()

        self.kategori_input.setCurrentIndex(0)

        self.selected_row = None

        self.simpan_btn.setText(
            "💾 Simpan Produk"
        )

    # =====================================================
    # SMOOTH SCROLL
    # =====================================================
    def smooth_wheel_event(self, event):

        delta = event.angleDelta().y()

        current_value = (
            self.scroll.verticalScrollBar().value()
        )

        step = 220

        if delta > 0:
            target = current_value - step
        else:
            target = current_value + step

        self.scroll_animation.stop()

        self.scroll_animation.setStartValue(
            current_value
        )

        self.scroll_animation.setEndValue(
            target
        )

        self.scroll_animation.start()

if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = KelolaProdukPage()
    window.show()

    sys.exit(app.exec())