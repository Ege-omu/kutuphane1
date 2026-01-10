from db import get_connection

def kitap_teslim_al(odunc_id, kullanici_id):
    conn = get_connection(kullanici_id)
    cur = conn.cursor()

    try:
        cur.execute(
            "CALL sp_kitap_teslim_al(%s);",
            (odunc_id,)
        )
        conn.commit()
        return True, "Kitap teslim alındı"
    except Exception as e:
        conn.rollback()
        return False, str(e)
    finally:
        cur.close()
        conn.close()
