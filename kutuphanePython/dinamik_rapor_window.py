from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QTableWidget,
    QTableWidgetItem, QComboBox, QCheckBox,
    QMessageBox, QFileDialog
)
from db import get_connection


class DinamikRaporWindow(QWidget):
    def __init__(self, kullanici_id):
        super().__init__()
        self.kullanici_id = kullanici_id

        self.setWindowTitle("Dinamik Kitap Arama & Rapor")
        self.setFixedSize(1000, 600)

        self.init_ui()
        self.kategorileri_doldur()

    def init_ui(self):
        main = QVBoxLayout()

        f = QHBoxLayout()

        self.txt_ad = QLineEdit()
        self.txt_ad.setPlaceholderText("Kitap Adı")

        self.txt_yazar = QLineEdit()
        self.txt_yazar.setPlaceholderText("Yazar")

        self.cmb_kategori = QComboBox()
        self.cmb_kategori.addItem("Tümü", None)

        self.txt_min = QLineEdit()
        self.txt_min.setPlaceholderText("Min Basım Yılı")

        self.txt_max = QLineEdit()
        self.txt_max.setPlaceholderText("Max Basım Yılı")

        self.chk_mevcut = QCheckBox("Sadece Mevcut Kitaplar")

        btn_ara = QPushButton("Ara")
        btn_ara.clicked.connect(self.sorgula)

        f.addWidget(self.txt_ad)
        f.addWidget(self.txt_yazar)
        f.addWidget(self.cmb_kategori)
        f.addWidget(self.txt_min)
        f.addWidget(self.txt_max)
        f.addWidget(self.chk_mevcut)
        f.addWidget(btn_ara)

        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "ID", "Kitap", "Yazar", "Kategori",
            "Basım Yılı", "Toplam", "Mevcut"
        ])

        btn_export = QPushButton("Excel'e Aktar")
        btn_export.clicked.connect(self.export_excel)

        main.addLayout(f)
        main.addWidget(self.table)
        main.addWidget(btn_export)

        self.setLayout(main)

    def kategorileri_doldur(self):
        conn = get_connection(self.kullanici_id)
        cur = conn.cursor()

        cur.execute("SELECT kategori_id, kategori_adi FROM kategoriler")
        for kid, kad in cur.fetchall():
            self.cmb_kategori.addItem(kad, kid)

        cur.close()
        conn.close()

    def sorgula(self):
        conn = get_connection(self.kullanici_id)
        cur = conn.cursor()

        sql = """
            SELECT
                k.kitap_id,
                k.ad,
                k.yazar,
                kat.kategori_adi,
                k.basim_yili,
                k.toplam_kopya,
                k.mevcut_kopya
            FROM kitaplar k
            LEFT JOIN kategoriler kat ON kat.kategori_id = k.kategori_id
            WHERE 1=1
        """

        params = []

        if self.txt_ad.text():
            sql += " AND k.ad ILIKE %s"
            params.append(f"%{self.txt_ad.text()}%")

        if self.txt_yazar.text():
            sql += " AND k.yazar ILIKE %s"
            params.append(f"%{self.txt_yazar.text()}%")

        if self.cmb_kategori.currentData():
            sql += " AND k.kategori_id = %s"
            params.append(self.cmb_kategori.currentData())

        if self.txt_min.text():
            sql += " AND k.basim_yili >= %s"
            params.append(int(self.txt_min.text()))

        if self.txt_max.text():
            sql += " AND k.basim_yili <= %s"
            params.append(int(self.txt_max.text()))

        if self.chk_mevcut.isChecked():
            sql += " AND k.mevcut_kopya > 0"

        sql += " ORDER BY k.ad"

        cur.execute(sql, params)
        rows = cur.fetchall()

        self.table.setRowCount(len(rows))
        for i, row in enumerate(rows):
            for j, val in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(val)))

        cur.close()
        conn.close()

    def export_excel(self):
        path, _ = QFileDialog.getSaveFileName(
            self, "Kaydet", "", "CSV Files (*.csv)"
        )

        if not path:
            return

        with open(path, "w", encoding="utf-8") as f:
            headers = [
                self.table.horizontalHeaderItem(i).text()
                for i in range(self.table.columnCount())
            ]
            f.write(",".join(headers) + "\n")

            for r in range(self.table.rowCount()):
                row = []
                for c in range(self.table.columnCount()):
                    row.append(self.table.item(r, c).text())
                f.write(",".join(row) + "\n")

        QMessageBox.information(self, "Başarılı", "Excel dosyası oluşturuldu")