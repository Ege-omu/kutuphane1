from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel
from odunc_window import OduncWindow
from teslim_window import TeslimWindow
from raporlar_window import RaporWindow
from dinamik_rapor_window import DinamikRaporWindow
from uye_window import UyeWindow
from kitap_window import KitapWindow
from ceza_window import CezaWindow

class MainWindow(QWidget):
    def __init__(self, kullanici_id, rol_id, kullanici_adi):
        super().__init__()
        self.kullanici_id = kullanici_id
        self.rol_id = rol_id
        self.kullanici_adi = kullanici_adi

        self.setWindowTitle("Kütüphane Sistemi")
        self.setFixedSize(400, 450)

        self.init_ui()

    def init_ui(self):
        lbl_greet= QLabel(f"Hoş geldiniz, {self.kullanici_adi}")


        btn_uye = QPushButton("Üye Yönetimi")
        btn_uye.clicked.connect(self.open_uye)

        btn_kitap = QPushButton("Kitap Yönetimi")
        btn_kitap.clicked.connect(self.open_kitap)

        btn_odunc = QPushButton("Kitap Ödünç Ver")
        btn_odunc.clicked.connect(self.open_odunc)

        btn_teslim = QPushButton("Kitap Teslim Al")
        btn_teslim.clicked.connect(self.open_teslim)

        btn_ceza = QPushButton("Ceza Görüntüle")
        btn_ceza.clicked.connect(self.open_ceza)

        btn_rapor = QPushButton("Raporlar")
        btn_rapor.clicked.connect(self.open_rapor)

        btn_dinamik = QPushButton("Dinamik Sorgu")
        btn_dinamik.clicked.connect(self.open_dinamik)

        btn_cikis = QPushButton("Çıkış")
        btn_cikis.clicked.connect(self.close)


        if self.rol_id != 1:
            btn_rapor.hide()
            btn_dinamik.hide()

        layout = QVBoxLayout()
        
        layout.addWidget(lbl_greet)
        layout.addWidget(btn_uye)
        layout.addWidget(btn_kitap)
        layout.addWidget(btn_odunc)
        layout.addWidget(btn_teslim)
        layout.addWidget(btn_ceza)
        layout.addWidget(btn_rapor)
        layout.addWidget(btn_dinamik)
        layout.addWidget(btn_cikis)

        self.setLayout(layout)

    def open_uye(self):
        self.uye_window = UyeWindow()
        self.uye_window.show()

    def open_kitap(self):
        self.kitap_window = KitapWindow()
        self.kitap_window.show()

    def open_odunc(self):
        self.odunc_window = OduncWindow(self.kullanici_id)
        self.odunc_window.show()

    def open_teslim(self):
        self.teslim_window = TeslimWindow(self.kullanici_id)
        self.teslim_window.show()
    
    def open_ceza(self):
        self.ceza_window = CezaWindow(self.kullanici_id)
        self.ceza_window.show()

    def open_rapor(self):
        self.rapor_window = RaporWindow(self.kullanici_id)
        self.rapor_window.show()

    def open_dinamik(self):
        self.dinamik_window = DinamikRaporWindow(self.kullanici_id)
        self.dinamik_window.show()