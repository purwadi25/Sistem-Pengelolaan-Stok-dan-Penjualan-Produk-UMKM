import sqlite3
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH  = os.path.join(BASE_DIR, "database", "umkm.db")

#KONEKSI
def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

#INISIALISASI
def init_db() -> None:
    with get_connection() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS produk (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                nama        TEXT    NOT NULL,
                kategori    TEXT    NOT NULL DEFAULT 'Lainnya',
                harga       INTEGER NOT NULL DEFAULT 0,
                modal       INTEGER NOT NULL DEFAULT 0,
                stok        INTEGER NOT NULL DEFAULT 0,
                satuan      TEXT    NOT NULL DEFAULT 'pcs',
                dibuat_pada TEXT    NOT NULL DEFAULT (datetime('now','localtime')),
                diubah_pada TEXT    NOT NULL DEFAULT (datetime('now','localtime'))
            );

            CREATE TABLE IF NOT EXISTS penjualan (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                no_transaksi TEXT   NOT NULL UNIQUE,
                tanggal     TEXT    NOT NULL,
                pelanggan   TEXT    NOT NULL DEFAULT 'Umum',
                kategori    TEXT    NOT NULL DEFAULT '-',
                total       INTEGER NOT NULL DEFAULT 0,
                keuntungan  INTEGER NOT NULL DEFAULT 0,
                status      TEXT    NOT NULL DEFAULT 'Selesai',
                dibuat_pada TEXT    NOT NULL DEFAULT (datetime('now','localtime'))
            );

            CREATE TABLE IF NOT EXISTS item_jual (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                penjualan_id    INTEGER NOT NULL REFERENCES penjualan(id) ON DELETE CASCADE,
                produk_id       INTEGER REFERENCES produk(id) ON DELETE SET NULL,
                nama_produk     TEXT    NOT NULL,
                harga_satuan    INTEGER NOT NULL DEFAULT 0,
                qty             INTEGER NOT NULL DEFAULT 1,
                subtotal        INTEGER NOT NULL DEFAULT 0
            );

            CREATE TABLE IF NOT EXISTS pengguna (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                username     TEXT    NOT NULL UNIQUE,
                password     TEXT    NOT NULL,
                nama_toko    TEXT    NOT NULL DEFAULT '',
                nama_pemilik TEXT    NOT NULL DEFAULT '',
                alamat       TEXT    NOT NULL DEFAULT '',
                telepon      TEXT    NOT NULL DEFAULT ''
            );

            CREATE TABLE IF NOT EXISTS pembelian_stok (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                produk_id    INTEGER REFERENCES produk(id) ON DELETE SET NULL,
                nama_produk  TEXT    NOT NULL,
                jenis        TEXT    NOT NULL DEFAULT 'Baru',
                stok_lama    INTEGER NOT NULL DEFAULT 0,
                jumlah_tambah INTEGER NOT NULL DEFAULT 0,
                stok_baru    INTEGER NOT NULL DEFAULT 0,
                harga_modal  INTEGER NOT NULL DEFAULT 0,
                total_modal  INTEGER NOT NULL DEFAULT 0,
                dibuat_pada  TEXT    NOT NULL DEFAULT (datetime('now','localtime'))
            );

            CREATE INDEX IF NOT EXISTS idx_pembelian_produk
                ON pembelian_stok(produk_id);

            CREATE INDEX IF NOT EXISTS idx_item_jual_penjualan
                ON item_jual(penjualan_id);
            CREATE INDEX IF NOT EXISTS idx_item_jual_produk
                ON item_jual(produk_id);
        """)
        
        # Buat akun default jika tabel pengguna masih kosong
        with get_connection() as conn:
            count = conn.execute("SELECT COUNT(*) FROM pengguna").fetchone()[0]
            if count == 0:
                import hashlib
                default_hash = hashlib.sha256("admin123".encode()).hexdigest()
                conn.execute(
                    """INSERT INTO pengguna (username, password, nama_toko,
                       nama_pemilik, alamat, telepon)
                       VALUES (?, ?, '', '', '', '')""",
                    ("admin", default_hash),
                )

# PRODUK - CRUD
def produk_get_all() -> list[dict]:
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM produk ORDER BY nama ASC"
        ).fetchall()
    return [dict(r) for r in rows]

def produk_get_by_id(produk_id: int) -> dict | None:
    with get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM produk WHERE id = ?", (produk_id,)
        ).fetchone()
    return dict(row) if row else None

def produk_insert(nama: str, kategori: str, harga: int, modal: int,stok: int, satuan: str) -> int:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with get_connection() as conn:
        cur = conn.execute(
            """INSERT INTO produk (nama, kategori, harga, modal, stok, satuan,
               dibuat_pada, diubah_pada)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (nama, kategori, harga, modal, stok, satuan, now, now),
        )
        produk_id = cur.lastrowid

        if stok > 0:
            conn.execute(
                """INSERT INTO pembelian_stok
                   (produk_id, nama_produk, jenis, stok_lama, jumlah_tambah,
                    stok_baru, harga_modal, total_modal, dibuat_pada)
                   VALUES (?, ?, 'Baru', 0, ?, ?, ?, ?, ?)""",
                (produk_id, nama, stok, stok, modal, modal * stok, now),
            )
    return produk_id

