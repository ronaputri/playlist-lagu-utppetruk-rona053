"""fileio.py - baca / tulis / tambah file. Semua pakai with open()."""
from .models import Lagu
from .validasi import ValidasiError


def buat_file_data(path, lagu_awal):
    """Mode 'x': membuat file data pertama kali, gagal jika sudah ada
    sehingga data lama tidak pernah tertimpa."""
    try:
        with open(path, "x", encoding="utf-8") as file:
            for lagu in lagu_awal:
                file.write(lagu.ke_baris() + "\n")
        print(f"File '{path}' berhasil dibuat.")
        return True
    except FileExistsError:
        print(f"File '{path}' sudah ada, tidak dibuat ulang.")
        return False


def tambah_lagu(path, lagu):
    """Mode 'a': menambah satu lagu di akhir file tanpa menghapus data lama."""
    with open(path, "a", encoding="utf-8") as file:
        file.write(lagu.ke_baris() + "\n")


def baca_lagu(path):
    """Mode 'r': membaca baris demi baris (iteratif).
    Baris rusak dilewati. Return (list_lagu, jumlah_baris_rusak)."""
    hasil = []
    rusak = 0
    try:
        with open(path, "r", encoding="utf-8") as file:
            for nomor, baris in enumerate(file, start=1):  # iteratif
                if not baris.strip():
                    continue  # lewati baris kosong
                try:
                    hasil.append(Lagu.dari_baris(baris))
                except (ValueError, ValidasiError) as err:
                    # Baris rusak dilewati, program tetap lanjut
                    rusak += 1
                    print(f"  [!] Baris {nomor} dilewati: {err}")
    except FileNotFoundError:
        print(f"Error: file '{path}' belum ada. Jalankan program utama "
              f"terlebih dahulu untuk membuatnya.")
        return [], 0
    return hasil, rusak


def tulis_laporan(path, teks):
    """Mode 'w': menulis laporan (isi lama diganti dengan laporan terbaru)."""
    with open(path, "w", encoding="utf-8") as file:
        file.write(teks)


def tampilkan_file(path):
    """Tampilkan isi file ke layar (mode 'r', iteratif)."""
    try:
        with open(path, "r", encoding="utf-8") as file:
            for baris in file:
                print(baris.rstrip())
    except FileNotFoundError:
        print(f"Error: file '{path}' tidak ditemukan.")