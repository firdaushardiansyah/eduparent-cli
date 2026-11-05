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

def tambah_siswa():
    # Menambahkan data siswa baru ke file CSV
    daftar = muat_siswa()
    nisn = input('NISN            : ').strip()
    if cari_siswa(daftar, nisn) is not None:
        print('NISN sudah terdaftar!')
        return
    baru = {
        'nisn': nisn,
        'nama': input('Nama            : ').strip(),
        'jenis_kelamin': input('Jenis kelamin (L/P): ').strip().upper(),
        'usia_bulan': input('Usia (bulan)    : ').strip(),
        'nama_ortu': input('Nama orang tua  : ').strip(),
        'penjemput_resmi': input('Penjemput resmi : ').strip(),
    }
    storage.tambah_baris_csv(FILE_SISWA, HEADER_SISWA, baru)
    print('Siswa berhasil ditambahkan.')

def menu_data_master():
    # Menu interaktif berbasis teks
    while True:
        print('\n--- DATA MASTER ---')
        print('1. Lihat semua siswa')
        print('2. Cari siswa (NISN/Nama)')
        print('3. Tambah siswa')
        print('0. Kembali')
        p = input('Pilih: ')
        if p == '1':
            tampilkan_tabel_siswa()
        elif p == '2':
            hasil = cari_siswa(muat_siswa(), input('Kata kunci: '))
            print(hasil if hasil is not None else 'Siswa tidak ditemukan.')
        elif p == '3':
            tambah_siswa()
        elif p == '0':
            print('Keluar dari menu Data Master.')
            break
        else:
            print('Pilihan tidak valid. Silakan pilih 0-3.')

# Bagian pemanggil utama agar menu otomatis muncul saat file dijalankan
if __name__ == '__main__':
    print(">>> Membuka Menu Data Master...")
    menu_data_master()