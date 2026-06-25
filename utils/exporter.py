import csv
import os
from datetime import datetime

from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units     import mm
from reportlab.lib.styles    import getSampleStyleSheet
from reportlab.lib            import colors
from reportlab.platypus       import (
    SimpleDocTemplate, Table, TableStyle,
    Paragraph, Spacer,
)

# HELPER
def _fmt_rp(angka: int) -> str:
    return f"Rp {angka:,}".replace(",", ".")

def _default_path(suffix: str, ext: str) -> str:
    for folder in ["~/Downloads", "~/Desktop", "~"]:
        expanded = os.path.expanduser(folder)
        if os.path.isdir(expanded):
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            return os.path.join(expanded, f"UMKM_{suffix}_{ts}.{ext}")
    return os.path.expanduser(f"~/UMKM_{suffix}.{ext}")

# EXPORT DATA PRODUK KE FORMAT CSV
def export_produk_csv(data_produk: list, filepath: str | None = None) -> str:
    path = filepath or _default_path("Produk", "csv")
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["No", "Nama Produk", "Kategori",
                         "Harga (Rp)", "Modal (Rp)", "Stok", "Satuan"])
        for i, p in enumerate(data_produk, 1):
            writer.writerow([
                i,
                p.get("nama", ""),
                p.get("kategori", ""),
                p.get("harga", 0),
                p.get("modal", 0),
                p.get("stok", 0),
                p.get("satuan", ""),
            ])
    return path

# EXPORT DATA PENJUALAN KE FORMAT CSV
def export_penjualan_csv(data_penjualan: list, filepath: str | None = None, dari: str = "", sampai: str = "", kategori: str = "") -> str:
    path = filepath or _default_path("Penjualan", "csv")
    rows = _apply_filter(data_penjualan, dari, sampai, kategori)
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["No Transaksi", "Tanggal", "Kategori",
                         "Pelanggan", "Total (Rp)", "Keuntungan (Rp)", "Status"])
        for t in rows:
            writer.writerow([
                t.get("no_transaksi") or t.get("transaksi", ""),
                t.get("tanggal", ""),
                t.get("kategori", ""),
                t.get("pelanggan", ""),
                t.get("total", 0),
                t.get("keuntungan", 0),
                t.get("status", ""),
            ])
    return path

# EXPORT DATA PRODUK KE FORMAT PDF
def export_produk_pdf(data_produk: list, filepath: str | None = None, nama_toko: str = "UMKM Stock") -> str:
    path   = filepath or _default_path("Produk", "pdf")
    doc    = SimpleDocTemplate(
        path,
        pagesize   = A4,
        leftMargin = 15*mm, rightMargin  = 15*mm,
        topMargin  = 15*mm, bottomMargin = 15*mm,
    )
    styles = getSampleStyleSheet()
    story  = []

    story.append(Paragraph(f"<b>Daftar Produk — {nama_toko}</b>", styles["Title"]))
    story.append(Paragraph(
        f"Dicetak: {datetime.now().strftime('%d %B %Y %H:%M')}   |   "
        f"Total Produk: {len(data_produk)}",
        styles["Normal"],
    ))
    story.append(Spacer(1, 8*mm))

    header = ["No", "Nama Produk", "Kategori", "Harga", "Modal", "Stok", "Satuan"]
    table_data = [header]
    for i, p in enumerate(data_produk, 1):
        table_data.append([
            str(i),
            p.get("nama", ""),
            p.get("kategori", ""),
            _fmt_rp(p.get("harga", 0)),
            _fmt_rp(p.get("modal", 0)),
            str(p.get("stok", 0)),
            p.get("satuan", ""),
        ])

    tbl = Table(table_data, repeatRows=1)
    tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, 0),  colors.HexColor("#0f766e")),
        ("TEXTCOLOR",     (0, 0), (-1, 0),  colors.white),
        ("FONTNAME",      (0, 0), (-1, 0),  "Helvetica-Bold"),
        ("FONTSIZE",      (0, 0), (-1, -1), 9),
        ("GRID",          (0, 0), (-1, -1), 0.4, colors.HexColor("#d1d5db")),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.white, colors.HexColor("#f0fdfa")]),
        ("ALIGN",         (5, 1), (5, -1),  "CENTER"),
    ]))
    story.append(tbl)
    doc.build(story)
    return path

