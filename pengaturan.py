# =========================================================
# PENGATURAN PAGE
# =========================================================
from PySide6.QtWidgets import (
    QWidget,
    QFrame,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QMessageBox,
    QScrollArea
)

from PySide6.QtCore import Qt


class PengaturanPage(QWidget):
    def __init__(self, main_window):
        super().__init__()

        self.main_window = main_window

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

            QFrame{
                background:white;
                border-radius:20px;
                border:1px solid #e5e7eb;
            }

            QLabel{
                color:#111827;
            }

            QLineEdit{
                border:2px solid #e5e7eb;
                border-radius:12px;
                padding:14px;
                font-size:14px;
                background:white;
                color:#111827;
            }

            QLineEdit:focus{
                border:2px solid #14b8a6;
            }

            QPushButton{
                padding:14px;
                border-radius:12px;
                font-weight:bold;
                font-size:14px;
                border:none;
            }
        """)

        # =================================================
        # MAIN LAYOUT
        # =================================================
        main_layout = QVBoxLayout(self)

        main_layout.setContentsMargins(0, 0, 0, 0)

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
                background:#f4f7fb;
            }
        """)

        main_layout.addWidget(scroll)

        # =================================================
        # CONTAINER
        # =================================================
        container = QWidget()

        scroll.setWidget(container)

        root = QVBoxLayout(container)

        root.setContentsMargins(30, 25, 30, 25)
        root.setSpacing(24)

        # =================================================
        # HEADER
        # =================================================
        title = QLabel("⚙ Pengaturan Aplikasi")

        title.setStyleSheet("""
            font-size:36px;
            font-weight:800;
            color:#111827;
        """)

        subtitle = QLabel(
            "Kelola informasi toko dan akun aplikasi UMKM"
        )

        subtitle.setStyleSheet("""
            color:#6b7280;
            font-size:15px;
        """)

        root.addWidget(title)
        root.addWidget(subtitle)

        # =================================================
        # CONTENT ROW
        # =================================================
        content_row = QHBoxLayout()

        # =================================================
        # KOLOM KIRI
        # =================================================
        left_layout = QVBoxLayout()

        left_layout.setAlignment(Qt.AlignTop)
        left_layout.setSpacing(20)

        # =================================================
        # INFORMASI TOKO
        # =================================================
        toko_frame = QFrame()

        toko_layout = QVBoxLayout(toko_frame)

        toko_layout.setContentsMargins(
            24, 24, 24, 24
        )

        toko_layout.setSpacing(16)

        toko_title = QLabel("🏪 Informasi Toko")

        toko_title.setStyleSheet("""
            font-size:22px;
            font-weight:800;
        """)

        toko_layout.addWidget(toko_title)

        self.input_nama_toko = QLineEdit()
        self.input_nama_toko.setPlaceholderText(
            "Masukkan nama toko"
        )

        self.input_pemilik = QLineEdit()
        self.input_pemilik.setPlaceholderText(
            "Masukkan nama pemilik"
        )

        self.input_alamat = QLineEdit()
        self.input_alamat.setPlaceholderText(
            "Masukkan alamat toko"
        )

        self.input_telepon = QLineEdit()
        self.input_telepon.setPlaceholderText(
            "Masukkan nomor telepon"
        )

        labels = [
            ("Nama Toko", self.input_nama_toko),
            ("Nama Pemilik", self.input_pemilik),
            ("Alamat", self.input_alamat),
            ("Telepon", self.input_telepon),
        ]

        for text, widget in labels:

            label = QLabel(text)

            label.setStyleSheet("""
                font-size:14px;
                font-weight:600;
                color:#374151;
            """)

            toko_layout.addWidget(label)
            toko_layout.addWidget(widget)

        # BUTTON SIMPAN
        self.btn_simpan = QPushButton(
            "💾 Simpan Pengaturan"
        )

        self.btn_simpan.setMinimumHeight(50)
        self.btn_simpan.setMaximumWidth(300)

        self.btn_simpan.setStyleSheet("""
            QPushButton{
                background:#14b8a6;
                color:white;
            }

            QPushButton:hover{
                background:#0f766e;
            }
        """)

        self.btn_simpan.clicked.connect(
            self.simpan_pengaturan
        )

        btn_wrap = QHBoxLayout()

        btn_wrap.addStretch()
        btn_wrap.addWidget(self.btn_simpan)
        btn_wrap.addStretch()

        toko_layout.addSpacing(10)
        toko_layout.addLayout(btn_wrap)

        left_layout.addWidget(toko_frame)

        # =================================================
        # PENGATURAN AKUN
        # =================================================
        akun_frame = QFrame()

        akun_layout = QVBoxLayout(akun_frame)

        akun_layout.setContentsMargins(
            24, 24, 24, 24
        )

        akun_layout.setSpacing(16)

        akun_title = QLabel("🔐 Pengaturan Akun")

        akun_title.setStyleSheet("""
            font-size:22px;
            font-weight:800;
        """)

        akun_layout.addWidget(akun_title)

        self.input_username = QLineEdit()

        self.input_username.setPlaceholderText(
            "Masukkan username baru"
        )

        self.input_password = QLineEdit()

        self.input_password.setPlaceholderText(
            "Masukkan password baru"
        )

        self.input_password.setEchoMode(
            QLineEdit.Password
        )

        akun_labels = [
            ("Username", self.input_username),
            ("Password", self.input_password),
        ]

        for text, widget in akun_labels:

            label = QLabel(text)

            label.setStyleSheet("""
                font-size:14px;
                font-weight:600;
                color:#374151;
            """)

            akun_layout.addWidget(label)
            akun_layout.addWidget(widget)

        self.btn_update_akun = QPushButton(
            "🔄 Update Akun"
        )

        self.btn_update_akun.setMinimumHeight(50)
        self.btn_update_akun.setMaximumWidth(250)

        self.btn_update_akun.setStyleSheet("""
            QPushButton{
                background:#3b82f6;
                color:white;
            }

            QPushButton:hover{
                background:#2563eb;
            }
        """)

        self.btn_update_akun.clicked.connect(
            self.update_akun
        )

        akun_btn_wrap = QHBoxLayout()

        akun_btn_wrap.addStretch()

        akun_btn_wrap.addWidget(
            self.btn_update_akun
        )

        akun_btn_wrap.addStretch()

        akun_layout.addSpacing(10)

        akun_layout.addLayout(
            akun_btn_wrap
        )

        left_layout.addWidget(akun_frame)

        # =================================================
        # ADD LAYOUT
        # =================================================
        content_row.addLayout(left_layout)

        root.addLayout(content_row)

        root.addStretch()

    # =====================================================
    # SIMPAN PENGATURAN
    # =====================================================
    def simpan_pengaturan(self):

        QMessageBox.information(
            self,
            "Berhasil",
            "Pengaturan toko berhasil disimpan!"
        )

    # =====================================================
    # UPDATE AKUN
    # =====================================================
    def update_akun(self):

        username = self.input_username.text()
        password = self.input_password.text()

        if username == "" or password == "":

            QMessageBox.warning(
                self,
                "Error",
                "Username dan password tidak boleh kosong!"
            )

            return

        QMessageBox.information(
            self,
            "Berhasil",
            "Akun berhasil diperbarui!"
        )