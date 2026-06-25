import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PySide6.QtWidgets import (
    QApplication, QWidget, QMainWindow, QLabel,
    QPushButton, QVBoxLayout, QHBoxLayout,
    QFrame, QStackedWidget, QLineEdit, QMessageBox,
    QMenuBar, QMenu, QStatusBar,
)
from PySide6.QtCore  import Qt
from PySide6.QtGui   import QIcon, QPixmap, QAction

from utils.auth    import verify_login, load_credentials
from database.db   import init_db

from gui.dashboard     import DashboardPage
from gui.kelola_produk import KelolaProdukPage
from gui.penjualan     import PenjualanPage
from gui.laporan       import LaporanPenjualanPage
from gui.pengaturan    import PengaturanPage

# Info anggota kelompok
ANGGOTA = [
    ("Lutfi Alfarizi",  "F1D02310121"),
    ("Lalu Ahmad Purwadi",  "F1D02310115"),
    ("Salsa Reike Maharani",  "F1D02310136"),
]
STATUS_BAR_TEXT = "  |  ".join(
    f"{n}  [{nim}]" for n, nim in ANGGOTA
)

# LOGIN WINDOW
class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login - UMKM Stock")
        self.resize(500, 580)
        self._set_window_icon()
        self.setStyleSheet("""
            QWidget { background: #f8fafc; font-family: 'Segoe UI'; color: #111827; }
            QLabel  { border: none; background: transparent; }
        """)
        self._setup_ui()

    def _set_window_icon(self):
        p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "icon.png")
        if os.path.exists(p):
            self.setWindowIcon(QIcon(p))

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        card = QFrame()
        card.setFixedWidth(380)
        card.setStyleSheet("""
            QFrame  { background:white; border-radius:20px; border:1px solid #e5e7eb; }
            QLabel  { background:transparent; border:none; }
        """)
        cl = QVBoxLayout(card)
        cl.setContentsMargins(40, 40, 40, 40)
        cl.setSpacing(16)

        logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                 "assets", "logo.png")
        if os.path.exists(logo_path):
            logo_lbl = QLabel()
            pix = QPixmap(logo_path).scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            logo_lbl.setPixmap(pix)
            logo_lbl.setAlignment(Qt.AlignCenter)
        else:
            logo_lbl = QLabel("🛒")
            logo_lbl.setAlignment(Qt.AlignCenter)
            logo_lbl.setStyleSheet("font-size: 56px;")

        title    = QLabel("UMKM STOCK")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size:26px; font-weight:bold; color:#111827;")

        subtitle = QLabel("Sistem Pengelolaan Stok & Penjualan")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color:#6b7280; font-size:13px;")

        inp_style = """
            QLineEdit {
                padding:10px 14px; border:1.5px solid #d1d5db;
                border-radius:10px; font-size:14px; color:#111827; background:white;
            }
            QLineEdit:focus { border:2px solid #14b8a6; }
        """
        self._username = QLineEdit()
        self._username.setPlaceholderText("Username")
        self._username.setMinimumHeight(46)
        self._username.setStyleSheet(inp_style)
        self._username.returnPressed.connect(self._login)

        self._password = QLineEdit()
        self._password.setPlaceholderText("Password")
        self._password.setEchoMode(QLineEdit.Password)
        self._password.setMinimumHeight(46)
        self._password.setStyleSheet(inp_style)
        self._password.returnPressed.connect(self._login)

        btn = QPushButton("LOGIN")
        btn.setMinimumHeight(48)
        btn.setStyleSheet("""
            QPushButton {
                background:#14b8a6; color:white; border:none;
                border-radius:10px; font-size:15px; font-weight:bold;
            }
            QPushButton:hover   { background:#0f766e; }
            QPushButton:pressed { background:#0d6861; }
        """)
        btn.clicked.connect(self._login)

        hint = QLabel("Default: admin / admin123")
        hint.setAlignment(Qt.AlignCenter)
        hint.setStyleSheet("color:#9ca3af; font-size:11px;")

        for w in [logo_lbl, title, subtitle, self._username, self._password, btn, hint]:
            cl.addWidget(w)

        layout.addWidget(card)

    def _login(self):
        user = self._username.text().strip()
        pw   = self._password.text()
        if not user or not pw:
            QMessageBox.warning(self, "Input Kosong", "Username dan password wajib diisi.")
            return
        if verify_login(user, pw):
            self._main = MainWindow(logged_in_user=user)
            self._main.show()
            self.close()
        else:
            QMessageBox.warning(self, "Login Gagal", "Username atau password salah!")
            self._password.clear()
            self._password.setFocus()

