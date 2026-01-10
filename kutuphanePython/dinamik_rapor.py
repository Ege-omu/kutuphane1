from db import get_connection


def odunc_dinamik_ara(durum=None):
    conn = get_connection()
    cur = conn.cursor()

    query = """
        SELECT
            o.odunc_id,
            u.ad || ' ' || u.soyad AS uye,
            k.ad AS kitap,
            o.alis_tarihi,
            o.son_teslim_tarihi,
            o.durum
        FROM odunc o
        JOIN uyeler u ON o.uye_id = u.uye_id
        JOIN kitaplar k ON o.kitap_id = k.kitap_id
    """

    params = []

    if durum and durum != "Hepsi":
        query += " WHERE o.durum = %s"
        params.append(durum)

    query += " ORDER BY o.alis_tarihi DESC"

    cur.execute(query, params)

    rows = cur.fetchall()
    cols = [desc[0] for desc in cur.description]

    cur.close()
    conn.close()
    return cols, rows