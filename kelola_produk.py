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

from PySide6.QtCore import Qt
import sys


class KelolaProdukPage(QWidget):
    def __init__(self, app_data, dashboard):
        super().__init__()

        self.setWindowTitle("Kelola Produk UMKM")
        self.resize(1400, 850)

        self.data_produk = app_data
        self.dashboard = dashboard

        self.selected_row = None

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

        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)


        # =====================================================
        # CONTENT
        # =====================================================
        content = QWidget()

        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(30, 25, 30, 25)
        content_layout.setSpacing(25)

        # HEADER
        title = QLabel("Kelola Produk")

        title.setStyleSheet("""
            font-size:34px;
            font-weight:bold;
            color:#111827;
        """)

        subtitle = QLabel(
            "Kelola data produk, stok, dan informasi produk Anda"
        )

        subtitle.setStyleSheet("""
            color:#6b7280;
            font-size:14px;
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
                border-radius:18px;
                border:1px solid #e5e7eb;
            }
        """)

        form_layout = QVBoxLayout(form_card)
        form_layout.setContentsMargins(25, 25, 25, 25)

        form_title = QLabel("➕ Tambah / Edit Produk")

        form_title.setStyleSheet("""
            font-size:24px;
            font-weight:bold;
        """)

        form_layout.addWidget(form_title)

        # INPUT ROW
        input_row = QHBoxLayout()

        def create_input(placeholder):

            inp = QLineEdit()
            inp.setPlaceholderText(placeholder)

            inp.setStyleSheet("""
                QLineEdit{
                    border:1px solid #d1d5db;
                    border-radius:10px;
                    padding:14px;
                    font-size:13px;
                    background:white;
                }

                QLineEdit:focus{
                    border:2px solid #14b8a6;
                }
            """)

            return inp

        self.nama_input = create_input(
            "Nama Produk"
        )

        self.harga_input = create_input(
            "Harga"
        )

        self.stok_input = create_input(
            "Stok"
        )

        self.satuan_input = create_input(
            "Satuan"
        )

        self.kategori_input = QComboBox()

        self.kategori_input.addItems([
            "Pilih Kategori",
            "Makanan",
            "Minuman",
            "Snack",
            "Lainnya"
        ])

        self.kategori_input.setStyleSheet("""
            QComboBox{
                border:1px solid #d1d5db;
                border-radius:10px;
                padding:14px;
                background:white;
                font-size:13px;
            }
        """)

        input_row.addWidget(self.nama_input)
        input_row.addWidget(self.kategori_input)
        input_row.addWidget(self.harga_input)
        input_row.addWidget(self.stok_input)
        input_row.addWidget(self.satuan_input)

        form_layout.addLayout(input_row)

        # =====================================================
        # BUTTON
        # =====================================================
        btn_row = QHBoxLayout()

        self.simpan_btn = QPushButton(
            "💾 Simpan Produk"
        )

        self.simpan_btn.setStyleSheet("""
            QPushButton{
                background:#14b8a6;
                color:white;
                border:none;
                padding:14px 22px;
                border-radius:10px;
                font-size:14px;
                font-weight:bold;
            }

            QPushButton:hover{
                background:#0f766e;
            }
        """)

        self.simpan_btn.clicked.connect(
            self.simpan_produk
        )

        reset_btn = QPushButton(
            "🔄 Bersihkan"
        )

        reset_btn.setStyleSheet("""
            QPushButton{
                background:#f3f4f6;
                border:none;
                padding:14px 22px;
                border-radius:10px;
                font-size:14px;
                font-weight:bold;
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
                border-radius:18px;
                border:1px solid #e5e7eb;
            }
        """)

        table_layout = QVBoxLayout(table_card)
        table_layout.setContentsMargins(25, 25, 25, 25)

        table_title = QLabel("📦 Daftar Produk")

        table_title.setStyleSheet("""
            font-size:24px;
            font-weight:bold;
        """)

        table_layout.addWidget(table_title)

        # SEARCH
        self.search_input = QLineEdit()

        self.search_input.setPlaceholderText(
            "🔍 Cari produk..."
        )

        self.search_input.textChanged.connect(
            self.refresh_table
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

        self.search_input.setMaximumWidth(300)

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

        self.table.setStyleSheet("""
            QTableWidget{
                border:none;
                background:white;
                font-size:13px;
                gridline-color:#f3f4f6;
            }

            QHeaderView::section{
                background:#f3f4f6;
                padding:14px;
                border:none;
                font-weight:bold;
            }
        """)

        self.table.cellClicked.connect(
            self.handle_table_click
        )

        table_layout.addWidget(self.table)

        content_layout.addWidget(table_card)

        root.addWidget(content)

    # =====================================================
    # SIMPAN PRODUK
    # =====================================================
    def simpan_produk(self):

        nama = self.nama_input.text()
        kategori = self.kategori_input.currentText()
        harga = self.harga_input.text()
        stok = self.stok_input.text()
        satuan = self.satuan_input.text()

        if (
            nama == "" or
            kategori == "Pilih Kategori" or
            harga == "" or
            stok == "" or
            satuan == ""
        ):

            QMessageBox.warning(
                self,
                "Error",
                "Semua field wajib diisi!"
            )

            return

        produk = {
            "nama": nama,
            "kategori": kategori,
            "harga": int(harga),
            "stok": int(stok),
            "satuan": satuan
        }

        # EDIT
        if self.selected_row is not None:

            self.data_produk[self.selected_row] = produk

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

            QMessageBox.information(
                self,
                "Berhasil",
                "Produk berhasil ditambahkan!"
            )

        self.refresh_table()
        self.dashboard.refresh_dashboard()
        self.reset_form()

    # =====================================================
    # REFRESH TABLE
    # =====================================================
    def refresh_table(self):

        keyword = self.search_input.text().lower()

        self.table.setRowCount(0)

        for index, produk in enumerate(self.data_produk):

            if keyword not in produk["nama"].lower():
                continue

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

        if column == 7:

            self.data_produk.pop(row)

            self.refresh_table()
            self.dashboard.refresh_dashboard()
            return

        produk = self.data_produk[row]

        self.nama_input.setText(
            produk["nama"]
        )

        self.kategori_input.setCurrentText(
            produk["kategori"]
        )

        self.harga_input.setText(
            str(produk["harga"])
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
        self.stok_input.clear()
        self.satuan_input.clear()

        self.kategori_input.setCurrentIndex(0)

        self.selected_row = None

        self.simpan_btn.setText(
            "💾 Simpan Produk"
        )


if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = KelolaProdukPage()
    window.show()

    sys.exit(app.exec())