from PySide6.QtWidgets import (
    QWidget, QFrame, QLabel, QPushButton,
    QVBoxLayout, QHBoxLayout, QLineEdit,
    QMessageBox, QScrollArea, QDialog, QDialogButtonBox,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QCursor

from utils.styles import (
    PAGE_STYLE, CARD_STYLE, INPUT_STYLE,
    BTN_PRIMARY_STYLE, BTN_SECONDARY_STYLE,
    COLOR_TEXT_DARK, COLOR_TEXT_MUTED,
)
from utils.auth import load_credentials, update_credentials, update_info_toko, verify_login

# HELPER
def _field(layout: QVBoxLayout, label_text: str, placeholder: str, echo: bool = False) -> QLineEdit:
    lbl = QLabel(label_text)
    lbl.setStyleSheet(f"font-size:13px; font-weight:600; color:{COLOR_TEXT_DARK};")
    layout.addWidget(lbl)

    inp = QLineEdit()
    inp.setPlaceholderText(placeholder)
    inp.setFixedHeight(44)
    inp.setStyleSheet(INPUT_STYLE)
    if echo:
        inp.setEchoMode(QLineEdit.Password)
    layout.addWidget(inp)
    layout.addSpacing(14)
    return inp

def _dialog_buttons(layout: QVBoxLayout, ok_text: str = "💾  Simpan") -> QDialogButtonBox:
    btns = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
    btns.button(QDialogButtonBox.Ok).setText(ok_text)
    btns.button(QDialogButtonBox.Cancel).setText("Batal")
    btns.button(QDialogButtonBox.Ok).setStyleSheet(BTN_PRIMARY_STYLE)
    btns.button(QDialogButtonBox.Cancel).setStyleSheet(BTN_SECONDARY_STYLE)
    layout.addSpacing(6)
    layout.addWidget(btns)
    return btns

# DIALOG — Tambah / Ubah Informasi Toko
class InfoTokoDialog(QDialog):
    def __init__(self, parent=None, creds: dict | None = None):
        super().__init__(parent)
        self.setWindowTitle("Pengaturan Toko")
        self.setFixedWidth(480)
        self.setModal(True)
        self.setStyleSheet(f"""
            QDialog {{ background:#f8fafc; font-family:'Segoe UI'; }}
            QLabel  {{ color:{COLOR_TEXT_DARK}; background:transparent; border:none; }}
        """)
        self._setup_ui()
        if creds:
            self._inp_nama_toko.setText(creds.get("nama_toko", ""))
            self._inp_pemilik.setText(creds.get("nama_pemilik", ""))
            self._inp_alamat.setText(creds.get("alamat", ""))
            self._inp_telepon.setText(creds.get("telepon", ""))

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 28, 28, 24)
        layout.setSpacing(4)

        title = QLabel("🏪  Tambah / Ubah Informasi Toko")
        title.setStyleSheet(f"font-size:19px; font-weight:800; color:{COLOR_TEXT_DARK};")
        layout.addWidget(title)
        layout.addSpacing(4)

        desc = QLabel("Informasi ini akan ditampilkan pada struk dan laporan cetak.")
        desc.setStyleSheet(f"color:{COLOR_TEXT_MUTED}; font-size:13px;")
        desc.setWordWrap(True)
        layout.addWidget(desc)
        layout.addSpacing(14)

        self._inp_nama_toko = _field(layout, "Nama Toko",    "Masukkan nama toko")
        self._inp_pemilik   = _field(layout, "Nama Pemilik", "Masukkan nama pemilik")
        self._inp_alamat    = _field(layout, "Alamat",       "Masukkan alamat toko")
        self._inp_telepon   = _field(layout, "No. Telepon",  "Contoh: 0812-3456-7890")

        btns = _dialog_buttons(layout, "💾  Simpan")
        btns.accepted.connect(self._validate_and_accept)
        btns.rejected.connect(self.reject)

    def _validate_and_accept(self):
        if not self._inp_nama_toko.text().strip():
            QMessageBox.warning(self, "Input Kosong", "Nama toko tidak boleh kosong.")
            return
        self.accept()

    def get_data(self) -> dict:
        return {
            "nama_toko":    self._inp_nama_toko.text().strip(),
            "nama_pemilik": self._inp_pemilik.text().strip(),
            "alamat":       self._inp_alamat.text().strip(),
            "telepon":      self._inp_telepon.text().strip(),
        }

