from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLineEdit,
    QTableWidget, QTableWidgetItem, QMessageBox
)
from uye import uyeleri_getir, uye_ekle, uye_silinebilir_mi, uye_sil


class UyeWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Üye Yönetimi")
        self.setFixedSize(600, 400)
        self.init_ui()
        self.listele()

    def init_ui(self):
        self.txt_ara = QLineEdit()
        self.txt_ara.setPlaceholderText("Ad / Soyad / Email ara")
        self.txt_ara.textChanged.connect(self.listele)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(
            ["ID", "Ad", "Soyad", "Email", "Telefon"]
        )

        self.txt_ad = QLineEdit()
        self.txt_ad.setPlaceholderText("Ad")
        self.txt_soyad = QLineEdit()
        self.txt_soyad.setPlaceholderText("Soyad")
        self.txt_email = QLineEdit()
        self.txt_email.setPlaceholderText("Email")
        self.txt_tel = QLineEdit()
        self.txt_tel.setPlaceholderText("Telefon")

        btn_ekle = QPushButton("Yeni Üye Ekle")
        btn_sil = QPushButton("Seçili Üyeyi Sil")

        btn_ekle.clicked.connect(self.ekle)
        btn_sil.clicked.connect(self.sil)

        layout = QVBoxLayout()
        layout.addWidget(self.txt_ara)
        layout.addWidget(self.table)
        layout.addWidget(self.txt_ad)
        layout.addWidget(self.txt_soyad)
        layout.addWidget(self.txt_email)
        layout.addWidget(self.txt_tel)
        layout.addWidget(btn_ekle)
        layout.addWidget(btn_sil)

        self.setLayout(layout)

    def listele(self):
        rows = uyeleri_getir(self.txt_ara.text())
        self.table.setRowCount(len(rows))
        for i, row in enumerate(rows):
            for j, val in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(val)))

    def ekle(self):
        try:
            uye_ekle(
                self.txt_ad.text(),
                self.txt_soyad.text(),
                self.txt_email.text(),
                self.txt_tel.text()
            )
            self.listele()
        except Exception as e:
            QMessageBox.critical(self, "Hata", str(e))

    def sil(self):
        row = self.table.currentRow()
        if row < 0:
            return

        uye_id = int(self.table.item(row, 0).text())

        if not uye_silinebilir_mi(uye_id):
            QMessageBox.warning(
                self,
                "Uyarı",
                "Üyenin aktif ödünç kaydı var, silinemez!"
            )
            return

        uye_sil(uye_id)
        self.listele()
