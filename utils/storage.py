def format_rupiah(angka: int) -> str:
    return f"Rp {angka:,}".replace(",", ".")