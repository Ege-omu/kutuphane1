Create OR Replace Procedure sp_kitap_odunc_ver(
	p_uye_id INT,
	p_kitap_id INT
)

Language plpgsql
As $$
	Declare
		v_mevcut INT;
	Begin
		if NOT exists (
			Select 1 From uyeler
			Where uye_id = p_uye_id AND aktif = True
		) Then
			Raise Exception 'Üye Aktif Değil';
		End if;
	
		Select mevcut_kopya Into v_mevcut From kitaplar
		Where kitap_id = p_kitap_id;
	
		if v_mevcut is NULL OR v_mevcut <= 0 Then
			Raise Exception 'Kitap Stokta Yok';
		End if;

		if Exists(
			Select 1 From odunc
			Where uye_id = p_uye_id
			AND kitap_id = p_kitap_id
			AND durum = 'Aktif'
		) Then
			Raise Exception 'Bu kitap zaten ödünç alınmış';
		End if;
		
		Insert Into odunc(uye_id, kitap_id, son_teslim_tarihi)
		Values(p_uye_id, p_kitap_id, Current_Date + Interval '14 day');
	End;
$$;

Create OR Replace Procedure sp_kitap_teslim_al(
	p_odunc_id INT
)

Language plpgsql
As $$
	Declare
		v_son_teslim Date;
		v_iade_tarihi Date:= Current_Date;
		v_uye_id INT;
		v_gecikme INT;

	Begin
		Select son_teslim_tarihi, uye_id Into v_son_teslim, v_uye_id From odunc
		Where odunc_id = p_odunc_id;

		if Exists(
			Select 1 From odunc
			Where odunc_id = p_odunc_id
			AND iade_tarihi Is Not NULL
		) Then
			Raise Exception 'Bu ödünç zaten teslim alınmış';
		End if;

		if v_son_teslim is NULL Then
			Raise Exception 'Ödünç Kaydı Bulunamadı';
		End if;

		Update odunc
			Set iade_tarihi = v_iade_tarihi,
			durum = Case
						When v_iade_tarihi > v_son_teslim Then 'Gecikmis'
						Else 'TeslimEdildi'
					End
			Where odunc_id = p_odunc_id;

			v_gecikme:= Greatest(0,v_iade_tarihi - v_son_teslim);

			if v_gecikme > 0 Then
				Insert Into cezalar(odunc_id, uye_id, gecikme_gunu, tutar)
				Values(p_odunc_id, v_uye_id, v_gecikme, v_gecikme * 2);
			End if;

	
	End;
$$;
