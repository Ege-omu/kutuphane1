Create Table if Not Exists roller(
	rol_id Serial Primary Key,
	rol_adi Varchar(30) Unique Not NULL
);

Create Table if Not Exists kullanicilar(
	kullanici_id Serial Primary Key,
	kullanici_adi Varchar(50) Unique Not NULL,
	sifre Varchar(100) Not NULL,
	rol_id INT References roller(rol_id),
	aktif Bool Default True
);

Create Table if Not Exists uyeler(
	uye_id Serial Primary key,
	ad Varchar(50) Not Null,
	soyad Varchar(50) Not NULL,
	email Varchar(100) Not NULL,
	telefon Varchar(20) Not NULL,
	kayit_tarihi Date Default current_date,
	aktif Bool Default True
);

Create Table if Not Exists kategoriler(
	kategori_id Serial Primary key,
	kategori_adi Varchar(50) Unique Not NULL
);

Create Table if Not Exists kitaplar(
	kitap_id Serial Primary key,
	ad Varchar(100) Not NULL,
	yazar Varchar(100) Not NULL,
	kategori_id INT References kategoriler(kategori_id) ON Delete Set NULL,
	yayin_evi Varchar(100) Not NUll,
	basim_yili INT Not NUll,
	toplam_kopya INT Not NUll
	Check (toplam_kopya >= 0),
	mevcut_kopya INT Not NULL
	Check (mevcut_kopya >= 0 AND mevcut_kopya <= toplam_kopya)
);

Create Table if Not Exists odunc(
	odunc_id Serial Primary Key,
	uye_id INT Not NULL References uyeler(uye_id),
	kitap_id INT Not NULL References kitaplar(kitap_id),
	alis_tarihi DATE Default Current_Date,
	son_teslim_tarihi Date,
	iade_tarihi Date,
	Durum VARCHAR(20) Default 'Aktif' Check (Durum In ('Aktif', 'TeslimEdildi', 'Gecikmis'))
);

Create Table if Not Exists cezalar(
	ceza_id Serial Primary Key,
    odunc_id INT References odunc(odunc_id),
	uye_id INT References uyeler(uye_id),
    gecikme_gunu INT Not NULL Check(gecikme_gunu >= 0),
    tutar Numeric(6,2) Not NULL Check(tutar >= 0),
    odendi Bool Default False
);

Create Table if Not Exists Log_kayitlari(
	log_id Serial Primary Key,
	tablo_adi Varchar(50) Not NUll,
	islem_turu Varchar(20) Not NULL check(islem_turu In ('INSERT', 'UPDATE', 'DELETE')),
	islem_yapan_kullanici_id INT References kullanicilar(kullanici_id),
	aciklama Text,
	islem_tarihi Date Default Current_Date
); 


