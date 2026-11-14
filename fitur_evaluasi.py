import math
from datetime import datetime

import data_master
import storage

# Fungsi dan variabel untuk fitur evaluasi tumbuh kembang
FILE_EVALUASI = "tumbuh_kembang.txt"  #file storage text data evaluasi tumbuh kembang
HEADER_EVALUASI = [
    "nisn",
    "bulan_tahun",
    "tb",
    "bb",
    "lk",
    "zscore_tb",
    "status_gizi",
]

# Nilai dari briefing menggunakan contoh pada dokumen panduan aka briefing
ACUAN_TB = {
    ("P", 48): (100.3, 4.1),
    ("L", 48): (102.3, 4.2),
    ("P", 52): (102.9, 4.2),
    ("L", 52): (104.5, 4.3),
}

# fungsi menghitung Z-Score TB/U
def hitung_zscore_tb(tb, jenis_kelamin, usia_bulan):
    """
    Menghitung Z-Score TB/U dari acuan median dan simpangan baku.
    Mengembalikan None jika kelompok usia/jenis kelamin belum memiliki acuan.
    """
    kunci = (jenis_kelamin, usia_bulan)
    if kunci not in ACUAN_TB:
        return None

    median, simpangan_baku = ACUAN_TB[kunci]
    return (tb - median) / simpangan_baku

# fungsi menentukan status gizi berdasarkan Z-Score TB/U
def tentukan_status_gizi(zscore_tb):
    if zscore_tb < -3:
        return "Sangat pendek"
    elif zscore_tb < -2:
        return "Pendek"
    elif zscore_tb <= 3:
        return "Normal"
    return "Tinggi"

#pencarian data siswa dari NISN
def _cari_siswa(nisn):
    if callable(getattr(data_master, "cari_siswa_by_nisn", None)):
        return True, data_master.cari_siswa_by_nisn(nisn)

    if callable(getattr(data_master, "muat_siswa", None)) and callable(
        getattr(data_master, "cari_siswa", None)
    ):
        daftar_siswa = data_master.muat_siswa()
        return True, data_master.cari_siswa(daftar_siswa, nisn)

    print(
        "[ERROR] Fungsi pencarian siswa belum tersedia. "
        "data_master.py harus menyediakan cari_siswa_by_nisn(nisn) "
        "atau muat_siswa() dan cari_siswa(daftar, kata_kunci)."
    )
    return False, None

#fungsi input ukuran (TB, BB, LK) dengan validasi
def _input_ukuran(label):
    nilai_teks = input(label).strip()
    try:
        nilai = float(nilai_teks)
    except ValueError:
        print("[ERROR] Input harus berupa angka.")
        return None

    if not math.isfinite(nilai) or nilai <= 0:
        print("[ERROR] Nilai ukuran harus berupa angka lebih besar dari 0.")
        return None
    return nilai

#utk input bulan & tahun pengukuran, default bulan sekarang jika tidak diisi
def _input_bulan_tahun():
    bulan_sekarang = datetime.now().strftime("%Y-%m")
    while True:
        bulan_tahun = input(
            f"Bulan pengukuran (YYYY-MM) [{bulan_sekarang}]: "
        ).strip()
        if bulan_tahun == "":
            return bulan_sekarang   #otomatis menggunakan bulan sekarang jika tidak diisi

        if _bulan_tahun_valid(bulan_tahun):
            return bulan_tahun

        print("[ERROR] Format bulan tidak valid. Gunakan format YYYY-MM.")

#fungsi validasi format bulan_tahun
def _bulan_tahun_valid(bulan_tahun):
    bagian = bulan_tahun.split("-")
    return (
        len(bagian) == 2
        and len(bagian[0]) == 4
        and bagian[0].isdecimal()
        and len(bagian[1]) == 2
        and bagian[1].isdecimal()
        and 1 <= int(bagian[1]) <= 12
        and int(bagian[0]) > 0
    )

