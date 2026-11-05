# data_master.py
import storage

FILE_SISWA = 'siswa.txt'

def muat_siswa():
    # Membaca baris teks dari file menggunakan storage milik Firdaus
    baris_teks = storage.baca_data_txt(FILE_SISWA)
    daftar = []
    
    for baris in baris_teks:
        # Format teks: nisn|nama|jenis_kelamin|usia_bulan|nama_ortu|penjemput_resmi
        data_kolom = baris.split('|')
        if len(data_kolom) == 6:
            siswa = {
                'nisn': data_kolom[0],
                'nama': data_kolom[1],
                'jenis_kelamin': data_kolom[2],
                'usia_bulan': data_kolom[3],
                'nama_ortu': data_kolom[4],
                'penjemput_resmi': data_kolom[5]
            }
            daftar.append(siswa)
            
    # Jika file masih kosong, buatkan data contoh (dummy) otomatis
    if len(daftar) == 0:
        data_dummy = [
            "0012345678|Aisyah Putri|P|48|Budi Santoso|Budi Santoso",
            "0012345679|Rafi Pratama|L|52|Sari Dewi|Sari Dewi"
        ]
        for item in data_dummy:
            storage.simpan_data_txt(FILE_SISWA, item)
        return muat_siswa() # Muat ulang setelah diisi data dummy
        
    return daftar

def cari_siswa(daftar, kata_kunci):
    # Menggunakan Linear Search untuk mencari berdasarkan NISN atau Nama
    kata = kata_kunci.strip().lower()
    for i in range(len(daftar)):
        if daftar[i]['nisn'] == kata_kunci.strip() or daftar[i]['nama'].lower() == kata:
            return daftar[i]
    return None

def tampilkan_tabel_siswa():
    # Menampilkan data siswa dalam bentuk tabel rapi di terminal
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
    # Menambahkan data siswa baru ke file txt
    daftar = muat_siswa()
    nisn = input('NISN            : ').strip()
    if cari_siswa(daftar, nisn) is not None:
        print('NISN sudah terdaftar!')
        return
        
    nama = input('Nama            : ').strip()
    jk = input('Jenis kelamin (L/P): ').strip().upper()
    usia = input('Usia (bulan)    : ').strip()
    ortu = input('Nama orang tua  : ').strip()
    penjemput = input('Penjemput resmi : ').strip()
    
    # Gabungkan data dengan pemisah '|' sesuai format storage txt
    baris_baru = f"{nisn}|{nama}|{jk}|{usia}|{ortu}|{penjemput}"
    
    sukses = storage.simpan_data_txt(FILE_SISWA, baris_baru)
    if sukses:
        print('Siswa berhasil ditambahkan.')
    else:
        print('Gagal menyimpan siswa.')

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

if __name__ == '__main__':
    print(">>> Membuka Menu Data Master...")
    menu_data_master()