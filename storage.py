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