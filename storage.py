# storage.py
import os

def simpan_data_txt(filename, data_string):
    """
    Menyimpan atau menambahkan baris teks baru ke dalam file.
    """
    try:
        with open(filename, 'a', encoding='utf-8') as file:
            file.write(data_string + '\n')
        return True
    except Exception as e:
        print(f"[ERROR Storage] Gagal menyimpan ke {filename}: {e}")
        return False

def baca_data_txt(filename):
    """
    Membaca semua baris dari fille teks dan mengembalikannya dalam bentuk list.
    """
    lines = []
    if not os.path.exists(filename):
        print(f"[ERROR Storage] File {filename} tidak ditemukan.")
        return lines
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                cleaned_line = line.strip()
                if cleaned_line:  # Hanya tambahkan baris yang tidak kosong
                    lines.append(cleaned_line)
    except Exception as e:
        print(f"[ERROR Storage] Gagal membaca file {filename}: {e}")
    return lines