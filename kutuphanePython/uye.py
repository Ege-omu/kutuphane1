from db import get_connection


def uyeleri_getir(aranan=""):
    conn = get_connection()
    cur = conn.cursor()

    query = """
        SELECT uye_id, ad, soyad, email, telefon
        FROM uyeler
        WHERE ad ILIKE %s OR soyad ILIKE %s OR email ILIKE %s
        ORDER BY ad
    """
    like = f"%{aranan}%"
    cur.execute(query, (like, like, like))

    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def uye_ekle(ad, soyad, email, telefon):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO uyeler (ad, soyad, email, telefon)
        VALUES (%s, %s, %s, %s)
    """, (ad, soyad, email, telefon))

    conn.commit()
    cur.close()
    conn.close()


def uye_silinebilir_mi(uye_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT COUNT(*) FROM odunc
        WHERE uye_id = %s AND durum = 'Aktif'
    """, (uye_id,))

    count = cur.fetchone()[0]
    cur.close()
    conn.close()
    return count == 0

def uye_sil(uye_id):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "DELETE FROM uyeler WHERE uye_id = %s",
            (uye_id,)
        )
        conn.commit()
        return True, "Üye silindi"
    except Exception as e:
        conn.rollback()
        return False, str(e)
    finally:
        cur.close()
        conn.close()