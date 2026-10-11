"""processing.py - perhitungan dan analisis data lagu."""
from .validasi import ValidasiError


def hitung_total_durasi(*durasi):
    """*args: menerima sejumlah durasi (detik) dan menjumlahkannya."""
    # assert: durasi tidak boleh negatif (kesalahan program jika terjadi)
    assert all(d >= 0 for d in durasi), "Durasi tidak boleh negatif"
    return sum(durasi)


def total_durasi_playlist(daftar):
    """Total durasi seluruh lagu (detik)."""
    return hitung_total_durasi(*[lagu.durasi_detik for lagu in daftar])


def format_durasi(detik):
    """Ubah detik menjadi 'jam:menit:detik' atau 'menit:detik'."""
    menit, sisa = divmod(int(detik), 60)
    jam, menit = divmod(menit, 60)
    if jam:
        return f"{jam}:{menit:02d}:{sisa:02d}"
    return f"{menit}:{sisa:02d}"


def rata_rata_durasi(daftar):
    """Rata-rata durasi lagu (detik); 0 jika daftar kosong."""
    if not daftar:
        return 0.0
    return total_durasi_playlist(daftar) / len(daftar)


def lagu_terpanjang(daftar):
    """Lagu dengan durasi terbesar (lambda sebagai key)."""
    return max(daftar, key=lambda l: l.durasi_detik) if daftar else None


def lagu_terpendek(daftar):
    """Lagu dengan durasi terkecil (lambda sebagai key)."""
    return min(daftar, key=lambda l: l.durasi_detik) if daftar else None


def urutkan_lagu(daftar, berdasarkan="judul", terbalik=False):
    """Urutkan lagu berdasarkan judul/artis/tahun/durasi."""
    # Tiap kunci pengurutan berupa lambda
    kunci = {
        "judul": lambda l: l.judul.lower(),
        "artis": lambda l: (l.artis.lower(), l.tahun),
        "tahun": lambda l: l.tahun,
        "durasi": lambda l: l.durasi_detik,
    }
    if berdasarkan not in kunci:
        raise ValidasiError(f"Urutan '{berdasarkan}' tidak dikenal. "
                            f"Pilih: {', '.join(kunci)}")
    return sorted(daftar, key=kunci[berdasarkan], reverse=terbalik)


def filter_artis(daftar, artis):
    """Ambil lagu milik satu artis (filter + lambda)."""
    return list(filter(lambda l: l.artis.lower() == artis.strip().lower(),
                       daftar))


def hitung_per_artis(daftar):
    """Hitung jumlah lagu dan total durasi tiap artis -> dict."""
    hasil = {}
    for lagu in daftar:
        data = hasil.setdefault(lagu.artis, {"jumlah": 0, "durasi": 0})
        data["jumlah"] += 1
        data["durasi"] += lagu.durasi_detik
    return hasil


def buat_laporan(daftar, nama_playlist):
    """Susun teks laporan statistik playlist."""
    baris = [f"LAPORAN PLAYLIST: {nama_playlist}", "=" * 50,
             f"Jumlah lagu     : {len(daftar)}",
             f"Total durasi    : {format_durasi(total_durasi_playlist(daftar))}",
             f"Rata-rata durasi: {format_durasi(rata_rata_durasi(daftar))}"]
    panjang, pendek = lagu_terpanjang(daftar), lagu_terpendek(daftar)
    if panjang:
        baris.append(f"Terpanjang      : {panjang.judul} ({panjang.durasi_format()})")
        baris.append(f"Terpendek       : {pendek.judul} ({pendek.durasi_format()})")
    baris += ["", "Per artis:"]
    for artis, data in hitung_per_artis(daftar).items():
        baris.append(f"- {artis}: {data['jumlah']} lagu, "
                     f"{format_durasi(data['durasi'])}")
    baris += ["", "Daftar lagu (urut tahun):"]
    for i, lagu in enumerate(urutkan_lagu(daftar, berdasarkan="tahun"), 1):
        baris.append(f"{i:2d}. {lagu}")
    return "\n".join(baris) + "\n"