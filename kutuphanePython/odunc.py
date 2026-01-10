from db import get_connection


def kitap_odunc_ver(uye_id, kitap_id, kullanici_id):
    """
    sp_kitap_odunc_ver prosedürünü çağırır
    """
    conn = get_connection(kullanici_id)
    cur = conn.cursor()

    try:
        cur.execute(
            "CALL sp_kitap_odunc_ver(%s, %s);",
            (uye_id, kitap_id)
        )
        conn.commit()
        return True, "Kitap başarıyla ödünç verildi"

    except Exception as e:
        conn.rollback()
        return False, str(e)

    finally:
        cur.close()
        conn.close()


def kitap_teslim_al(odunc_id, kullanici_id):
    """
    sp_kitap_teslim_al prosedürünü çağırır
    """
    conn = get_connection(kullanici_id)
    cur = conn.cursor()

    try:
        cur.execute(
            "CALL sp_kitap_teslim_al(%s);",
            (odunc_id,)
        )
        conn.commit()
        return True, "Kitap başarıyla teslim alındı"

    except Exception as e:
        conn.rollback()
        return False, str(e)

    finally:
        cur.close()
        conn.close()