def produk_update(produk_id: int, nama: str, kategori: str, harga: int, modal: int, stok: int, satuan: str) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with get_connection() as conn:
        row_lama = conn.execute(
            "SELECT stok FROM produk WHERE id=?", (produk_id,)
        ).fetchone()
        stok_lama = row_lama["stok"] if row_lama else 0

        conn.execute(
            """UPDATE produk SET nama=?, kategori=?, harga=?, modal=?,
               stok=?, satuan=?, diubah_pada=? WHERE id=?""",
            (nama, kategori, harga, modal, stok, satuan, now, produk_id),
        )

        selisih = stok - stok_lama
        if selisih > 0:
            conn.execute(
                """INSERT INTO pembelian_stok
                   (produk_id, nama_produk, jenis, stok_lama, jumlah_tambah,
                    stok_baru, harga_modal, total_modal, dibuat_pada)
                   VALUES (?, ?, 'Restock', ?, ?, ?, ?, ?, ?)""",
                (produk_id, nama, stok_lama, selisih, stok, modal, modal * selisih, now),
            )

def produk_update_stok(produk_id: int, stok_baru: int) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with get_connection() as conn:
        conn.execute(
            "UPDATE produk SET stok=?, diubah_pada=? WHERE id=?",
            (stok_baru, now, produk_id),
        )

def produk_delete(produk_id: int) -> None:
    with get_connection() as conn:
        conn.execute("DELETE FROM produk WHERE id=?", (produk_id,))

def produk_search(keyword: str) -> list[dict]:
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM produk WHERE nama LIKE ? ORDER BY nama ASC",
            (f"%{keyword}%",),
        ).fetchall()
    return [dict(r) for r in rows]

# PEMBELIAN STOK — riwayat penambahan stok (produk baru & restock)
def pembelian_get_all() -> list[dict]:
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM pembelian_stok ORDER BY id DESC"
        ).fetchall()
    return [dict(r) for r in rows]

def pembelian_get_by_produk(produk_id: int) -> list[dict]:
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM pembelian_stok WHERE produk_id=? ORDER BY id DESC",
            (produk_id,),
        ).fetchall()
    return [dict(r) for r in rows]

# PENJUALAN — CRUD
def penjualan_get_all() -> list[dict]:
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM penjualan ORDER BY id DESC"
        ).fetchall()
        result = []
        for row in rows:
            t = dict(row)
            items = conn.execute(
                "SELECT * FROM item_jual WHERE penjualan_id=?", (t["id"],)
            ).fetchall()
            t["items"] = [dict(i) for i in items]
            result.append(t)
    return result

def penjualan_get_with_items(penjualan_id: int) -> dict | None:
    with get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM penjualan WHERE id=?", (penjualan_id,)
        ).fetchone()
        if not row:
            return None
        result = dict(row)
        items  = conn.execute(
            "SELECT * FROM item_jual WHERE penjualan_id=?", (penjualan_id,)
        ).fetchall()
        result["items"] = [dict(i) for i in items]
    return result

def penjualan_insert(no_transaksi: str, tanggal: str, pelanggan: str, kategori: str, total: int, keuntungan: int, status: str, items: list[dict]) -> int:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with get_connection() as conn:
        cur = conn.execute(
            """INSERT INTO penjualan
               (no_transaksi, tanggal, pelanggan, kategori,
                total, keuntungan, status, dibuat_pada)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (no_transaksi, tanggal, pelanggan, kategori,
             total, keuntungan, status, now),
        )
        penjualan_id = cur.lastrowid
        for item in items:
            conn.execute(
                """INSERT INTO item_jual
                   (penjualan_id, produk_id, nama_produk,
                    harga_satuan, qty, subtotal)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (penjualan_id,
                 item.get("produk_id"),
                 item["nama_produk"],
                 item["harga_satuan"],
                 item["qty"],
                 item["subtotal"]),
            )
    return penjualan_id

def penjualan_filter(tanggal_dari: str, tanggal_sampai: str, kategori: str = "") -> list[dict]:
    with get_connection() as conn:
        if kategori and kategori != "Semua Kategori":
            rows = conn.execute(
                """SELECT * FROM penjualan
                   WHERE tanggal BETWEEN ? AND ?
                   AND kategori = ?
                   ORDER BY id DESC""",
                (tanggal_dari, tanggal_sampai, kategori),
            ).fetchall()
        else:
            rows = conn.execute(
                """SELECT * FROM penjualan
                   WHERE tanggal BETWEEN ? AND ?
                   ORDER BY id DESC""",
                (tanggal_dari, tanggal_sampai),
            ).fetchall()
    return [dict(r) for r in rows]

def penjualan_get_items(penjualan_id: int) -> list[dict]:
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM item_jual WHERE penjualan_id=?", (penjualan_id,)
        ).fetchall()
    return [dict(r) for r in rows]

# PENGGUNA — autentikasi & info toko
def pengguna_get(username: str) -> dict | None:
    with get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM pengguna WHERE username=?", (username,)
        ).fetchone()
    return dict(row) if row else None

def pengguna_get_first() -> dict | None:
    with get_connection() as conn:
        row = conn.execute("SELECT * FROM pengguna LIMIT 1").fetchone()
    return dict(row) if row else None

def pengguna_update_akun(old_username: str, new_username: str, new_password_hash: str) -> None:
    with get_connection() as conn:
        conn.execute(
            "UPDATE pengguna SET username=?, password=? WHERE username=?",
            (new_username, new_password_hash, old_username),
        )

def pengguna_update_info_toko(username: str, nama_toko: str, nama_pemilik: str, alamat: str, telepon: str) -> None:
    with get_connection() as conn:
        conn.execute(
            """UPDATE pengguna SET nama_toko=?, nama_pemilik=?,
               alamat=?, telepon=? WHERE username=?""",
            (nama_toko, nama_pemilik, alamat, telepon, username),
        )