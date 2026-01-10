from db import get_connection


def cezalari_getir():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            c.ceza_id,
            u.ad || ' ' || u.soyad AS uye,
            c.gecikme_gunu,
            c.tutar,
            c.odendi
        FROM cezalar c
        JOIN uyeler u ON c.uye_id = u.uye_id
        ORDER BY c.odendi, c.ceza_id DESC
    """)

    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def ceza_odendi_yap(ceza_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE cezalar
        SET odendi = TRUE
        WHERE ceza_id = %s
    """, (ceza_id,))
    conn.commit()
    cur.close()
    conn.close()
