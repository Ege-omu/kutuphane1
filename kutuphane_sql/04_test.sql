Insert Into roller (rol_adi)
Values	('Admin'),
		('Personel');

Insert Into kullanicilar (kullanici_adi, sifre, rol_id)
Values 	('admin', '1234', 1),
		('personel', '1234', 2);

Insert Into uyeler (ad, soyad, email, telefon)
Values
('Egemen', 'Sarac', '23060542@stu.omu.edu.tr', '5541469034'),
('Murat Yasar', 'Sayan', '23060540@stu.omu.edu.tr', '5541506070'),
('Ali', 'Yılmaz', '23060123', '5551355040');

Insert Into kategoriler (kategori_adi)
Values 
('Roman'),
('Bilim'),
('Tarih');

INSERT INTO kitaplar (
    ad, yazar, kategori_id, yayin_evi,
    basim_yili, toplam_kopya, mevcut_kopya
)
VALUES
('Suç ve Ceza', 'Dostoyevski', 1, 'İş Bankası', 2019, 5, 5),
('Sapiens', 'Yuval Noah Harari', 2, 'Kolektif', 2020, 3, 3),
('Nutuk', 'Mustafa Kemal Atatürk', 3, 'Türk Tarih Kurumu', 2018, 4, 4),
('Sefiller', 'viktor hugo', 1, 'Kolektif', 2016, 2, 2);


-- SELECT * FROM odunc;
-- SELECT * FROM cezalar;
-- SELECT * FROM log_kayitlari;
-- SELECT * FROM kitaplar;
-- SELECT * FROM kullanicilar;
-- SELECT * FROM uyeler;

-- TRUNCATE TABLE
--     log_kayitlari,
--     cezalar,
--     odunc,
--     kitaplar,
--     kategoriler,
--     uyeler,
--     kullanicilar,
--     roller
-- RESTART IDENTITY CASCADE;