# DIALOG — Ubah Username
class UbahUsernameDialog(QDialog):
    def __init__(self, parent=None, current_username: str = ""):
        super().__init__(parent)
        self.setWindowTitle("Ubah Username")
        self.setFixedWidth(420)
        self.setModal(True)
        self.setStyleSheet(f"""
            QDialog {{ background:#f8fafc; font-family:'Segoe UI'; }}
            QLabel  {{ color:{COLOR_TEXT_DARK}; background:transparent; border:none; }}
        """)
        self._current_username = current_username
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 28, 28, 24)
        layout.setSpacing(4)

        title = QLabel("👤  Ubah Username")
        title.setStyleSheet(f"font-size:19px; font-weight:800; color:{COLOR_TEXT_DARK};")
        layout.addWidget(title)
        layout.addSpacing(4)

        desc = QLabel("Masukkan password Anda untuk konfirmasi, lalu isi username baru.")
        desc.setStyleSheet(f"color:{COLOR_TEXT_MUTED}; font-size:13px;")
        desc.setWordWrap(True)
        layout.addWidget(desc)
        layout.addSpacing(14)

        self._inp_username = _field(layout, "Username Baru", "Masukkan username baru")
        self._inp_pw       = _field(layout, "Password (konfirmasi)", "", echo=True)
        self._inp_username.setText(self._current_username)

        btns = _dialog_buttons(layout, "🔄  Ubah Username")
        btns.accepted.connect(self._validate_and_accept)
        btns.rejected.connect(self.reject)

    def _validate_and_accept(self):
        pw       = self._inp_pw.text()
        username = self._inp_username.text().strip()

        if not pw or not username:
            QMessageBox.warning(self, "Tidak Lengkap", "Semua field wajib diisi.")
            return
        if not verify_login(self._current_username, pw):
            QMessageBox.warning(self, "Password Salah", "Password yang Anda masukkan tidak sesuai.")
            return
        if len(username) < 3:
            QMessageBox.warning(self, "Username Terlalu Pendek", "Username minimal 3 karakter.")
            return
        self.accept()

    def get_username(self) -> str:
        return self._inp_username.text().strip()

# DIALOG — Ubah Password
class UbahPasswordDialog(QDialog):
    def __init__(self, parent=None, current_username: str = ""):
        super().__init__(parent)
        self.setWindowTitle("Ubah Password")
        self.setFixedWidth(420)
        self.setModal(True)
        self.setStyleSheet(f"""
            QDialog {{ background:#f8fafc; font-family:'Segoe UI'; }}
            QLabel  {{ color:{COLOR_TEXT_DARK}; background:transparent; border:none; }}
        """)
        self._current_username = current_username
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 28, 28, 24)
        layout.setSpacing(4)

        title = QLabel("🔒  Ubah Password")
        title.setStyleSheet(f"font-size:19px; font-weight:800; color:{COLOR_TEXT_DARK};")
        layout.addWidget(title)
        layout.addSpacing(4)

        desc = QLabel("Masukkan password lama, lalu isi password baru.")
        desc.setStyleSheet(f"color:{COLOR_TEXT_MUTED}; font-size:13px;")
        desc.setWordWrap(True)
        layout.addWidget(desc)
        layout.addSpacing(14)

        self._inp_pw_lama    = _field(layout, "Password Lama",            "", echo=True)
        self._inp_pw_baru    = _field(layout, "Password Baru",            "", echo=True)
        self._inp_pw_konfirm = _field(layout, "Konfirmasi Password Baru", "", echo=True)

        btns = _dialog_buttons(layout, "🔒  Ubah Password")
        btns.accepted.connect(self._validate_and_accept)
        btns.rejected.connect(self.reject)

    def _validate_and_accept(self):
        pw_lama    = self._inp_pw_lama.text()
        pw_baru    = self._inp_pw_baru.text()
        pw_konfirm = self._inp_pw_konfirm.text()

        if not all([pw_lama, pw_baru, pw_konfirm]):
            QMessageBox.warning(self, "Tidak Lengkap", "Semua field wajib diisi.")
            return
        if not verify_login(self._current_username, pw_lama):
            QMessageBox.warning(self, "Password Salah", "Password lama yang Anda masukkan tidak sesuai.")
            return
        if pw_baru != pw_konfirm:
            QMessageBox.warning(self, "Tidak Cocok", "Password baru dan konfirmasi tidak sama.")
            return
        if len(pw_baru) < 6:
            QMessageBox.warning(self, "Password Lemah", "Password minimal 6 karakter.")
            return
        self.accept()

    def get_password(self) -> str:
        return self._inp_pw_baru.text()

