class ValidasiError(Exception):
    """Exception buatan sendiri untuk data yang tidak valid."""


def validasi_teks(nilai, nama_field):
    """Pastikan teks tidak kosong dan tidak mengandung ';' (pemisah file)."""
    teks = str(nilai).strip()
    if not teks:
        # raise: memunculkan exception buatan sendiri saat field kosong
        raise ValidasiError(f"Field '{nama_field}' tidak boleh kosong")
    if ";" in teks:
        raise ValidasiError(f"Field '{nama_field}' tidak boleh berisi ';'")
    return teks


def validasi_angka_positif(nilai, nama_field):
    """Ubah ke int dan pastikan > 0. int() bisa memunculkan ValueError."""
    angka = int(nilai)
    if angka <= 0:
        raise ValidasiError(f"Field '{nama_field}' harus lebih dari 0")
    return angka


def validasi_tahun(nilai):
    """Pastikan tahun berupa angka dalam rentang wajar."""
    tahun = int(nilai)
    if not 1900 <= tahun <= 2100:
        raise ValidasiError(f"Tahun {tahun} di luar rentang 1900-2100")
    return tahun


if __name__ == "__main__":
    # Blok pengujian lokal: hanya jalan jika file ini dieksekusi langsung,
    # TIDAK jalan saat modul ini diimpor oleh modul lain / main.py.
    print("Uji lokal validasi.py")
    print(validasi_teks("  Queen ", "artis"))
    print(validasi_angka_positif("240", "durasi"))
    for percobaan in (lambda: validasi_teks("", "judul"),
                      lambda: validasi_angka_positif("-5", "durasi"),
                      lambda: validasi_angka_positif("abc", "durasi")):
        try:
            percobaan()
        except (ValidasiError, ValueError) as e:
            print("Error tertangkap:", e)