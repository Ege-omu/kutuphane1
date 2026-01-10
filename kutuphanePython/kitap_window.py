from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QTableWidget,
    QTableWidgetItem, QMessageBox, QComboBox,
    QInputDialog
)

from kitap import (
    kitaplari_listele,
    kitap_ekle,
    kitap_silinebilir_mi,
    kitap_sil
)
from kategori import kategori_ekle, kategorileri_getir


class KitapWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kitap Yönetimi")
        self.setFixedSize(700, 450)

        self.init_ui()
        self.kategorileri_doldur()
        self.listele()

    def init_ui(self):
        self.txt_ara = QLineEdit()
        self.txt_ara.setPlaceholderText("Kitap adı / Yazar ara")
        self.txt_ara.textChanged.connect(self.listele)

        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "ID", "Ad", "Yazar", "Kategori",
            "Yayınevi", "Basım Yılı", "Mevcut"
        ])

        self.txt_ad = QLineEdit()
        self.txt_ad.setPlaceholderText("Kitap Adı")

        self.txt_yazar = QLineEdit()
        self.txt_yazar.setPlaceholderText("Yazar")

        self.txt_yayin = QLineEdit()
        self.txt_yayin.setPlaceholderText("Yayınevi")

        self.txt_yil = QLineEdit()
        self.txt_yil.setPlaceholderText("Basım Yılı")

        self.txt_toplam = QLineEdit()
        self.txt_toplam.setPlaceholderText("Toplam Adet")

        self.cmb_kategori = QComboBox()
        self.btn_kategori_ekle = QPushButton("+")
        self.btn_kategori_ekle.setFixedWidth(30)
        self.btn_kategori_ekle.clicked.connect(self.yeni_kategori)

        kat_layout = QHBoxLayout()
        kat_layout.addWidget(self.cmb_kategori)
        kat_layout.addWidget(self.btn_kategori_ekle)

        btn_ekle = QPushButton("Yeni Kitap Ekle")
        btn_sil = QPushButton("Seçili Kitabı Sil")
        btn_ekle.clicked.connect(self.ekle)
        btn_sil.clicked.connect(self.sil)

        layout = QVBoxLayout()
        layout.addWidget(self.txt_ara)
        layout.addWidget(self.table)
        layout.addWidget(self.txt_ad)
        layout.addWidget(self.txt_yazar)
        layout.addLayout(kat_layout)
        layout.addWidget(self.txt_yayin)
        layout.addWidget(self.txt_yil)
        layout.addWidget(self.txt_toplam)
        layout.addWidget(btn_ekle)
        layout.addWidget(btn_sil)

        self.setLayout(layout)

    def listele(self):
        rows = kitaplari_listele(self.txt_ara.text())
        self.table.setRowCount(len(rows))
        for i, row in enumerate(rows):
            for j, val in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(val)))

    def ekle(self):
        try:
            kitap_ekle(
                self.txt_ad.text(),
                self.txt_yazar.text(),
                self.cmb_kategori.currentData(),
                self.txt_yayin.text(),
                int(self.txt_yil.text()),
                int(self.txt_toplam.text())
            )
            self.listele()
        except Exception as e:
            QMessageBox.critical(self, "Hata", str(e))

    def sil(self):
        row = self.table.currentRow()
        if row < 0:
            return

        kitap_id = int(self.table.item(row, 0).text())

        if not kitap_silinebilir_mi(kitap_id):
            QMessageBox.warning(
                self,
                "Uyarı",
                "Kitabın aktif ödünç kaydı var, silinemez!"
            )
            return

        kitap_sil(kitap_id)
        self.listele()

    def kategorileri_doldur(self):
        self.cmb_kategori.clear()
        for kid, kad in kategorileri_getir():
            self.cmb_kategori.addItem(kad, kid)

    def yeni_kategori(self):
        ad, ok = QInputDialog.getText(
            self,
            "Yeni Kategori",
            "Kategori adı:"
        )

        if ok and ad.strip():
            kategori_ekle(ad.strip())
            self.kategorileri_doldur()
        else:
            QMessageBox.warning(self, "Uyarı", "Kategori adı boş olamaz")