# HALAMAN PENGATURAN
class PengaturanPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self._setup_ui()

    # ==========================================================
    def _setup_ui(self):
        self.setStyleSheet(PAGE_STYLE)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setStyleSheet("QScrollArea { border:none; background:#f4f7fb; }")
        main_layout.addWidget(scroll)

        container = QWidget()
        scroll.setWidget(container)

        root = QVBoxLayout(container)
        root.setContentsMargins(30, 24, 30, 24)
        root.setSpacing(20)

        h1 = QLabel("⚙  Pengaturan Aplikasi")
        h1.setStyleSheet(f"font-size:32px; font-weight:800; color:{COLOR_TEXT_DARK};")
        sub = QLabel("Kelola informasi toko dan akun pengguna")
        sub.setStyleSheet(f"color:{COLOR_TEXT_MUTED}; font-size:14px;")
        root.addWidget(h1)
        root.addWidget(sub)

        root.addWidget(self._build_toko_card())
        root.addWidget(self._build_akun_card())
        root.addStretch()

        self.reload_data()

    # ----------------------------------------------------------
    def _build_toko_card(self) -> QFrame:
        card = QFrame()
        card.setMaximumWidth(640)
        card.setStyleSheet(CARD_STYLE)
        cl = QVBoxLayout(card)
        cl.setContentsMargins(28, 24, 28, 24)
        cl.setSpacing(4)

        title = QLabel("🏪  Informasi Toko")
        title.setStyleSheet(f"font-size:18px; font-weight:800; color:{COLOR_TEXT_DARK};")
        cl.addWidget(title)
        cl.addSpacing(10)

        self._lbl_nama_toko = QLabel("—")
        self._lbl_pemilik   = QLabel("—")
        self._lbl_alamat    = QLabel("—")
        self._lbl_telepon   = QLabel("—")

        for lbl in [self._lbl_nama_toko, self._lbl_pemilik,
                    self._lbl_alamat, self._lbl_telepon]:
            lbl.setStyleSheet(f"font-size:14px; color:{COLOR_TEXT_DARK};")
            lbl.setWordWrap(True)
            cl.addWidget(lbl)

        cl.addSpacing(14)

        btn = QPushButton("✏  Tambah / Ubah Data Toko")
        btn.setFixedHeight(44)
        btn.setCursor(QCursor(Qt.PointingHandCursor))
        btn.setStyleSheet(BTN_PRIMARY_STYLE)
        btn.clicked.connect(self._open_toko_dialog)
        cl.addWidget(btn)

        return card

    # ----------------------------------------------------------
    def _build_akun_card(self) -> QFrame:
        card = QFrame()
        card.setMaximumWidth(640)
        card.setStyleSheet(CARD_STYLE)
        cl = QVBoxLayout(card)
        cl.setContentsMargins(28, 24, 28, 24)
        cl.setSpacing(4)

        title = QLabel("🔐  Akun Pengguna")
        title.setStyleSheet(f"font-size:18px; font-weight:800; color:{COLOR_TEXT_DARK};")
        cl.addWidget(title)
        cl.addSpacing(10)

        self._lbl_username = QLabel("—")
        self._lbl_username.setStyleSheet(f"font-size:14px; color:{COLOR_TEXT_DARK};")
        cl.addWidget(self._lbl_username)

        cl.addSpacing(14)

        btn_row = QHBoxLayout()
        btn_row.setSpacing(10)

        btn_user = QPushButton("👤  Ubah Username")
        btn_user.setFixedHeight(44)
        btn_user.setCursor(QCursor(Qt.PointingHandCursor))
        btn_user.setStyleSheet("""
            QPushButton {
                background:#3b82f6; color:white; border:none;
                border-radius:10px; font-size:14px; font-weight:bold;
            }
            QPushButton:hover { background:#2563eb; }
        """)
        btn_user.clicked.connect(self._open_username_dialog)

        btn_pw = QPushButton("🔒  Ubah Password")
        btn_pw.setFixedHeight(44)
        btn_pw.setCursor(QCursor(Qt.PointingHandCursor))
        btn_pw.setStyleSheet(BTN_SECONDARY_STYLE)
        btn_pw.clicked.connect(self._open_password_dialog)

        btn_row.addWidget(btn_user)
        btn_row.addWidget(btn_pw)
        cl.addLayout(btn_row)

        return card

    # DIALOG TOKO
    def _open_toko_dialog(self):
        creds = load_credentials()
        dlg = InfoTokoDialog(self, creds=creds)
        if dlg.exec() != QDialog.Accepted:
            return
        d = dlg.get_data()
        update_info_toko(d["nama_toko"], d["nama_pemilik"], d["alamat"], d["telepon"])
        self.reload_data()
        QMessageBox.information(self, "Berhasil", "Informasi toko berhasil disimpan.")

    # DIALOG USERNAME
    def _open_username_dialog(self):
        creds = load_credentials()
        dlg = UbahUsernameDialog(self, current_username=creds.get("username", ""))
        if dlg.exec() != QDialog.Accepted:
            return
        new_username = dlg.get_username()

        from database.db import pengguna_update_akun
        pengguna_update_akun(creds["username"], new_username, creds["password"])

        self.reload_data()
        win = self.main_window
        if hasattr(win, "dashboard"):
            win.dashboard.update_user_display(new_username)
        QMessageBox.information(self, "Berhasil", f"Username berhasil diubah menjadi '{new_username}'.")

    # DIALOG PASSWORD
    def _open_password_dialog(self):
        creds = load_credentials()
        dlg = UbahPasswordDialog(self, current_username=creds.get("username", ""))
        if dlg.exec() != QDialog.Accepted:
            return
        new_password = dlg.get_password()
        update_credentials(creds["username"], new_password)
        QMessageBox.information(self, "Berhasil", "Password berhasil diubah.")

    # MUAT ULANG RINGKASAN DATA
    def reload_data(self):
        creds = load_credentials()

        nama_toko = creds.get("nama_toko", "")
        self._lbl_nama_toko.setText(f"Nama Toko: {nama_toko or '(belum diatur)'}")
        self._lbl_pemilik.setText(f"Nama Pemilik: {creds.get('nama_pemilik', '') or '(belum diatur)'}")
        self._lbl_alamat.setText(f"Alamat: {creds.get('alamat', '') or '(belum diatur)'}")
        self._lbl_telepon.setText(f"No. Telepon: {creds.get('telepon', '') or '(belum diatur)'}")
        self._lbl_username.setText(f"Username: {creds.get('username', '')}")