# EXPORT DATA PENJUALAN KE FORMAT PDF
def export_laporan_pdf(data_penjualan: list, filepath: str | None = None, dari: str = "", sampai: str = "", kategori: str = "", nama_toko: str = "UMKM Stock") -> str:
    path = filepath or _default_path("Laporan", "pdf")
    rows = _apply_filter(data_penjualan, dari, sampai, kategori)

    doc  = SimpleDocTemplate(
        path,
        pagesize   = landscape(A4),
        leftMargin = 15*mm, rightMargin  = 15*mm,
        topMargin  = 15*mm, bottomMargin = 15*mm,
    )
    styles  = getSampleStyleSheet()
    story   = []

    # Header
    story.append(Paragraph(
        f"<b>Laporan Penjualan — {nama_toko}</b>",
        styles["Title"],
    ))
    period = f"{dari} s/d {sampai}" if dari or sampai else "Semua Periode"
    kat_str = f" | Kategori: {kategori}" if kategori and kategori != "Semua Kategori" else ""
    story.append(Paragraph(
        f"Periode: {period}{kat_str}   |   "
        f"Dicetak: {datetime.now().strftime('%d %B %Y %H:%M')}",
        styles["Normal"],
    ))
    story.append(Spacer(1, 8*mm))

    # Tabel data
    header = ["No Transaksi", "Tanggal", "Kategori", "Pelanggan",
              "Total", "Keuntungan", "Status"]
    table_data = [header]
    total_pendapatan = 0
    total_keuntungan = 0
    for t in rows:
        total_val   = t.get("total", 0)
        untung_val  = t.get("keuntungan", 0)
        total_pendapatan += total_val
        total_keuntungan += untung_val
        table_data.append([
            t.get("no_transaksi") or t.get("transaksi", ""),
            t.get("tanggal", ""),
            t.get("kategori", ""),
            t.get("pelanggan", ""),
            _fmt_rp(total_val),
            _fmt_rp(untung_val),
            t.get("status", ""),
        ])

    # Baris total
    table_data.append([
        "TOTAL", "", "", "",
        _fmt_rp(total_pendapatan),
        _fmt_rp(total_keuntungan),
        f"{len(rows)} transaksi",
    ])

    tbl = Table(table_data, repeatRows=1)
    tbl.setStyle(TableStyle([
        # Header
        ("BACKGROUND",   (0, 0), (-1, 0),  colors.HexColor("#0f766e")),
        ("TEXTCOLOR",    (0, 0), (-1, 0),  colors.white),
        ("FONTNAME",     (0, 0), (-1, 0),  "Helvetica-Bold"),
        ("FONTSIZE",     (0, 0), (-1, 0),  9),
        ("BOTTOMPADDING",(0, 0), (-1, 0),  6),
        ("TOPPADDING",   (0, 0), (-1, 0),  6),
        # Body
        ("FONTSIZE",     (0, 1), (-1, -2), 8),
        ("ROWBACKGROUNDS",(0,1),(-1,-2),[colors.white, colors.HexColor("#f0fdfa")]),
        ("GRID",         (0, 0), (-1, -1), 0.4, colors.HexColor("#d1d5db")),
        ("ALIGN",        (4, 1), (5, -1),  "RIGHT"),
        ("ALIGN",        (0, 0), (-1, 0),  "CENTER"),
        # Baris total
        ("BACKGROUND",  (0, -1), (-1, -1), colors.HexColor("#f3f4f6")),
        ("FONTNAME",    (0, -1), (-1, -1), "Helvetica-Bold"),
        ("FONTSIZE",    (0, -1), (-1, -1), 9),
    ]))
    story.append(tbl)
    story.append(Spacer(1, 6*mm))

    # Ringkasan
    story.append(Paragraph(
        f"<b>Total Pendapatan: {_fmt_rp(total_pendapatan)}</b>   |   "
        f"<b>Total Keuntungan: {_fmt_rp(total_keuntungan)}</b>   |   "
        f"<b>Jumlah Transaksi: {len(rows)}</b>",
        styles["Normal"],
    ))

    doc.build(story)
    return path

# HELPER FILTER
def _apply_filter(data: list, dari: str, sampai: str, kategori: str) -> list:
    result = []
    for t in data:
        tgl = t.get("tanggal", "")

        # Filter tanggal (format ISO yyyy-MM-dd atau dd MMMM yyyy)
        if dari or sampai:
            # Normalkan ke ISO jika perlu
            tgl_iso = _to_iso(tgl)
            if dari   and tgl_iso < dari:   continue
            if sampai and tgl_iso > sampai: continue

        # Filter kategori
        if kategori and kategori not in ("Semua Kategori", ""):
            if t.get("kategori", "") != kategori:
                continue

        result.append(t)
    return result

def _to_iso(tgl_str: str) -> str:
    # Sudah ISO
    if len(tgl_str) == 10 and tgl_str[4] == "-":
        return tgl_str
    # Format "dd MMMM yyyy" (PySide6 lokal Indonesia)
    try:
        from PySide6.QtCore import QDate
        d = QDate.fromString(tgl_str, "dd MMMM yyyy")
        if d.isValid():
            return d.toString("yyyy-MM-dd")
    except Exception:
        pass
    return tgl_str