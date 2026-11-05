# data_master.py
import storage

# Menyiapkan konstanta untuk kolom dan nama file CSV siswa
HEADER_SISWA = ['nisn', 'nama', 'jenis_kelamin', 'usia_bulan', 'nama_ortu', 'penjemput_resmi']
FILE_SISWA = 'siswa.csv'

def muat_siswa():
    # Membaca data dari file CSV menggunakan modul storage
    data = storage.baca_csv(FILE_SISWA)
    return data

def cari_siswa(daftar, kata_kunci):
    # Menggunakan Linear Search untuk mencari berdasarkan NISN atau Nama
    kata = kata_kunci.strip().lower()
    for i in range(len(daftar)):
        if daftar[i]['nisn'] == kata_kunci.strip() or daftar[i]['nama'].lower() == kata:
            return daftar[i]
    return None

def tampilkan_tabel_siswa():
    # Menampilkan data siswa dalam bentuk tabel 
    daftar = muat_siswa()
    garis = '+' + '-' * 12 + '+' + '-' * 22 + '+' + '-' * 4 + '+' + '-' * 8 + '+'
    print(garis)
    print(f"|{'NISN':<12}|{'Nama':<22}|{'JK':<4}|{'Usia(bln)':<8}|")
    print(garis)
    for s in daftar:
        print(f"|{s['nisn']:<12}|{s['nama']:<22}|{s['jenis_kelamin']:<4}|{s['usia_bulan']:<8}|")
    print(garis)
    print('Total siswa:', len(daftar)) 