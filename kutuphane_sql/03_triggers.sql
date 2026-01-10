Create OR Replace Function fn_log_kayit()
Returns Trigger
Language plpgsql
AS $$
Begin
	Insert Into log_kayitlari(
		tablo_adi,
		islem_turu,
		islem_yapan_kullanici_id,
		aciklama
	)
	Values(
		TG_TABLE_NAME,
		Tg_OP,
		current_setting('application.user_id', true)::INT,
		'Otomatik Log Kaydı'
	);

	Return Coalesce(New, Old);
End;
$$;

Create OR Replace Function fn_tr_uye_delete_block()
RETURNS Trigger
Language plpgsql
AS $$
BEGIN
    IF Exists (
        Select 1
        From odunc
        Where uye_id = OLD.uye_id
          AND durum = 'Aktif'
    ) Then
        Raise Exception
        'Bu üyenin aktif ödünç kaydı var, silinemez.';
    END If;

    IF EXISTS (
        SELECT 1
        FROM cezalar
        WHERE uye_id = OLD.uye_id
          AND odendi = FALSE
    ) THEN
        RAISE EXCEPTION
        'Bu üyenin ödenmemiş cezası var, silinemez.';
    END IF;

    RETURN OLD;
END;
$$;

CREATE OR REPLACE FUNCTION fn_tr_odunc_insert()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE kitaplar
    SET mevcut_kopya = mevcut_kopya - 1
    WHERE kitap_id = NEW.kitap_id;

    Insert Into log_kayitlari (
        tablo_adi,
        islem_turu,
        islem_yapan_kullanici_id,
        aciklama
    )
    Values (
        'odunc',
        'INSERT',
        current_setting('application.user_id', true)::INT,
        'ODUNC tablosuna yeni kayıt eklendi'
    );

    RETURN NEW;
END;
$$;

Create OR Replace Function fn_tr_odunc_update_teslim()
RETURNS Trigger
LANGUAGE plpgsql
AS $$
BEGIN
    IF OLD.iade_tarihi IS NULL AND NEW.iade_tarihi IS NOT NULL THEN

        Update kitaplar
        Set mevcut_kopya = mevcut_kopya + 1
        Where kitap_id = NEW.kitap_id;

        Insert Into log_kayitlari (
            tablo_adi,
            islem_turu,
            islem_yapan_kullanici_id,
            aciklama
        )
        Values (
            'odunc',
            'UPDATE',
            current_setting('application.user_id', true)::INT,
            'Ödünç teslim alındı, kitap stoğu artırıldı'
        );
    END IF;

    RETURN NEW;
END;
$$;


Create Trigger trg_log_odunc
After Insert OR Update OR Delete
on odunc
For Each Row
Execute Function fn_log_kayit();

Create Trigger trg_log_kitaplar
After Update
on kitaplar
For Each Row
Execute Function fn_log_kayit();

Create Trigger trg_log_cezalar
After Insert
on cezalar
For Each Row
Execute Function fn_log_kayit();

Create Trigger tr_uye_delete_block
Before Delete ON uyeler
FOR EACH ROW
Execute Function fn_tr_uye_delete_block();

Create Trigger tr_odunc_insert
After Insert ON odunc
FOR EACH ROW
Execute Function fn_tr_odunc_insert();

Create Trigger tr_odunc_update_teslim
After Update ON odunc
FOR EACH ROW
Execute Function fn_tr_odunc_update_teslim();

