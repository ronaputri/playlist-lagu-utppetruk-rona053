"""main.py - program utama Playlist Lagu (Queen, The Beatles, The Smiths)."""
import os
import unittest

from playlist import Lagu, Playlist, ValidasiError, fileio, processing
from playlist import testing

# Lokasi file selalu relatif terhadap folder main.py
FOLDER = os.path.dirname(os.path.abspath(__file__))
FILE_DATA = os.path.join(FOLDER, "data_playlist.txt")
FILE_LAPORAN = os.path.join(FOLDER, "laporan_playlist.txt")


def lagu_awal():
    """Data awal playlist yang ditulis saat file data pertama kali dibuat."""
    return [
        Lagu("Bohemian Rhapsody", "Queen", 1975, 354, album="A Night at the Opera"),
        Lagu("Somebody to Love", "Queen", 1976, 297, album="A Day at the Races"),
        Lagu("We Will Rock You", "Queen", 1977, 122, album="News of the World"),
        Lagu("Don't Stop Me Now", "Queen", 1978, 209, album="Jazz"),
        Lagu("Another One Bites the Dust", "Queen", 1980, 215, album="The Game"),
        Lagu("Under Pressure", "Queen", 1981, 248, album="Hot Space"),
        Lagu("Help!", "The Beatles", 1965, 138, album="Help!"),
        Lagu("Yesterday", "The Beatles", 1965, 125, album="Help!"),
        Lagu("Hey Jude", "The Beatles", 1968, 431, album="Hey Jude"),
        Lagu("Come Together", "The Beatles", 1969, 259, album="Abbey Road"),
        Lagu("Here Comes the Sun", "The Beatles", 1969, 185, album="Abbey Road"),
        Lagu("Let It Be", "The Beatles", 1970, 243, album="Let It Be"),
        Lagu("This Charming Man", "The Smiths", 1983, 162, album="Single"),
        Lagu("Heaven Knows I'm Miserable Now", "The Smiths", 1984, 224,
             album="Hatful of Hollow"),
        Lagu("How Soon Is Now?", "The Smiths", 1984, 400, album="Hatful of Hollow"),
        Lagu("Panic", "The Smiths", 1986, 139, album="Single"),
        Lagu("Bigmouth Strikes Again", "The Smiths", 1986, 193,
             album="The Queen Is Dead"),
        Lagu("There Is a Light That Never Goes Out", "The Smiths", 1986, 244,
             album="The Queen Is Dead"),
    ]


def muat_playlist():
    """Baca file data dan kembalikan objek Playlist."""
    playlist = Playlist("Playlist Klasik")
    daftar, rusak = fileio.baca_lagu(FILE_DATA)
    for lagu in daftar:
        try:
            playlist.tambah(lagu)
        except ValidasiError as err:
            print(f"  [!] {err}")
    if rusak:
        print(f"({rusak} baris rusak dilewati)")
    return playlist


def tampilkan(daftar):
    """Cetak daftar lagu bernomor."""
    if not daftar:
        print("(tidak ada lagu)")
    for i, lagu in enumerate(daftar, start=1):
        print(f"{i:2d}. {lagu}")


def menu_tambah():
    """Minta input lagu baru, validasi, lalu simpan ke file (mode 'a')."""
    print("\n-- Tambah lagu baru --")
    try:
        lagu = Lagu(input("Judul   : "), input("Artis   : "),
                    input("Tahun   : "), input("Durasi (detik): "),
                    album=input("Album   : ").strip() or "-")
        playlist = muat_playlist()
        playlist.tambah(lagu)          # cek duplikat
        fileio.tambah_lagu(FILE_DATA, lagu)
        print("Lagu berhasil ditambahkan.")
    except ValueError:
        print("Input salah: tahun dan durasi harus berupa angka.")
    except ValidasiError as err:
        print(f"Data tidak valid: {err}")


def menu_urutkan(playlist):
    print("Urutkan berdasarkan: judul / artis / tahun / durasi")
    kunci = input("Pilihan: ").strip().lower()
    terbalik = input("Terbalik? (y/n): ").strip().lower() == "y"
    try:
        # keyword argument saat memanggil fungsi
        tampilkan(processing.urutkan_lagu(playlist.daftar,
                                          berdasarkan=kunci, terbalik=terbalik))
    except ValidasiError as err:
        print(f"Error: {err}")


def menu_laporan(playlist):
    """Buat laporan (mode 'w') lalu tampilkan isinya dari file."""
    teks = processing.buat_laporan(playlist.daftar, nama_playlist=playlist.nama)
    fileio.tulis_laporan(FILE_LAPORAN, teks)
    print(f"\nLaporan disimpan di: {FILE_LAPORAN}\n")
    fileio.tampilkan_file(FILE_LAPORAN)


def jalankan_tes():
    """Jalankan seluruh unittest di playlist/testing.py."""
    suite = unittest.defaultTestLoader.loadTestsFromModule(testing)
    unittest.TextTestRunner(verbosity=2).run(suite)


def main():
    # Membuat file data pertama kali (mode 'x'); jika sudah ada, dilewati
    fileio.buat_file_data(FILE_DATA, lagu_awal())

    while True:
        print("\n===== PLAYLIST LAGU =====")
        print("1. Tampilkan semua lagu")
        print("2. Tambah lagu")
        print("3. Urutkan lagu")
        print("4. Cari berdasarkan artis")
        print("5. Buat laporan")
        print("6. Jalankan pengujian (unittest)")
        print("0. Keluar")
        pilihan = input("Pilih menu: ").strip()

        if pilihan == "0":
            print("Terima kasih!")
            break
        elif pilihan == "2":
            menu_tambah()
        elif pilihan == "6":
            jalankan_tes()
        elif pilihan in ("1", "3", "4", "5"):
            playlist = muat_playlist()
            if pilihan == "1":
                tampilkan(playlist.daftar)
            elif pilihan == "3":
                menu_urutkan(playlist)
            elif pilihan == "4":
                tampilkan(processing.filter_artis(playlist.daftar,
                                                  input("Nama artis: ")))
            else:
                menu_laporan(playlist)
        else:
            print("Pilihan tidak valid.")


if __name__ == "__main__":
    main()