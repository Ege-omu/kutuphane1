from db import get_connection


def kategori_ekle(kategori_adi):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO kategoriler (kategori_adi)
        VALUES (%s)
        ON CONFLICT (kategori_adi) DO NOTHING
    """, (kategori_adi,))

    conn.commit()
    cur.close()
    conn.close()


def kategorileri_getir():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT kategori_id, kategori_adi
        FROM kategoriler
        ORDER BY kategori_adi
    """)

    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows
