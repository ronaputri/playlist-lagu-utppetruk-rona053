"""versi_awal.py - versi SEBELUM refactoring (untuk kolom "Sebelum" di tabel).

Jalankan dari folder playlist_lagu:  python versi_awal.py
Bagian bawah file membandingkan hasilnya dengan kode final di package playlist.
"""
import os
import tempfile


class ValidasiError(Exception):
    pass


# 
# 1. SEBELUM: validasi ditulis berulang di dalam __init__
#    (sesudah: validasi_teks(), validasi_angka_positif(), validasi_tahun())
# 
class LaguAwal:
    def __init__(self, judul, artis, tahun, durasi_detik, **kwargs):
        if str(judul).strip() == "":
            raise ValidasiError("Field 'judul' tidak boleh kosong")
        if ";" in str(judul):
            raise ValidasiError("Field 'judul' tidak boleh berisi ';'")
        if str(artis).strip() == "":
            raise ValidasiError("Field 'artis' tidak boleh kosong")
        if ";" in str(artis):
            raise ValidasiError("Field 'artis' tidak boleh berisi ';'")
        if int(tahun) < 1900 or int(tahun) > 2100:
            raise ValidasiError("Tahun di luar rentang 1900-2100")
        if int(durasi_detik) <= 0:
            raise ValidasiError("Field 'durasi' harus lebih dari 0")
        self.judul = str(judul).strip()
        self.artis = str(artis).strip()
        self.tahun = int(tahun)
        self.durasi_detik = int(durasi_detik)
        self.atribut_tambahan = kwargs


# 
# 2. SEBELUM: rantai if/elif, sorted() ditulis berulang
#    (sesudah: dictionary berisi lambda + satu baris sorted)
# 

def urutkan_lagu_awal(daftar, berdasarkan="judul", terbalik=False):
    if berdasarkan == "judul":
        return sorted(daftar, key=lambda l: l.judul.lower(), reverse=terbalik)
    elif berdasarkan == "artis":
        return sorted(daftar, key=lambda l: (l.artis.lower(), l.tahun),
                      reverse=terbalik)
    elif berdasarkan == "tahun":
        return sorted(daftar, key=lambda l: l.tahun, reverse=terbalik)
    elif berdasarkan == "durasi":
        return sorted(daftar, key=lambda l: l.durasi_detik, reverse=terbalik)
    else:
        raise ValidasiError("Urutan tidak dikenal")


# 
# 3. SEBELUM: parsing baris file ditulis langsung di dalam loop baca file
#    (sesudah: dipindah ke Lagu.dari_baris() di models.py)
# 
def baca_lagu_awal(path):
    hasil = []
    rusak = 0
    with open(path, "r", encoding="utf-8") as file:
        for baris in file:
            if not baris.strip():
                continue
            try:
                b = baris.strip().split(";")
                if len(b) != 5:
                    raise ValueError("Jumlah kolom salah")
                atribut = {}
                for p in b[4].split(","):
                    if "=" in p:
                        k, _, v = p.partition("=")
                        atribut[k] = v
                hasil.append(LaguAwal(b[0], b[1], b[2], b[3], **atribut))
            except (ValueError, ValidasiError):
                rusak += 1
    return hasil, rusak


# 
# 5. SEBELUM: nama variabel tidak jelas + loop manual
#    (sesudah: nama jelas, hitung_total_durasi(*args), max(... lambda))
# 
def hitung_total_awal(d):
    t = 0
    for l in d:
        t = t + l.durasi_detik
    return t


def lagu_terpanjang_awal(d):
    p = None
    for l in d:
        if p is None or l.durasi_detik > p.durasi_detik:
            p = l
    return p


# 
# Pembanding: versi awal harus menghasilkan hasil yang SAMA dengan final
# 
if __name__ == "__main__":
    from playlist import Lagu, processing, fileio

    data = [("Hey Jude", "The Beatles", 1968, 431),
            ("Panic", "The Smiths", 1986, 139),
            ("Under Pressure", "Queen", 1981, 248)]
    awal = [LaguAwal(*x) for x in data]
    final = [Lagu(*x) for x in data]

    # 1. validasi: input salah harus ditolak oleh kedua versi
    for argumen in [("", "Queen", 1975, 200), ("A", "Queen", 1975, -10)]:
        for kelas in (LaguAwal, Lagu):
            try:
                kelas(*argumen)
            except Exception as e:
                print(f"1. {kelas.__name__:9s} menolak -> {type(e).__name__}")

    # 2. pengurutan
    for kunci in ("judul", "artis", "tahun", "durasi"):
        a = [l.judul for l in urutkan_lagu_awal(awal, berdasarkan=kunci)]
        f = [l.judul for l in processing.urutkan_lagu(final, berdasarkan=kunci)]
        print(f"2. urut {kunci:6s} sama: {a == f}")

    # 3. baca file (satu baris sengaja rusak)
    with tempfile.TemporaryDirectory() as folder:
        path = os.path.join(folder, "tes.txt")
        with open(path, "w", encoding="utf-8") as f:
            f.write("Panic;The Smiths;1986;139;album=Single\n")
            f.write("rusak;tanpa;format\n")
        a_lagu, a_rusak = baca_lagu_awal(path)
        f_lagu, f_rusak = fileio.baca_lagu(path)
    print(f"3. baca file sama: {len(a_lagu) == len(f_lagu)} "
          f"(rusak awal={a_rusak}, final={f_rusak})")

    # 5. total & terpanjang
    print("5. total sama:", hitung_total_awal(awal) ==
          processing.total_durasi_playlist(final))
    print("5. terpanjang sama:", lagu_terpanjang_awal(awal).judul ==
          processing.lagu_terpanjang(final).judul)