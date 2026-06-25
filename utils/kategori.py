from itertools import combinations

# KATEGORI DASAR — dipakai untuk produk (Kelola Produk)
KATEGORI_DASAR = ["Makanan", "Minuman", "Snack", "Lainnya"]

def _semua_kombinasi_kategori() -> list[str]:
    hasil = list(KATEGORI_DASAR) 
    for jumlah in range(2, len(KATEGORI_DASAR) + 1):
        for kombinasi in combinations(KATEGORI_DASAR, jumlah):
            hasil.append(" & ".join(kombinasi))
    return hasil

# Daftar lengkap 15 kategori transaksi (dasar + semua kombinasi)
KATEGORI_TRANSAKSI = _semua_kombinasi_kategori()

def hitung_kategori_gabungan(daftar_kategori_item: list[str]) -> str:
    unik = set(daftar_kategori_item)
    if not unik:
        return "Lainnya"

    # Urutkan sesuai urutan KATEGORI_DASAR, abaikan kategori tak dikenal
    terurut = [k for k in KATEGORI_DASAR if k in unik]

    return " & ".join(terurut) if terurut else "Lainnya"