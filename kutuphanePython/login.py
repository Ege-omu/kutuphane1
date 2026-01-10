from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel,
    QLineEdit, QPushButton, QMessageBox
)
from db import get_connection


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Giriş")
        self.setFixedSize(300, 200)
        self.init_ui()

    def init_ui(self):
        lbl_user = QLabel("Kullanıcı Adı")
        lbl_pass = QLabel("Şifre")

        self.txt_user = QLineEdit()
        self.txt_pass = QLineEdit()
        self.txt_pass.setEchoMode(QLineEdit.Password)

        btn_login = QPushButton("Giriş Yap")
        btn_login.clicked.connect(self.login)

        layout = QVBoxLayout()
        layout.addWidget(lbl_user)
        layout.addWidget(self.txt_user)
        layout.addWidget(lbl_pass)
        layout.addWidget(self.txt_pass)
        layout.addWidget(btn_login)

        self.setLayout(layout)

    def login(self):
        kullanici_adi = self.txt_user.text()
        sifre = self.txt_pass.text()

        if not kullanici_adi or not sifre:
            QMessageBox.warning(self, "Uyarı", "Alanlar boş olamaz")
            return

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT kullanici_id, rol_id, kullanici_adi
            FROM kullanicilar
            WHERE kullanici_adi = %s
              AND sifre = %s
              AND aktif = TRUE
        """, (kullanici_adi, sifre))

        row = cur.fetchone()
        cur.close()
        conn.close()

        if row:
            kullanici_id, rol_id, kullanici_adi = row
            self.open_main_window(kullanici_id, rol_id, kullanici_adi)
            self.close()
        else:
            QMessageBox.critical(self, "Hata", "Giriş başarısız")

    def open_main_window(self, kullanici_id, rol_id, kullanici_adi):
        from main_window import MainWindow
        self.main_window = MainWindow(kullanici_id, rol_id, kullanici_adi)
        self.main_window.show()
