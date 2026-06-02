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
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QLineEdit,
    QMessageBox
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
                background:#f8fafc;
                font-family:'Segoe UI';
            }

            QFrame{
                background:white;
                border-radius:12px;
                border:1px solid #e5e7eb;
            }

            QLabel{
                color:#111827;
            }

            QLineEdit{
                border:1px solid #d1d5db;
                border-radius:8px;
                padding:10px;
                font-size:13px;
                background:white;
            }

            QPushButton{
                padding:12px;
                border-radius:8px;
                font-weight:bold;
                font-size:13px;
                border:none;
            }
        """)

        root = QVBoxLayout(self)
        root.setContentsMargins(20, 20, 20, 20)
        root.setSpacing(15)

        # =================================================
        # HEADER
        # =================================================
        title = QLabel("Pengaturan Aplikasi")

        title.setStyleSheet("""
            font-size:28px;
            font-weight:bold;
        """)

        subtitle = QLabel(
            "Kelola informasi aplikasi dan akun UMKM"
        )

        subtitle.setStyleSheet("""
            color:#6b7280;
            font-size:13px;
        """)

        root.addWidget(title)
        root.addWidget(subtitle)

        # =================================================
        # INFORMASI TOKO
        # =================================================
        toko_frame = QFrame()

        toko_layout = QVBoxLayout(toko_frame)

        toko_title = QLabel("🏪 Informasi Toko")

        toko_title.setStyleSheet("""
            font-size:18px;
            font-weight:bold;
        """)

        toko_layout.addWidget(toko_title)

        self.input_nama_toko = QLineEdit()
        self.input_nama_toko.setPlaceholderText(
            "Nama Toko"
        )

        self.input_pemilik = QLineEdit()
        self.input_pemilik.setPlaceholderText(
            "Nama Pemilik"
        )

        self.input_alamat = QLineEdit()
        self.input_alamat.setPlaceholderText(
            "Alamat Toko"
        )

        self.input_telepon = QLineEdit()
        self.input_telepon.setPlaceholderText(
            "Nomor Telepon"
        )

        toko_layout.addWidget(
            QLabel("Nama Toko")
        )

        toko_layout.addWidget(
            self.input_nama_toko
        )

        toko_layout.addWidget(
            QLabel("Nama Pemilik")
        )

        toko_layout.addWidget(
            self.input_pemilik
        )

        toko_layout.addWidget(
            QLabel("Alamat")
        )

        toko_layout.addWidget(
            self.input_alamat
        )

        toko_layout.addWidget(
            QLabel("Telepon")
        )

        toko_layout.addWidget(
            self.input_telepon
        )

        # BUTTON SIMPAN
        self.btn_simpan = QPushButton(
            "Simpan Pengaturan"
        )

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

        toko_layout.addWidget(self.btn_simpan)

        root.addWidget(toko_frame)

        # =================================================
        # PENGATURAN AKUN
        # =================================================
        akun_frame = QFrame()

        akun_layout = QVBoxLayout(akun_frame)

        akun_title = QLabel("🔐 Pengaturan Akun")

        akun_title.setStyleSheet("""
            font-size:18px;
            font-weight:bold;
        """)

        akun_layout.addWidget(akun_title)

        self.input_username = QLineEdit()
        self.input_username.setPlaceholderText(
            "Username Baru"
        )

        self.input_password = QLineEdit()
        self.input_password.setPlaceholderText(
            "Password Baru"
        )

        akun_layout.addWidget(
            QLabel("Username")
        )

        akun_layout.addWidget(
            self.input_username
        )

        akun_layout.addWidget(
            QLabel("Password")
        )

        akun_layout.addWidget(
            self.input_password
        )

        # BUTTON UPDATE
        self.btn_update_akun = QPushButton(
            "Update Akun"
        )

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

        akun_layout.addWidget(
            self.btn_update_akun
        )

        root.addWidget(akun_frame)

        # =================================================
        # INFORMASI APP
        # =================================================
        info_frame = QFrame()

        info_layout = QVBoxLayout(info_frame)

        info_title = QLabel("ℹ Informasi Aplikasi")

        info_title.setStyleSheet("""
            font-size:18px;
            font-weight:bold;
        """)

        info_layout.addWidget(info_title)

        app_name = QLabel(
            "Nama App : Sistem Pengelolaan UMKM"
        )

        version = QLabel(
            "Versi : 1.0.0"
        )

        developer = QLabel(
            "Developer : UMKM App Team"
        )

        app_name.setStyleSheet("""
            font-size:13px;
        """)

        version.setStyleSheet("""
            font-size:13px;
        """)

        developer.setStyleSheet("""
            font-size:13px;
        """)

        info_layout.addWidget(app_name)
        info_layout.addWidget(version)
        info_layout.addWidget(developer)

        root.addWidget(info_frame)

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