"""models.py - class Lagu dan Playlist."""
from .validasi import (ValidasiError, validasi_teks,
                       validasi_angka_positif, validasi_tahun)


class Lagu:
    """Satu lagu. Atribut tambahan (album, genre, dll) lewat **kwargs."""

    def __init__(self, judul, artis, tahun, durasi_detik, **kwargs):
        # Setiap field divalidasi saat objek dibuat
        self.judul = validasi_teks(judul, "judul")
        self.artis = validasi_teks(artis, "artis")
        self.tahun = validasi_tahun(tahun)
        self.durasi_detik = validasi_angka_positif(durasi_detik, "durasi")
        # **kwargs: atribut yang bervariasi tiap lagu disimpan dalam dict
        self.atribut_tambahan = kwargs

    def durasi_format(self):
        """Ubah detik menjadi format menit:detik, contoh 354 -> 5:54."""
        menit, detik = divmod(self.durasi_detik, 60)
        return f"{menit}:{detik:02d}"

    def ke_baris(self):
        """Ubah objek menjadi satu baris teks untuk disimpan ke file."""
        extra = ",".join(f"{k}={v}" for k, v in self.atribut_tambahan.items())
        return f"{self.judul};{self.artis};{self.tahun};{self.durasi_detik};{extra}"

    @classmethod
    def dari_baris(cls, baris):
        """Buat objek Lagu dari satu baris file. Baris rusak -> exception."""
        bagian = baris.strip().split(";")
        if len(bagian) != 5:
            raise ValueError(f"Jumlah kolom {len(bagian)}, seharusnya 5")
        judul, artis, tahun, durasi, extra = bagian
        atribut = {}
        for pasangan in extra.split(","):
            if "=" in pasangan:
                kunci, _, nilai = pasangan.partition("=")
                atribut[kunci] = nilai
        # **atribut: dict dibongkar menjadi keyword argument
        return cls(judul, artis, tahun, durasi, **atribut)

    def __str__(self):
        album = self.atribut_tambahan.get("album", "-")
        return (f"{self.judul} - {self.artis} ({self.tahun}) "
                f"[{self.durasi_format()}] album: {album}")


class Playlist:
    """Kumpulan lagu dalam satu playlist."""

    def __init__(self, nama):
        self.nama = nama
        self.daftar = []

    def tambah(self, lagu):
        """Tambah lagu; tolak jika judul + artis sudah ada."""
        for l in self.daftar:
            if (l.judul.lower(), l.artis.lower()) == \
               (lagu.judul.lower(), lagu.artis.lower()):
                raise ValidasiError(f"Lagu '{lagu.judul}' sudah ada di playlist")
        self.daftar.append(lagu)

    def hapus(self, judul):
        """Hapus lagu berdasarkan judul. Return True jika ada yang dihapus."""
        sebelum = len(self.daftar)
        self.daftar = [l for l in self.daftar
                       if l.judul.lower() != judul.lower()]
        return len(self.daftar) < sebelum

    def jumlah(self):
        return len(self.daftar)