# data_master.py
import storage

# Menyiapkan konstanta untuk kolom dan nama file CSV siswa
HEADER_SISWA = ['nisn', 'nama', 'jenis_kelamin', 'usia_bulan', 'nama_ortu', 'penjemput_resmi']
FILE_SISWA = 'siswa.csv'

def muat_siswa():
    # Membaca data dari file CSV menggunakan modul storage
    data = storage.baca_csv(FILE_SISWA)
    return data
