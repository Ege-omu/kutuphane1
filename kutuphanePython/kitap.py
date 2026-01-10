from db import get_connection


def kitaplari_listele(aranan=""):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            k.kitap_id,
            k.ad,
            k.yazar,
            COALESCE(ka.kategori_adi, ''),
            k.yayin_evi,
            k.basim_yili,
            k.mevcut_kopya
        FROM kitaplar k
        LEFT JOIN kategoriler ka
            ON k.kategori_id = ka.kategori_id
        WHERE k.ad ILIKE %s
           OR k.yazar ILIKE %s
        ORDER BY k.ad
    """, (f"%{aranan}%", f"%{aranan}%"))

    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def kategorileri_listele():
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


def kitap_ekle(ad, yazar, kategori_id, yayin_evi, basim_yili, toplam_kopya):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO kitaplar (
            ad,
            yazar,
            kategori_id,
            yayin_evi,
            basim_yili,
            toplam_kopya,
            mevcut_kopya
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        ad,
        yazar,
        kategori_id,
        yayin_evi,
        basim_yili,
        toplam_kopya,
        toplam_kopya
    ))

    conn.commit()
    cur.close()
    conn.close()


def kitap_silinebilir_mi(kitap_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT COUNT(*)
        FROM odunc
        WHERE kitap_id = %s
          AND durum = 'Aktif'
    """, (kitap_id,))

    aktif_sayi = cur.fetchone()[0]
    cur.close()
    conn.close()
    return aktif_sayi == 0


def kitap_sil(kitap_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        DELETE FROM kitaplar
        WHERE kitap_id = %s
    """, (kitap_id,))

    conn.commit()
    cur.close()
    conn.close()
