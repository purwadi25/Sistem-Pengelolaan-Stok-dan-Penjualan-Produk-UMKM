import sys
import json
import os
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QMainWindow,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
    QStackedWidget,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QDialog,
    QFormLayout,
    QLineEdit,
    QMessageBox
)

from PySide6.QtCore import Qt
from dashboard import DashboardPage
from kelola_produk import KelolaProdukPage
from stok_produk import StokProdukPage
from penjualan import PenjualanPage
from laporan import LaporanPenjualanPage
from pengaturan import PengaturanPage

# =========================================================
# LOGIN WINDOW
# =========================================================
class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Login UMKM")
        self.resize(500, 600)

        self.setStyleSheet("""
            QWidget{
                background:#f8fafc;
                font-family:'Segoe UI';
            }
        """)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        card = QFrame()
        card.setFixedWidth(380)

        card.setStyleSheet("""
            QFrame{
                background:white;
                border-radius:20px;
                border:1px solid #e5e7eb;
            }
        """)

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(40, 40, 40, 40)
        card_layout.setSpacing(20)

        logo = QLabel("🛒")
        logo.setAlignment(Qt.AlignCenter)

        logo.setStyleSheet("""
            font-size:60px;
        """)

        title = QLabel("UMKM STOCK")
        title.setAlignment(Qt.AlignCenter)

        title.setStyleSheet("""
            font-size:30px;
            font-weight:bold;
            color:#111827;
        """)

        subtitle = QLabel("Login Sistem Pengelolaan UMKM")
        subtitle.setAlignment(Qt.AlignCenter)

        subtitle.setStyleSheet("""
            color:#6b7280;
            font-size:14px;
        """)

        self.username = QLineEdit()
        self.username.setPlaceholderText("Username")

        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.Password)

        for inp in [self.username, self.password]:

            inp.setStyleSheet("""
                QLineEdit{
                    padding:12px;
                    border:1px solid #d1d5db;
                    border-radius:10px;
                    font-size:14px;
                }
            """)

        self.btn_login = QPushButton("LOGIN")

        self.btn_login.setStyleSheet("""
            QPushButton{
                background:#14b8a6;
                color:white;
                border:none;
                padding:14px;
                border-radius:10px;
                font-size:15px;
                font-weight:bold;
            }

            QPushButton:hover{
                background:#0f766e;
            }
        """)

        self.btn_login.clicked.connect(self.login)

        card_layout.addWidget(logo)
        card_layout.addWidget(title)
        card_layout.addWidget(subtitle)
        card_layout.addWidget(self.username)
        card_layout.addWidget(self.password)
        card_layout.addWidget(self.btn_login)

        layout.addWidget(card)

    def login(self):

        user = self.username.text()
        pw = self.password.text()

        if user == "admin" and pw == "123":

            self.main_window = MainWindow()
            self.main_window.show()

            self.close()

        else:

            QMessageBox.warning(
                self,
                "Login Gagal",
                "Username atau password salah!"
            )


# =========================================================
# DIALOG TAMBAH PRODUK
# =========================================================
class ProdukDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Tambah Produk")
        self.setFixedSize(350, 300)

        self.setStyleSheet("""
            QDialog{
                background:white;
            }

            QLabel{
                font-size:13px;
            }

            QLineEdit{
                border:1px solid #d1d5db;
                border-radius:6px;
                padding:10px;
                font-size:13px;
            }

            QPushButton{
                background:#14b8a6;
                color:white;
                border:none;
                padding:10px;
                border-radius:8px;
                font-weight:bold;
            }

            QPushButton:hover{
                background:#0f766e;
            }
        """)

        layout = QFormLayout(self)

        self.nama = QLineEdit()
        self.kategori = QLineEdit()
        self.stok = QLineEdit()
        self.harga = QLineEdit()

        layout.addRow("Nama Produk", self.nama)
        layout.addRow("Kategori", self.kategori)
        layout.addRow("Stok", self.stok)
        layout.addRow("Harga", self.harga)

        btn = QPushButton("Simpan")
        btn.clicked.connect(self.accept)

        layout.addWidget(btn)







# =========================================================
# PAGE DUMMY
# =========================================================
class DummyPage(QWidget):
    def __init__(self, text):
        super().__init__()

        layout = QVBoxLayout(self)

        label = QLabel(text)
        label.setAlignment(Qt.AlignCenter)

        label.setStyleSheet("""
            font-size:28px;
            font-weight:bold;
            color:#111827;
        """)

        layout.addWidget(label)


