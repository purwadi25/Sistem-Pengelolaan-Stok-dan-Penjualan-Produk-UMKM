import sys
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QLabel, QMessageBox
)
from PySide6.QtCore import Qt

class LoginPage(QWidget):
    def __init__(self, on_login_success):
        super().__init__()
        self.on_login_success = on_login_success
        self.init_ui()

    def init_ui(self):
        # Set background utama halaman
        self.setStyleSheet("background-color: #f8fafc;")
        
        # Main Layout (menggunakan tata letak horizontal agar card bisa presisi di tengah)
        main_layout = QHBoxLayout(self)
        
        # Container Card Login
        card = QWidget()
        card.setFixedWidth(380)
        card.setStyleSheet("""
            QWidget {
                background-color: #ffffff;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
            }
            QLabel { border: none; }
            QLineEdit {
                border: 1px solid #e2e8f0;
                border-radius: 6px;
                padding: 8px;
                font-size: 13px;
                color: #0f172a;
                background-color: #ffffff;
            }
            QLineEdit:focus {
                border: 1px solid #2563eb;
            }
            QPushButton {
                background-color: #2563eb;
                color: white;
                font-weight: bold;
                font-size: 14px;
                border: none;
                border-radius: 6px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #1d4ed8;
            }
        """)
        
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(30, 40, 30, 40)
        card_layout.setSpacing(15)

        # Branding Header
        lbl_logo = QLabel("🏪")
        lbl_logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_logo.setStyleSheet("font-size: 40px;")
        card_layout.addWidget(lbl_logo)

        lbl_title = QLabel("Selamat Datang Kembali")
        lbl_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_title.setStyleSheet("font-size: 18px; font-weight: bold; color: #0f172a;")
        card_layout.addWidget(lbl_title)

        lbl_sub = QLabel("Silakan masuk untuk mengelola sistem UMKM")
        lbl_sub.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_sub.setStyleSheet("font-size: 11px; color: #64748b;")
        card_layout.addWidget(lbl_sub)
        
        card_layout.addSpacing(10)

        # Form Username
        lbl_user = QLabel("Username")
        lbl_user.setStyleSheet("font-weight: bold; color: #334155; font-size: 12px;")
        card_layout.addWidget(lbl_user)
        
        self.entry_user = QLineEdit()
        self.entry_user.setPlaceholderText("Masukkan username...")
        self.entry_user.setText("admin") # Untuk mempermudah testing
        card_layout.addWidget(self.entry_user)

        # Form Password
        lbl_pass = QLabel("Password")
        lbl_pass.setStyleSheet("font-weight: bold; color: #334155; font-size: 12px;")
        card_layout.addWidget(lbl_pass)
        
        self.entry_pass = QLineEdit()
        self.entry_pass.setPlaceholderText("Masukkan password...")
        self.entry_pass.setEchoMode(QLineEdit.EchoMode.Password)
        self.entry_pass.setText("admin123") # Untuk mempermudah testing
        card_layout.addWidget(self.entry_pass)
        
        card_layout.addSpacing(10)

        # Tombol Masuk
        btn_login = QPushButton("Masuk ke Sistem")
        btn_login.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_login.clicked.connect(self.proses_login)
        card_layout.addWidget(btn_login)

        # Hubungkan tombol Enter di keyboard langsung ke fungsi login
        self.entry_user.returnPressed.connect(self.proses_login)
        self.entry_pass.returnPressed.connect(self.proses_login)

        main_layout.addWidget(card, alignment=Qt.AlignmentFlag.AlignCenter)

    def proses_login(self):
        username = self.entry_user.text().strip()
        password = self.entry_pass.text().strip()

        if not username or not password:
            QMessageBox.critical(self, "Gagal Masuk", "Username dan Password wajib diisi!")
            return

        if username == "admin" and password == "admin123":
            QMessageBox.information(self, "Sukses", f"Selamat datang kembali, {username}!")
            self.on_login_success()
        else:
            QMessageBox.critical(self, "Gagal Masuk", "Username atau Password salah!")