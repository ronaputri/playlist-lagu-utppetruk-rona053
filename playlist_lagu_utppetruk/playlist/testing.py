"""testing.py - pengujian dengan library unittest.

Jalankan: python -m unittest playlist.testing -v
"""
import os
import tempfile
import unittest

from .models import Lagu, Playlist
from .validasi import ValidasiError
from . import fileio, processing


def _contoh():
    """Data contoh untuk pengujian."""
    return [Lagu("Hey Jude", "The Beatles", 1968, 431),
            Lagu("Panic", "The Smiths", 1986, 139),
            Lagu("Under Pressure", "Queen", 1981, 248)]


class TestLagu(unittest.TestCase):
    def test_lagu_valid_dan_kwargs(self):
        lagu = Lagu("Yesterday", "The Beatles", "1965", "125", album="Help!")
        self.assertEqual(lagu.tahun, 1965)
        self.assertEqual(lagu.atribut_tambahan["album"], "Help!")

    def test_durasi_format(self):
        self.assertEqual(Lagu("A", "B", 2000, 354).durasi_format(), "5:54")

    def test_judul_kosong_memunculkan_error(self):
        with self.assertRaises(ValidasiError):
            Lagu("  ", "Queen", 1975, 200)

    def test_durasi_negatif_memunculkan_error(self):
        with self.assertRaises(ValidasiError):
            Lagu("A", "Queen", 1975, -10)

    def test_dari_baris_rusak(self):
        with self.assertRaises(ValueError):
            Lagu.dari_baris("Panic;The Smiths;abc;139;")

    def test_playlist_tolak_duplikat(self):
        pl = Playlist("Tes")
        pl.tambah(Lagu("Panic", "The Smiths", 1986, 139))
        with self.assertRaises(ValidasiError):
            pl.tambah(Lagu("panic", "the smiths", 1986, 139))


class TestProcessing(unittest.TestCase):
    def test_total_durasi_args(self):
        self.assertEqual(processing.hitung_total_durasi(100, 200, 50), 350)

    def test_total_durasi_negatif_assert(self):
        with self.assertRaises(AssertionError):
            processing.hitung_total_durasi(100, -1)

    def test_rata_rata_durasi(self):
        self.assertAlmostEqual(processing.rata_rata_durasi(_contoh()),
                               (431 + 139 + 248) / 3)

    def test_urutkan_berdasarkan_tahun_terbalik(self):
        hasil = processing.urutkan_lagu(_contoh(), berdasarkan="tahun",
                                        terbalik=True)
        self.assertEqual(hasil[0].judul, "Panic")

    def test_filter_artis(self):
        hasil = processing.filter_artis(_contoh(), "queen")
        self.assertEqual([l.judul for l in hasil], ["Under Pressure"])

    def test_lagu_terpanjang(self):
        self.assertEqual(processing.lagu_terpanjang(_contoh()).judul, "Hey Jude")


class TestFileIO(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.path = os.path.join(self.folder.name, "data.txt")

    def tearDown(self):
        self.folder.cleanup()

    def test_buat_file_tidak_menimpa(self):
        self.assertTrue(fileio.buat_file_data(self.path, _contoh()))
        self.assertFalse(fileio.buat_file_data(self.path, []))
        daftar, _ = fileio.baca_lagu(self.path)
        self.assertEqual(len(daftar), 3)

    def test_tambah_lagu(self):
        fileio.buat_file_data(self.path, _contoh())
        fileio.tambah_lagu(self.path, Lagu("Help!", "The Beatles", 1965, 138))
        daftar, _ = fileio.baca_lagu(self.path)
        self.assertEqual(len(daftar), 4)

    def test_baris_rusak_dilewati(self):
        with open(self.path, "w", encoding="utf-8") as f:
            f.write("Panic;The Smiths;1986;139;album=Single\n")
            f.write("rusak;tanpa;format\n")
            f.write("Lagu;Queen;abc;200;\n")
        daftar, rusak = fileio.baca_lagu(self.path)
        self.assertEqual((len(daftar), rusak), (1, 2))

    def test_file_tidak_ada(self):
        daftar, rusak = fileio.baca_lagu(os.path.join(self.folder.name, "x.txt"))
        self.assertEqual((daftar, rusak), ([], 0))


if __name__ == "__main__":
    unittest.main(verbosity=2)