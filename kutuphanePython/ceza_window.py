from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QTableWidget,
    QTableWidgetItem, QMessageBox, QComboBox, QDateEdit
)
from PyQt5.QtCore import QDate

from db import get_connection


class CezaWindow(QWidget):
    def __init__(self, kullanici_id):
        super().__init__()
        self.kullanici_id = kullanici_id

        self.setWindowTitle("Ceza Görüntüleme")
        self.setFixedSize(900, 500)

        self.init_ui()
        self.uyeleri_doldur()
        self.cezalari_listele()

    def init_ui(self):
        main_layout = QVBoxLayout()

        filter_layout = QHBoxLayout()

        self.cmb_uye = QComboBox()
        self.cmb_uye.addItem("Tüm Üyeler", None)
        self.cmb_uye.currentIndexChanged.connect(self.cezalari_listele)

        self.date_baslangic = QDateEdit()
        self.date_baslangic.setCalendarPopup(True)
        self.date_baslangic.setDate(QDate.currentDate().addMonths(-1))

        self.date_bitis = QDateEdit()
        self.date_bitis.setCalendarPopup(True)
        self.date_bitis.setDate(QDate.currentDate())

        btn_filtre = QPushButton("Filtrele")
        btn_filtre.clicked.connect(self.cezalari_listele)

        filter_layout.addWidget(QLabel("Üye:"))
        filter_layout.addWidget(self.cmb_uye)
        filter_layout.addWidget(QLabel("Başlangıç:"))
        filter_layout.addWidget(self.date_baslangic)
        filter_layout.addWidget(QLabel("Bitiş:"))
        filter_layout.addWidget(self.date_bitis)
        filter_layout.addWidget(btn_filtre)

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "Ceza ID", "Üye", "Kitap",
            "Gecikme (Gün)", "Tutar", "Ödendi"
        ])

        self.lbl_toplam = QLabel("Toplam Borç: 0 TL")

        main_layout.addLayout(filter_layout)
        main_layout.addWidget(self.table)
        main_layout.addWidget(self.lbl_toplam)

        self.setLayout(main_layout)

    def uyeleri_doldur(self):
        conn = get_connection(self.kullanici_id)
        cur = conn.cursor()

        cur.execute("""
            SELECT uye_id, ad || ' ' || soyad
            FROM uyeler
            ORDER BY ad
        """)

        for uid, ad in cur.fetchall():
            self.cmb_uye.addItem(ad, uid)

        cur.close()
        conn.close()

    def cezalari_listele(self):
        conn = get_connection(self.kullanici_id)
        cur = conn.cursor()

        uye_id = self.cmb_uye.currentData()
        bas = self.date_baslangic.date().toPyDate()
        bit = self.date_bitis.date().toPyDate()

        query = """
            SELECT
                c.ceza_id,
                u.ad || ' ' || u.soyad,
                k.ad,
                c.gecikme_gunu,
                c.tutar,
                c.odendi
            FROM cezalar c
            JOIN uyeler u ON u.uye_id = c.uye_id
            JOIN odunc o ON o.odunc_id = c.odunc_id
            JOIN kitaplar k ON k.kitap_id = o.kitap_id
            WHERE c.odendi = FALSE
            AND c.ceza_id IS NOT NULL
            AND c.odunc_id IS NOT NULL
            AND o.alis_tarihi BETWEEN %s AND %s
        """

        params = [bas, bit]

        if uye_id:
            query += " AND u.uye_id = %s"
            params.append(uye_id)

        cur.execute(query, params)
        rows = cur.fetchall()

        self.table.setRowCount(len(rows))

        toplam = 0
        for i, row in enumerate(rows):
            for j, val in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(val)))
            toplam += float(row[4])

        self.lbl_toplam.setText(f"Toplam Borç: {toplam:.2f} TL")

        cur.close()
        conn.close()