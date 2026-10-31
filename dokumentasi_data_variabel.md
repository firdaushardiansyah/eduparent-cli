# 📖 DOKUMENTASI VARIABEL & STRUKTUR DATA EDUPARENT CLI

Dokumen ini adalah acuan resmi (*Single Source of Truth*) nama variabel, kunci (*key*) dictionary, format file storage, dan kontrak fungsi yang **WAJIB** digunakan oleh seluruh anggota kelompok (Firdaus, Dzaky, Felya, Dzakwan).

---

## 🚦 1. STATUS IMPLEMENTASI PROGRAM SAAT INI

| Modul File | Penanggung Jawab | Status Integrasi di `main.py` | Keterangan Lengkap |
| :--- | :--- | :--- | :--- |
| `storage.py` | **Firdaus** | **Aktif (100%)** | Operasi baca/tulis file teks & inisialisasi file default berjalan lancar. |
| `main.py` | **Firdaus** | **Aktif Parsial** | **Menu Utama, Routing Akses, & Autentikasi Login Aktif (100%)**. Menu Orang Tua masih berupa tampilan statis/pesan belum tersedia. |
| `data_master.py` | Dzaky | *Dalam Pengembangan* | Menggunakan *fallback mock function* di `main.py`. |
| `fitur_harian.py` | Felya | *Dalam Pengembangan* | Menggunakan *fallback mock function* di `main.py`. |
| `fitur_evaluasi.py` | Dzakwan | *Dalam Pengembangan* | Menggunakan *fallback mock function* di `main.py`. |

---

## 📁 2. FORMAT FILE STORAGE TEKS (DATABASE FILE)

Data disimpan menggunakan format file teks sederhana dengan pemisah karakter garis tegak (`|`).

### 2.1 `users.txt` (Sudah Aktif & Terverifikasi Kode)
* **Format:** `username|password|role|nama_lengkap`
* **Contoh Data:**
  ```text
  guru|123|guru|Ibu Guru Ani
  ortu|123|orang_tua|Bapak Ahmad
  ```

### 2.2 `jurnal.txt` (Rancangan Format Modul Harian)
* **Format:** `nisn|tanggal|status_presensi|catatan_makan|aktivitas`
* **Contoh Data:**
  ```text
  1001|2026-11-01|Hadir|Makan Nasi Ayam|Bermain Balok Teks
  ```

### 2.3 `penjemputan.txt` (Rancangan Format Modul Penjemputan)
* **Format:** `nisn|tanggal|status_jemput|nama_penjemput|waktu_jemput`
* **Contoh Data:**
  ```text
  1001|2026-11-01|SUDAH_DIJEMPUT|Budi (Paman)|14:30
  ```

### 2.4 `tumbuh_kembang.txt` (Rancangan Format Modul Evaluasi)
* **Format:** `nisn|bulan_tahun|tb|bb|lk|zscore_tb|status_gizi`
* **Contoh Data:**
  ```text
  1001|2026-10|95.5|14.2|48.0|0.25|Gizi Baik
  ```

---

## 🗂️ 3. STANDAR STRUKTUR DATA (DICTIONARY KEYS)

Saat membaca data dari file teks ke memori program, anggota kelompok **WAJIB** menggunakan kunci *Dictionary* berikut:

### 3.1 Data Master Siswa (`data_master.py` - Dzaky)
```python
siswa = {
    "nisn": "1001",                   # str
    "nama": "Budi Santoso",            # str
    "kelas": "TK-A",                   # str
    "nama_ortu": "Bapak Ahmad",        # str
    "penjemput_resmi": ["Bapak Ahmad", "Ibu Siti", "Paman Budi"]  # list of str
}
```

### 3.2 Data Jurnal & Penjemputan (`fitur_harian.py` - Felya)
```python
jurnal_harian = {
    "nisn": "1001",                   # str
    "tanggal": "2026-11-01",          # str (YYYY-MM-DD)
    "status_presensi": "Hadir",       # str ("Hadir"/"Sakit"/"Izin"/"Alpa")
    "catatan_makan": "Habis 1 porsi", # str
    "aktivitas": "Mewarnai gambar"    # str
}

penjemputan = {
    "nisn": "1001",                   # str
    "tanggal": "2026-11-01",          # str (YYYY-MM-DD)
    "status_jemput": "SUDAH_DIJEMPUT",# str ("BELUM_DIJEMPUT" / "SUDAH_DIJEMPUT")
    "nama_penjemput": "Budi (Paman)", # str ("-" jika belum dijemput)
    "waktu_jemput": "14:30"           # str ("-" jika belum dijemput)
}
```

### 3.3 Data Evaluasi Tumbuh Kembang (`fitur_evaluasi.py` - Dzakwan)
```python
evaluasi = {
    "nisn": "1001",                   # str
    "bulan_tahun": "2026-10",         # str (YYYY-MM)
    "tb": 95.5,                       # float (Input fisik pengguna)
    "bb": 14.2,                       # float (Input fisik pengguna)
    "lk": 48.0,                       # float (Input fisik pengguna)
    "zscore_tb": 0.25,                # float (Hasil kalkulasi rumus z-score)
    "status_gizi": "Gizi Baik"        # str (Hasil penentuan status)
}
```

---

## ⚙️ 4. KONTRAK NAMA FUNGSI INTERFACE MODUL

Agar `main.py` dapat mengintegrasikan seluruh file tanpa error, nama fungsi di modul kalian **WAJIB SAMA PERSIS** dengan deklarasi berikut:

### 🔹 Modul Dzaky (`data_master.py`)
1. `tampilkan_semua_siswa()`
2. `cari_siswa_by_nisn(nisn)` $\rightarrow$ **Parameter wajib:** `nisn` (`str`). Mengembalikan `dict` data siswa atau `None` jika tidak ditemukan.

### 🔹 Modul Felya (`fitur_harian.py`)
1. `input_presensi_jurnal()`
2. `verifikasi_penjemputan()`

### 🔹 Modul Dzakwan (`fitur_evaluasi.py`)
1. `input_tumbuh_kembang()`
2. `tampilkan_rangking_zscore()` $\rightarrow$ *(Catatan: Di-import di `main.py` dengan ejaan `rangking` menggunakan huruf 'g')*.

---

## 📌 5. ATURAN PENGEMBANGAN & TIPE DATA

1. **Aturan Tipe Data & Input Pengguna:**
   * Angka ukur fisik (`tb`, `bb`, `lk`) **wajib dikonversi ke `float`** saat menerima input dari pengguna: `float(input())`.
   * Nilai `zscore_tb` **bukan di-input pengguna**, melainkan **hasil kalkulasi fungsi** di `fitur_evaluasi.py`.
2. **Karakter Terlarang:** Dilarang menginput karakter pipe (`|`) di dalam teks input terminal pengguna untuk menghindari kesalahan parsing string (`.split('|')`).