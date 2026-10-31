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

def autentikasi_login():
    """
    Fungsi untuk memvalidasi kredensial login penggunna dari file usenrs.txt.
    """
    print("\n===========================================")
    print("      AUTENTIKASI MASUK - EDUPARENT        ")
    print("===========================================")
    username_input = input("Masukkan Username : ").strip()
    password_input = input("Masukkan Password : ").strip()

    data_users = baca_data_txt("users.txt")

    for line in data_users:
        parts = line.split('|')
        if len(parts) >= 4:
            username, password, role, nama_lengkap = parts[0], parts[1], parts[2], parts[3]
            if username_input == username and password_input == password:
                return {"username": username, "role": role, "nama": nama_lengkap}
    print("\n[ERROR] Username atau password salah.")
    return None

def menu_guru(user_info):
    """
    Menampilkan menu untuk pengguna dengan peran guru.
    """
    while True:
        print("\n" +"="*45)
        print(f"   PANEL GURU - Selamat Datang, {user_info['nama']}!")
        print("="*45)
        print("1. Lihat & Cari Data Master Siswa")
        print("2. Input Presensi & Jurnal Harian")
        print("3. Verifikasi Status Penjemputan Anak")
        print("4. Input Evaluasi Tumbuh Kembang (TB/BB)")
        print("5. Lihat Urutan/Ranking Z-Score Siswa")
        print("6. Logout / Keluar")
        print("="*45)

        pilihan = input("Pilih menu (1-6): ").strip()

        if pilihan == '1':
            print("\n--- MENU DATA MASTER SISWA ---")
            print("a. Tampilkan Semua Siswa")
            print("b. Cari Siswa Berdasarkan NISN")
            sub_pilihan = input("Pilih menu (a/b): ").strip().lower()
            if sub_pilihan == 'a':
                tampilkan_semua_siswa()
            elif sub_pilihan == 'b':
                nisn = input("Masukkan NISN Siswa: ").strip()
                cari_siswa_by_nisn(nisn)
            else:
                print("[ERROR] Pilihan tidak valid. Silakan pilih 'a' atau 'b'.")
        elif pilihan == '2':
            input_presensi_jurnal()
        elif pilihan == '3':
            verifikasi_penjemputan()
        elif pilihan == '4':
            input_tumbuh_kembang()
        elif pilihan == '5':
            tampilkan_rangking_zscore()
        elif pilihan == '6':
            print("\n[INFO] Logout berhasil. Sampai jumpa!")
            break
        else:
            print("[ERROR] Pilihan tidak valid. Silakan pilih menu antara 1 hingga 6.")


def menu_orangtua(user_info):
    """
    Menampilkan menu untuk pengguna dengan peran orangtua.
    """
    while True:
        print("\n" +"="*45)
        print(f"   PANEL ORANGTUA - Selamat Datang, {user_info['nama']}!")
        print("="*45)
        print("1. Lihat Laporan Jurnal & Presensi Anak")
        print("2. Cek Status Penjemputan Anak Hari Ini")
        print("3. Lihat Perkembangan Tumbuh Kembang Anak")
        print("4. Logout / Keluar")
        print("="*45)

        pilihan = input("Pilih menu (1-4): ").strip()

        if pilihan == '1':
            print("\n[INFO] Fitur Lihat Laporan Jurnal & Presensi Anak belum tersedia. Silakan implementasikan di modul data_master.")
        elif pilihan == '2':
            print("\n[INFO] Fitur Cek Status Penjemputan Anak Hari Ini belum tersedia. Silakan implementasikan di modul fitur_harian.")
        elif pilihan == '3':
            print("\n[INFO] Fitur Lihat Perkembangan Tumbuh Kembang Anak belum tersedia. Silakan implementasikan di modul fitur_harian.")
        elif pilihan == '4':
            print("\n[INFO] Logout berhasil. Sampai jumpa!")
            break
        else:
            print("[ERROR] Pilihan tidak valid. Silakan pilih menu antara 1 hingga 4.")

def main():
    """
    Fungsi utama untuk menjalankan program EduParent.
    """
    inisialisasi_file_dasar()  # Pastikan file dasar tersedia sebelum login

    while True:
        print("\n" +"="*45)
        print("      SELAMAT DATANG DI EDUPARENT       ")
        print("="*45)
        print("1. Login Sistem")
        print("2. Keluar Sistem")
        print("="*45)

        opsi_awal = input("Pilih opsi (1-2): ").strip()

        if opsi_awal == '1':
            user_login = autentikasi_login()
            if user_login:
                print(f"\n[INFO] Login berhasil sebagai {user_login['role'].upper()}. Selamat datang, {user_login['nama']}!")
                if user_login['role'] == 'guru':
                    menu_guru(user_login)
                elif user_login['role'] == 'orang_tua':
                    menu_orangtua(user_login)
                else:
                    print("[ERROR] Username atau Password salah! Silakan coba lagi.")
        elif opsi_awal == '2':
            print("\n[INFO] Terima kasih telah menggunakan EduParent. Sampai jumpa!")
            break
        else:
            print("[ERROR] Pilihan tidak valid. Silakan pilih opsi 1 atau 2.")
if __name__ == "__main__":
    main()