# MAIN WINDOW
class MainWindow(QMainWindow):
    def __init__(self, logged_in_user: str = "admin"):
        super().__init__()
        self._current_user = logged_in_user
        self.setWindowTitle("Sistem Pengelolaan Stok UMKM")
        self.resize(1400, 820)
        self._set_window_icon()

        # Inisialisasi database SQLite
        init_db()

        from database.db import produk_get_all, penjualan_get_all
        self.data_produk    = produk_get_all()
        self.data_penjualan = penjualan_get_all()

        self._setup_ui()
        self.dashboard.update_user_display(logged_in_user)

    # ------------------------------------------------------------
    def _set_window_icon(self):
        p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "icon.png")
        if os.path.exists(p):
            self.setWindowIcon(QIcon(p))

    # ------------------------------------------------------------
    def _setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)

        # MENU BAR
        mb = self.menuBar()
        mb.setStyleSheet("""
            QMenuBar {
                background: #0f172a;
                color: white;
                font-size: 13px;
                padding: 2px 6px;
            }
            QMenuBar::item { padding: 6px 14px; border-radius: 6px; }
            QMenuBar::item:selected { background: #1e293b; }
            QMenu {
                background: white;
                color: #111827;
                border: 1px solid #e5e7eb;
                border-radius: 8px;
                padding: 4px;
                font-size: 13px;
            }
            QMenu::item { padding: 8px 20px; border-radius: 6px; }
            QMenu::item:selected { background: #f0fdf4; color: #0f766e; }
            QMenu::separator { height: 1px; background: #e5e7eb; margin: 4px 8px; }
        """)

        # Menu FILE
        file_menu = mb.addMenu("📁  File")

        act_dashboard = QAction("🏠  Dashboard",          self)
        act_produk    = QAction("🛠  Kelola Produk",      self)
        act_penjualan = QAction("🛒  Penjualan",          self)
        act_laporan   = QAction("📊  Laporan Penjualan",  self)
        act_pengaturan= QAction("⚙  Pengaturan",         self)

        act_dashboard.setShortcut("Ctrl+1")
        act_produk.setShortcut("Ctrl+2")
        act_penjualan.setShortcut("Ctrl+3")
        act_laporan.setShortcut("Ctrl+4")
        act_pengaturan.setShortcut("Ctrl+5")

        act_dashboard.triggered.connect(lambda: self._navigate(0))
        act_produk.triggered.connect(lambda: self._navigate(1))
        act_penjualan.triggered.connect(lambda: self._navigate(2))
        act_laporan.triggered.connect(lambda: self._navigate(3))
        act_pengaturan.triggered.connect(lambda: self._navigate(4))

        act_logout = QAction("⏻  Logout", self)
        act_logout.setShortcut("Ctrl+L")
        act_logout.triggered.connect(self._logout)

        act_exit = QAction("✕  Keluar", self)
        act_exit.setShortcut("Ctrl+Q")
        act_exit.triggered.connect(self.close)

        for act in [act_dashboard, act_produk, act_penjualan,
                    act_laporan, act_pengaturan]:
            file_menu.addAction(act)
        file_menu.addSeparator()
        file_menu.addAction(act_logout)
        file_menu.addSeparator()
        file_menu.addAction(act_exit)

        # Menu EXPORT
        export_menu = mb.addMenu("📤  Export")

        act_csv_produk  = QAction("CSV — Daftar Produk",        self)
        act_csv_jual    = QAction("CSV — Laporan Penjualan",     self)
        act_pdf_produk  = QAction("PDF — Daftar Produk",        self)
        act_pdf_laporan = QAction("PDF — Laporan Penjualan",     self)

        act_csv_produk.triggered.connect(self._export_csv_produk)
        act_csv_jual.triggered.connect(self._export_csv_penjualan)
        act_pdf_produk.triggered.connect(self._export_pdf_produk)
        act_pdf_laporan.triggered.connect(self._export_pdf_laporan)

        for act in [act_csv_produk, act_csv_jual,
                    act_pdf_produk, act_pdf_laporan]:
            export_menu.addAction(act)

        # Menu BANTUAN
        help_menu = mb.addMenu("❓  Bantuan")

        act_about = QAction("ℹ  Tentang Aplikasi", self)
        act_about.triggered.connect(self._show_about)
        help_menu.addAction(act_about)

        # STATUS BAR
        sb = QStatusBar()
        sb.setStyleSheet("""
            QStatusBar {
                background: #0f172a;
                color: #94a3b8;
                font-size: 12px;
                border-top: 1px solid #1e293b;
            }
        """)
        sb.showMessage(f"Anggota Kelompok:  {STATUS_BAR_TEXT}")
        sb.setSizeGripEnabled(False)
        self.setStatusBar(sb)

        # LAYOUT UTAMA
        root = QHBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # SIDEBAR
        sidebar = QFrame()
        sidebar.setFixedWidth(240)
        sidebar.setStyleSheet("""
            QFrame      { background: #0f172a; }
            QLabel      { background: transparent; border: none; }
            QPushButton { border: none; }
        """)
        sl = QVBoxLayout(sidebar)
        sl.setContentsMargins(14, 20, 14, 20)
        sl.setSpacing(4)

        logo_frame = QFrame()
        logo_frame.setStyleSheet("QFrame { background:transparent; border:none; }")
        logo_row = QHBoxLayout(logo_frame)
        logo_row.setContentsMargins(10, 8, 10, 8)
        logo_row.setSpacing(10)

        logo_icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                       "assets", "logo.png")
        if os.path.exists(logo_icon_path):
            logo_img = QLabel()
            pix = QPixmap(logo_icon_path).scaled(32, 32, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            logo_img.setPixmap(pix)
            logo_row.addWidget(logo_img)

        logo_txt = QLabel("UMKM STOCK")
        logo_txt.setStyleSheet("color:white; font-size:18px; font-weight:bold;")
        logo_row.addWidget(logo_txt)
        logo_row.addStretch()
        sl.addWidget(logo_frame)
        sl.addSpacing(8)

        # STACK
        self.stack = QStackedWidget()

        self.dashboard       = DashboardPage(self.data_produk, self.data_penjualan)
        self.kelola_produk   = KelolaProdukPage(self.data_produk, self.dashboard)
        self.penjualan_page  = PenjualanPage(self.data_produk, self.data_penjualan, self.dashboard)
        self.laporan_page    = LaporanPenjualanPage(self.data_penjualan)
        self.pengaturan_page = PengaturanPage(self)

        self.dashboard.set_navigate_callback(self._handle_nav_callback)

        for page in [self.dashboard, self.kelola_produk,
                     self.penjualan_page, self.laporan_page,
                     self.pengaturan_page]:
            self.stack.addWidget(page)

        menus = [
            ("🏠  Dashboard",         0),
            ("🛠  Kelola Produk",     1),
            ("🛒  Penjualan",         2),
            ("📊  Laporan Penjualan", 3),
            ("⚙  Pengaturan",        4),
        ]
        self._menu_buttons: list[QPushButton] = []
        for text, idx in menus:
            btn = QPushButton(text)
            btn.setStyleSheet(self._menu_style(False))
            btn.clicked.connect(lambda _, i=idx: self._navigate(i))
            sl.addWidget(btn)
            self._menu_buttons.append(btn)

        sl.addStretch()

        logout_btn = QPushButton("⏻  Logout")
        logout_btn.setStyleSheet("""
            QPushButton {
                color:#f87171; border:none; padding:14px 10px;
                text-align:left; border-radius:10px;
                font-size:14px; background:transparent;
            }
            QPushButton:hover { background:#1e293b; }
        """)
        logout_btn.clicked.connect(self._logout)
        sl.addWidget(logout_btn)

        root.addWidget(sidebar)
        root.addWidget(self.stack)
        self._navigate(0)

    # ------------------------------------------------------------
    def _navigate(self, idx: int, sub: str = ""):
        self.stack.setCurrentIndex(idx)
        for i, btn in enumerate(self._menu_buttons):
            btn.setStyleSheet(self._menu_style(i == idx))

    def _handle_nav_callback(self, idx, sub: str = ""):
        if idx == "logout":
            self._logout()
        else:
            self._navigate(idx, sub)

    def _menu_style(self, active: bool) -> str:
        bg = "#1e3a5f" if active else "transparent"
        return f"""
            QPushButton {{
                color:white; border:none;
                padding:14px 10px; text-align:left;
                border-radius:10px; font-size:14px; background:{bg};
            }}
            QPushButton:hover {{ background:#1e293b; }}
        """

    # EXPORT
    def _export_csv_produk(self):
        from utils.exporter import export_produk_csv
        try:
            path = export_produk_csv(self.data_produk)
            QMessageBox.information(self, "Export Berhasil",
                                    f"File CSV disimpan di:\n{path}")
        except Exception as e:
            QMessageBox.critical(self, "Export Gagal", str(e))

    def _export_csv_penjualan(self):
        from utils.exporter import export_penjualan_csv
        try:
            path = export_penjualan_csv(self.data_penjualan)
            QMessageBox.information(self, "Export Berhasil",
                                    f"File CSV disimpan di:\n{path}")
        except Exception as e:
            QMessageBox.critical(self, "Export Gagal", str(e))

    def _export_pdf_produk(self):
        from utils.exporter import export_produk_pdf
        creds = load_credentials()
        try:
            path = export_produk_pdf(self.data_produk,
                                      nama_toko=creds.get("nama_toko", "UMKM Stock"))
            QMessageBox.information(self, "Export Berhasil",
                                    f"File PDF disimpan di:\n{path}")
        except Exception as e:
            QMessageBox.critical(self, "Export Gagal", str(e))

    def _export_pdf_laporan(self):
        from utils.exporter import export_laporan_pdf
        creds = load_credentials()
        try:
            path = export_laporan_pdf(self.data_penjualan,
                                       nama_toko=creds.get("nama_toko", "UMKM Stock"))
            QMessageBox.information(self, "Export Berhasil",
                                    f"File PDF disimpan di:\n{path}")
        except Exception as e:
            QMessageBox.critical(self, "Export Gagal", str(e))

    # TENTANG
    def _show_about(self):
        anggota_str = "\n".join(f"  • {n}  [{nim}]" for n, nim in ANGGOTA)
        QMessageBox.about(
            self, "Tentang Aplikasi",
            f"<b>UMKM Stock</b><br>"
            f"Sistem Pengelolaan Stok dan Penjualan Produk UMKM<br><br>"
            f"<b>Mata Kuliah:</b> Pemrograman Visual<br>"
            f"<b>Teknologi:</b> Python 3 + PySide6 + SQLite<br><br>"
            f"<b>Anggota Kelompok:</b><br>"
            + "<br>".join(f"&nbsp;&nbsp;• {n} &nbsp;[{nim}]" for n, nim in ANGGOTA)
        )

    # DATA
    def reload_data(self):
        from database.db import produk_get_all, penjualan_get_all
        self.data_produk[:]    = produk_get_all()
        self.data_penjualan[:] = penjualan_get_all()

    def save_data(self):
        pass

    def closeEvent(self, event):
        event.accept()

    def _logout(self):
        self._login_win = LoginWindow()
        self._login_win.show()
        self.close()

# ENTRY POINT
if __name__ == "__main__":
    init_db()
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    login = LoginWindow()
    login.show()
    sys.exit(app.exec())