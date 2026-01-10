from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit, QPushButton,
    QTableWidget, QTableWidgetItem, QMessageBox, QLabel
)

from db import get_connection
from odunc import kitap_teslim_al


class TeslimWindow(QWidget):
    def __init__(self, kullanici_id):
        super().__init__()
        self.kullanici_id = kullanici_id

        self.setWindowTitle("Kitap Teslim Al")
        self.setFixedSize(900, 500)

        self.init_ui()
        self.odunc_listele()

    def init_ui(self):
        layout = QVBoxLayout()

        self.txt_ara = QLineEdit()
        self.txt_ara.setPlaceholderText("Üye adı / Kitap adı ara")
        self.txt_ara.textChanged.connect(self.odunc_listele)

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "ID", "Üye", "Kitap",
            "Alış Tarihi", "Son Teslim", "Durum"
        ])

        self.lbl_detay = QLabel("Detay: -")

        self.table.itemSelectionChanged.connect(self.detay_goster)

        btn_teslim = QPushButton("Teslim Al")
        btn_teslim.clicked.connect(self.teslim_al)

        layout.addWidget(self.txt_ara)
        layout.addWidget(self.table)
        layout.addWidget(self.lbl_detay)
        layout.addWidget(btn_teslim)

        self.setLayout(layout)

    def odunc_listele(self):
        conn = get_connection(self.kullanici_id)
        cur = conn.cursor()

        q = self.txt_ara.text()

        cur.execute("""
            SELECT
                o.odunc_id,
                u.ad || ' ' || u.soyad,
                k.ad,
                o.alis_tarihi,
                o.son_teslim_tarihi,
                o.durum
            FROM odunc o
            JOIN uyeler u ON u.uye_id = o.uye_id
            JOIN kitaplar k ON k.kitap_id = o.kitap_id
            WHERE o.iade_tarihi IS NULL
            AND (
                u.ad ILIKE %s OR
                u.soyad ILIKE %s OR
                k.ad ILIKE %s
            )
            ORDER BY o.alis_tarihi
        """, (f"%{q}%", f"%{q}%", f"%{q}%"))

        rows = cur.fetchall()
        self.table.setRowCount(len(rows))

        for i, row in enumerate(rows):
            for j, val in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(val)))

        cur.close()
        conn.close()

    def detay_goster(self):
        row = self.table.currentRow()
        if row >= 0:
            uye = self.table.item(row, 1).text()
            kitap = self.table.item(row, 2).text()
            son = self.table.item(row, 4).text()

            self.lbl_detay.setText(
                f"Üye: {uye} | Kitap: {kitap} | Son Teslim: {son}"
            )

    def teslim_al(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Uyarı", "Bir kayıt seçiniz")
            return

        odunc_id = int(self.table.item(row, 0).text())

        basarili, mesaj = kitap_teslim_al(
            odunc_id, self.kullanici_id
        )

        if basarili:
            QMessageBox.information(self, "Başarılı", mesaj)
            self.odunc_listele()
        else:
            QMessageBox.critical(self, "Hata", mesaj)
