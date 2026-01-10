from db import get_connection


def rapor_oduncte_olanlar():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT o.odunc_id,
               u.ad || ' ' || u.soyad AS uye,
               k.ad AS kitap,
               o.alis_tarihi,
               o.son_teslim_tarihi
        FROM odunc o
        JOIN uyeler u ON o.uye_id = u.uye_id
        JOIN kitaplar k ON o.kitap_id = k.kitap_id
        WHERE o.durum = 'Aktif'
        ORDER BY o.son_teslim_tarihi
    """)

    rows = cur.fetchall()
    cols = [desc[0] for desc in cur.description]

    cur.close()
    conn.close()
    return cols, rows


def rapor_gecikmeler():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT u.ad || ' ' || u.soyad AS uye,
               k.ad AS kitap,
               c.gecikme_gunu,
               c.tutar
        FROM cezalar c
        JOIN uyeler u ON c.uye_id = u.uye_id
        JOIN odunc o ON c.odunc_id = o.odunc_id
        JOIN kitaplar k ON o.kitap_id = k.kitap_id
        WHERE c.odendi = FALSE
        ORDER BY c.tutar DESC
    """)

    rows = cur.fetchall()
    cols = [desc[0] for desc in cur.description]

    cur.close()
    conn.close()
    return cols, rows


def rapor_en_cok_odunc():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT k.ad AS kitap,
               COUNT(*) AS odunc_sayisi
        FROM odunc o
        JOIN kitaplar k ON o.kitap_id = k.kitap_id
        GROUP BY k.ad
        ORDER BY odunc_sayisi DESC
    """)

    rows = cur.fetchall()
    cols = [desc[0] for desc in cur.description]

    cur.close()
    conn.close()
    return cols, rows
