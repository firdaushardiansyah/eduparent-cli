# main.py
import os
from storage import simpan_data_txt, baca_data_txt, inisialisasi_file_dasar

# Mock/Fallback fungsi milik modul teman jika belum tersedia
try:
    from data_master import tampilkan_semua_siswa, cari_siswa_by_nisn
except ImportError:
    def tampilkan_semua_siswa():
        print("\n[INFO] Fungsi tampilkan_semua_siswa() belum tersedia. Silakan implementasikan di modul data_master.")

    def cari_siswa_by_nisn(nisn):
        print(f"\n[INFO] Fungsi cari_siswa_by_nisn({nisn}) belum tersedia. Silakan implementasikan di modul data_master.")
        return None

try:
    from fitur_harian import input_presensi_jurnal, verifikasi_penjemputan
except ImportError:
    def input_presensi_jurnal():
        print("\n[INFO] Fungsi input_presensi_jurnal() belum tersedia. Silakan implementasikan di modul fitur_harian.")

    def verifikasi_penjemputan():
        print("\n[INFO] Fungsi verifikasi_penjemputan() belum tersedia. Silakan implementasikan di modul fitur_harian.")

try:
    from fitur_evaluasi import input_tumbuh_kembang, tampilkan_rangking_zscore
except ImportError:
    def input_tumbuh_kembang():
        print("\n[INFO] Fungsi input_tumbuh_kembang() belum tersedia. Silakan implementasikan di modul fitur_evaluasi.")

    def tampilkan_rangking_zscore():
        print("\n[INFO] Fungsi tampilkan_rangking_zscore() belum tersedia. Silakan implementasikan di modul fitur_evaluasi.")