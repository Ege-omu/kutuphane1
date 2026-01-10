from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit, QPushButton,
    QTableWidget, QTableWidgetItem, QMessageBox, QLabel
)

from uye import uyeleri_getir
from kitap import kitaplari_listele
from odunc import kitap_odunc_ver


class OduncWindow(QWidget):
    def __init__(self, kullanici_id):
        super().__init__()
        self.kullanici_id = kullanici_id

        self.setWindowTitle("Kitap Ödünç Ver")
        self.setFixedSize(850, 550)

        self.init_ui()
        self.uye_listele()
        self.kitap_listele()

    def init_ui(self):
        layout = QVBoxLayout()

        self.txt_uye_ara = QLineEdit()
        self.txt_uye_ara.setPlaceholderText("Üye ara (Ad / Soyad / Email)")
        self.txt_uye_ara.textChanged.connect(self.uye_listele)

        self.tbl_uye = QTableWidget()
        self.tbl_uye.setColumnCount(4)
        self.tbl_uye.setHorizontalHeaderLabels(
            ["ID", "Ad", "Soyad", "Email"]
        )

        self.txt_kitap_ara = QLineEdit()
        self.txt_kitap_ara.setPlaceholderText("Kitap ara (Ad / Yazar)")
        self.txt_kitap_ara.textChanged.connect(self.kitap_listele)

        self.tbl_kitap = QTableWidget()
        self.tbl_kitap.setColumnCount(7)
        self.tbl_kitap.setHorizontalHeaderLabels(
            ["ID", "Ad", "Yazar", "Kategori", "Yayınevi", "Basım Yılı","Mevcut"]
        )

        self.lbl_stok = QLabel("Mevcut Adet: -")
        self.tbl_kitap.itemSelectionChanged.connect(self.stok_goster)

        btn_odunc = QPushButton("Ödünç Ver")
        btn_odunc.clicked.connect(self.odunc_ver)

        layout.addWidget(self.txt_uye_ara)
        layout.addWidget(self.tbl_uye)
        layout.addWidget(self.txt_kitap_ara)
        layout.addWidget(self.tbl_kitap)
        layout.addWidget(self.lbl_stok)
        layout.addWidget(btn_odunc)

        self.setLayout(layout)

    def uye_listele(self):
        rows = uyeleri_getir(self.txt_uye_ara.text())
        self.tbl_uye.setRowCount(len(rows))

        for i, row in enumerate(rows):
            for j, val in enumerate(row):
                self.tbl_uye.setItem(i, j, QTableWidgetItem(str(val)))

    def kitap_listele(self):
        rows = kitaplari_listele(self.txt_kitap_ara.text())
        self.tbl_kitap.setRowCount(len(rows))

        for i, row in enumerate(rows):
            for j, val in enumerate(row):
                self.tbl_kitap.setItem(i, j, QTableWidgetItem(str(val)))

    def stok_goster(self):
        row = self.tbl_kitap.currentRow()
        if row >= 0:
            stok = self.tbl_kitap.item(row, 6).text()
            self.lbl_stok.setText(f"Mevcut Adet: {stok}")

    def odunc_ver(self):
        uye_row = self.tbl_uye.currentRow()
        kitap_row = self.tbl_kitap.currentRow()

        if uye_row < 0 or kitap_row < 0:
            QMessageBox.warning(self, "Uyarı", "Üye ve kitap seçiniz")
            return

        uye_id = int(self.tbl_uye.item(uye_row, 0).text())
        kitap_id = int(self.tbl_kitap.item(kitap_row, 0).text())

        basarili, mesaj = kitap_odunc_ver(
            uye_id, kitap_id, self.kullanici_id
        )

        if basarili:
            QMessageBox.information(self, "Başarılı", mesaj)
            self.kitap_listele()
        else:
            QMessageBox.critical(self, "Hata", mesaj)