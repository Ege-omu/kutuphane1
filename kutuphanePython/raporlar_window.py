from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QTableWidget,
    QTableWidgetItem, QComboBox, QDateEdit
)
from PyQt5.QtCore import QDate
from db import get_connection


class RaporWindow(QWidget):
    def __init__(self, kullanici_id):
        super().__init__()
        self.kullanici_id = kullanici_id

        self.setWindowTitle("Raporlar")
        self.setFixedSize(900, 500)

        self.init_ui()
        self.uyeleri_doldur()
        self.kategorileri_doldur()

    def init_ui(self):
        layout = QVBoxLayout()

        ust = QHBoxLayout()

        self.cmb_rapor = QComboBox()
        self.cmb_rapor.addItems([
            "Tarih Aralığına Göre Ödünçler",
            "Geciken Kitaplar",
            "En Çok Ödünç Alınan Kitaplar"
        ])

        self.date_bas = QDateEdit()
        self.date_bas.setCalendarPopup(True)
        self.date_bas.setDate(QDate.currentDate().addMonths(-1))

        self.date_bit = QDateEdit()
        self.date_bit.setCalendarPopup(True)
        self.date_bit.setDate(QDate.currentDate())

        self.cmb_uye = QComboBox()
        self.cmb_uye.addItem("Tüm Üyeler", None)

        self.cmb_kategori = QComboBox()
        self.cmb_kategori.addItem("Tüm Kategoriler", None)

        btn_getir = QPushButton("Raporu Getir")
        btn_getir.clicked.connect(self.raporu_getir)

        ust.addWidget(QLabel("Rapor:"))
        ust.addWidget(self.cmb_rapor)
        ust.addWidget(QLabel("Başlangıç:"))
        ust.addWidget(self.date_bas)
        ust.addWidget(QLabel("Bitiş:"))
        ust.addWidget(self.date_bit)
        ust.addWidget(self.cmb_uye)
        ust.addWidget(self.cmb_kategori)
        ust.addWidget(btn_getir)

        self.table = QTableWidget()

        layout.addLayout(ust)
        layout.addWidget(self.table)

        self.setLayout(layout)

    def uyeleri_doldur(self):
        conn = get_connection(self.kullanici_id)
        cur = conn.cursor()
        cur.execute("SELECT uye_id, ad || ' ' || soyad FROM uyeler")
        for uid, ad in cur.fetchall():
            self.cmb_uye.addItem(ad, uid)
        conn.close()

    def kategorileri_doldur(self):
        conn = get_connection(self.kullanici_id)
        cur = conn.cursor()
        cur.execute("SELECT kategori_id, kategori_adi FROM kategoriler")
        for kid, kad in cur.fetchall():
            self.cmb_kategori.addItem(kad, kid)
        conn.close()

    def raporu_getir(self):
        rapor = self.cmb_rapor.currentText()

        if rapor == "Tarih Aralığına Göre Ödünçler":
            self.rapor_odunc()
        elif rapor == "Geciken Kitaplar":
            self.rapor_geciken()
        elif rapor == "En Çok Ödünç Alınan Kitaplar":
            self.rapor_populer()

    def rapor_odunc(self):
        conn = get_connection(self.kullanici_id)
        cur = conn.cursor()

        sql = """
            SELECT
                u.ad || ' ' || u.soyad,
                k.ad,
                kat.kategori_adi,
                o.alis_tarihi,
                o.son_teslim_tarihi,
                o.durum
            FROM odunc o
            JOIN uyeler u ON u.uye_id = o.uye_id
            JOIN kitaplar k ON k.kitap_id = o.kitap_id
            LEFT JOIN kategoriler kat ON kat.kategori_id = k.kategori_id
            WHERE o.alis_tarihi BETWEEN %s AND %s
            AND (%s IS NULL OR u.uye_id = %s)
            AND (%s IS NULL OR k.kategori_id = %s)
            ORDER BY o.alis_tarihi
        """

        params = [
            self.date_bas.date().toPyDate(),
            self.date_bit.date().toPyDate(),
            self.cmb_uye.currentData(),
            self.cmb_uye.currentData(),
            self.cmb_kategori.currentData(),
            self.cmb_kategori.currentData()
        ]

        cur.execute(sql, params)
        self.tablo_doldur(cur.fetchall(),
                          ["Üye", "Kitap", "Kategori", "Alış", "Son Teslim", "Durum"])
        conn.close()

    def rapor_geciken(self):
        conn = get_connection(self.kullanici_id)
        cur = conn.cursor()

        cur.execute("""
            SELECT
                u.ad || ' ' || u.soyad,
                k.ad,
                o.alis_tarihi,
                o.son_teslim_tarihi,
                CURRENT_DATE - o.son_teslim_tarihi AS gecikme
            FROM odunc o
            JOIN uyeler u ON u.uye_id = o.uye_id
            JOIN kitaplar k ON k.kitap_id = o.kitap_id
            WHERE o.iade_tarihi IS NULL
            AND o.son_teslim_tarihi < CURRENT_DATE
            ORDER BY gecikme DESC
        """)

        self.tablo_doldur(
            cur.fetchall(),
            ["Üye", "Kitap", "Alış", "Son Teslim", "Gecikme (Gün)"]
        )
        conn.close()

    def rapor_populer(self):
        conn = get_connection(self.kullanici_id)
        cur = conn.cursor()

        cur.execute("""
            SELECT
                k.ad,
                COUNT(o.odunc_id)
            FROM odunc o
            JOIN kitaplar k ON k.kitap_id = o.kitap_id
            WHERE o.alis_tarihi BETWEEN %s AND %s
            GROUP BY k.ad
            ORDER BY COUNT(o.odunc_id) DESC
        """, (
            self.date_bas.date().toPyDate(),
            self.date_bit.date().toPyDate()
        ))

        self.tablo_doldur(
            cur.fetchall(),
            ["Kitap", "Ödünç Sayısı"]
        )
        conn.close()

    def tablo_doldur(self, rows, headers):
        self.table.clear()
        self.table.setRowCount(len(rows))
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)

        for i, row in enumerate(rows):
            for j, val in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(val)))