# =========================================================
# MAIN WINDOW
# =========================================================
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(
            "Sistem Pengelolaan Stok UMKM"
        )

        self.resize(1500, 850)

        self.load_data()

        central = QWidget()
        self.setCentralWidget(central)

        root = QHBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # SIDEBAR
        sidebar = QFrame()
        sidebar.setFixedWidth(250)

        sidebar.setStyleSheet("""
            QFrame{
                background:#0f172a;
            }
        """)

        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(15, 20, 15, 20)

        logo = QLabel("🛒 UMKM STOCK")

        logo.setStyleSheet("""
            color:white;
            font-size:24px;
            font-weight:bold;
            padding:15px;
        """)

        sidebar_layout.addWidget(logo)

        # STACK
        self.stack = QStackedWidget()

        self.dashboard = DashboardPage(
            self.data_produk,
            self.data_penjualan
        )

        self.kelola_produk = KelolaProdukPage(
            self.data_produk,
            self.dashboard
        )

        self.stok_produk = StokProdukPage(
            self.data_produk,
            self.dashboard
        )

        self.penjualan_page = PenjualanPage(
            self.data_produk,
            self.data_penjualan,
            self.dashboard
        )

        self.laporan_page = LaporanPenjualanPage(
            self.data_penjualan
        )

        self.pengaturan_page = PengaturanPage(
            self
        )

        # ADD PAGE
        self.stack.addWidget(self.dashboard)
        self.stack.addWidget(self.kelola_produk)
        self.stack.addWidget(self.stok_produk)
        self.stack.addWidget(self.penjualan_page)
        self.stack.addWidget(self.laporan_page)
        self.stack.addWidget(self.pengaturan_page)

        # MENU
        menus = [
            ("🏠 Dashboard", 0),
            ("🛠 Kelola Produk", 1),
            ("📦 Stok Produk", 2),
            ("🛒 Penjualan", 3),
            ("📊 Laporan Penjualan", 4),
            ("⚙ Pengaturan", 5),
        ]

        for text, index in menus:

            btn = QPushButton(text)

            btn.setStyleSheet("""
                QPushButton{
                    color:white;
                    border:none;
                    padding:15px;
                    text-align:left;
                    border-radius:10px;
                    font-size:14px;
                }

                QPushButton:hover{
                    background:#1e293b;
                }
            """)

            btn.clicked.connect(
                lambda checked, idx=index:
                self.stack.setCurrentIndex(idx)
            )

            sidebar_layout.addWidget(btn)

        sidebar_layout.addStretch()

        # LOGOUT
        logout = QPushButton("⏻ Logout")

        logout.setStyleSheet("""
            QPushButton{
                color:white;
                border:none;
                padding:15px;
                text-align:left;
                border-radius:10px;
                font-size:14px;
            }

            QPushButton:hover{
                background:#1e293b;
            }
        """)

        logout.clicked.connect(self.logout)

        sidebar_layout.addWidget(logout)

        root.addWidget(sidebar)
        root.addWidget(self.stack)

    # =========================================================
    # LOAD DATA JSON
    # =========================================================
    
    def load_data(self):

        # =========================
        # DATA PRODUK
        # =========================
        if os.path.exists("produk.json"):

            try:
                with open("produk.json", "r") as file:
                    self.data_produk = json.load(file)

            except:
                self.data_produk = []

        else:
            self.data_produk = []

        # =========================
        # DATA PENJUALAN
        # =========================
        if os.path.exists("penjualan.json"):

            try:
                with open("penjualan.json", "r") as file:
                    self.data_penjualan = json.load(file)

            except:
                self.data_penjualan = []

        else:
            self.data_penjualan = []

    # =========================================================
    # SAVE DATA JSON
    # =========================================================
    def save_data(self):

        with open("produk.json", "w") as file:

            json.dump(
                self.data_produk,
                file,
                indent=4,
                ensure_ascii=False
            )

        with open("penjualan.json", "w") as file:

            json.dump(
                self.data_penjualan,
                file,
                indent=4,
                ensure_ascii=False
            )


    # =========================================================
    # AUTO SAVE SAAT CLOSE
    # =========================================================
    def closeEvent(self, event):

        self.save_data()

        event.accept()

    # =========================================================
    # LOGOUT
    # =========================================================
    def logout(self):

        self.save_data()

        self.login = LoginWindow()
        self.login.show()

        self.close()


# =========================================================
# RUN APP
# =========================================================
if __name__ == "__main__":

    app = QApplication(sys.argv)

    login = LoginWindow()
    login.show()

    sys.exit(app.exec())