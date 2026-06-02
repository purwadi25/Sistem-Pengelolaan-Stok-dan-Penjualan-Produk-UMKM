# =========================================================
# LOGOUT FUNCTION
# =========================================================
def logout(self):

    konfirmasi = QMessageBox.question(
        self,
        "Logout",
        "Apakah Anda yakin ingin logout?",
        QMessageBox.Yes | QMessageBox.No
    )

    if konfirmasi == QMessageBox.Yes:

        # buka halaman login lagi
        self.login_window = LoginWindow()
        self.login_window.show()

        # tutup window sekarang
        self.close()