#fungsi utk membaca data evaluasi dari file tumbuh_kembang.txt
def input_tumbuh_kembang():
    print("\n--- INPUT EVALUASI TUMBUH KEMBANG ---")
    nisn = input("Masukkan NISN siswa: ").strip()
    if nisn == "" or "|" in nisn:
        print("[ERROR] NISN wajib diisi dan tidak boleh mengandung karakter '|'.")
        return

    pencarian_tersedia, siswa = _cari_siswa(nisn)
    if not pencarian_tersedia:
        return
    if siswa is None:
        print("[INFO] Siswa dengan NISN tersebut tidak ditemukan.")
        return

    if "jenis_kelamin" not in siswa or "usia_bulan" not in siswa:
        print(
            "[ERROR] Data siswa harus memiliki kunci 'jenis_kelamin' "
            "dan 'usia_bulan' untuk menghitung Z-Score."
        )
        return

    jenis_kelamin = str(siswa["jenis_kelamin"]).strip().upper()
    usia_teks = str(siswa["usia_bulan"]).strip()
    if not usia_teks.isdecimal():
        print("[ERROR] Usia siswa pada data master harus berupa bilangan bulan.")
        return
    usia_bulan = int(usia_teks)

    if jenis_kelamin not in ("L", "P") or usia_bulan <= 0:
        print("[ERROR] Jenis kelamin atau usia pada data master tidak valid.")
        return

    tb = _input_ukuran("Tinggi badan (cm): ")
    if tb is None:
        return
    bb = _input_ukuran("Berat badan (kg): ")
    if bb is None:
        return
    lk = _input_ukuran("Lingkar kepala (cm): ")
    if lk is None:
        return

    zscore_tb = hitung_zscore_tb(tb, jenis_kelamin, usia_bulan)
    if zscore_tb is None:
        print(
            "[ERROR] Acuan Z-Score belum tersedia untuk jenis kelamin "
            f"{jenis_kelamin} dan usia {usia_bulan} bulan. Data tidak disimpan."
        )
        return

    zscore_tersimpan = round(zscore_tb, 2)
    status_gizi = tentukan_status_gizi(zscore_tersimpan)
    bulan_tahun = _input_bulan_tahun()

    baris = "|".join(
        [
            nisn,
            bulan_tahun,
            str(tb),
            str(bb),
            str(lk),
            str(zscore_tersimpan),
            status_gizi,
        ]
    )
    if not storage.simpan_data_txt(FILE_EVALUASI, baris):
        print("[ERROR] Evaluasi gagal disimpan.")
        return
    print(f"\nZ-Score TB/U: {zscore_tersimpan:.2f}")
    print(f"Status gizi: {status_gizi}")
    print(
        "[PERINGATAN] Nilai acuan pada modul masih menggunakan contoh dari dokumen panduan & briefing."
    )
    print("[INFO] Data evaluasi berhasil disimpan.")

#fungsi membaca data evaluasi dari file tumbuh_kembang.txt
def _baca_data_evaluasi():
    data_evaluasi = []
    for nomor_baris, baris in enumerate(
        storage.baca_data_txt(FILE_EVALUASI), start=1
    ):
        bagian = baris.split("|")
        if (
            len(bagian) != len(HEADER_EVALUASI)
            or bagian[0].strip() == ""
            or not _bulan_tahun_valid(bagian[1].strip())
            or bagian[6].strip() == ""
        ):
            print(
                f"[ERROR] Baris {nomor_baris} pada {FILE_EVALUASI} "
                "tidak sesuai format dan dilewati."
            )
            continue

        try:
            zscore_tb = float(bagian[5])
            tb = float(bagian[2])
        except ValueError:
            print(
                f"[ERROR] Nilai TB atau Z-Score pada baris {nomor_baris} "
                "tidak valid dan dilewati."
            )
            continue

        if (
            not math.isfinite(zscore_tb)
            or not math.isfinite(tb)
            or tb <= 0
        ):
            print(
                f"[ERROR] Nilai TB atau Z-Score pada baris {nomor_baris} "
                "tidak valid dan dilewati."
            )
            continue

        data_evaluasi.append(
            {
                "nisn": bagian[0],
                "bulan_tahun": bagian[1],
                "tb": tb,
                "zscore_tb": zscore_tb,
                "status_gizi": bagian[6],
            }
        )
    return data_evaluasi

#fungsi mengurutkan data evaluasi berdasarkan zscore_tb secara menurun
def _urutkan_zscore_menurun(data_evaluasi):
    jumlah_data = len(data_evaluasi)
    for i in range(jumlah_data - 1):
        for j in range(jumlah_data - 1 - i):
            if data_evaluasi[j]["zscore_tb"] < data_evaluasi[j + 1]["zscore_tb"]:
                sementara = data_evaluasi[j]
                data_evaluasi[j] = data_evaluasi[j + 1]
                data_evaluasi[j + 1] = sementara
    return data_evaluasi

#fungsi menampilkan rangking zscore_tb secara menurun
def tampilkan_rangking_zscore():
    print("\n--- RANGKING Z-SCORE TB/U ---")
    data_evaluasi = _baca_data_evaluasi()
    if len(data_evaluasi) == 0:
        print("[INFO] Belum ada data evaluasi yang dapat ditampilkan.")
        return

    data_evaluasi = _urutkan_zscore_menurun(data_evaluasi)
    print(
        f"{'No.':<5}{'NISN':<16}{'Bulan':<10}"
        f"{'TB (cm)':<12}{'Z-Score':<10}Status"
    )
    for indeks, evaluasi in enumerate(data_evaluasi, start=1):
        print(
            f"{indeks:<5}{evaluasi['nisn']:<16}{evaluasi['bulan_tahun']:<10}"
            f"{evaluasi['tb']:<12.2f}{evaluasi['zscore_tb']:<10.2f}"
            f"{evaluasi['status_gizi']}"
        )
