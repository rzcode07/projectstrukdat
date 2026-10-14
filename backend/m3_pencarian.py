# backend/m3_laporan.py
# Modul Milestone 3: Sort & Search (Insertion Sort, Merge Sort, Linear Search, Binary Search)

class Pesanan:
    """Kelas representasi data satu pesanan dari pesanan.csv."""
    def __init__(self, oid, pelanggan, resto, menu, harga, prioritas, t_masuk, t_selesai, status):
        self.oid = oid
        self.pelanggan = pelanggan
        self.resto = resto
        self.menu = menu
        self.harga = int(harga) if (harga is not None and str(harga).strip() != "") else 0
        self.prioritas = int(prioritas) if (prioritas is not None and str(prioritas).strip() != "") else 3
        self.t_masuk = int(t_masuk) if (t_masuk is not None and str(t_masuk).strip() != "") else None
        self.t_selesai = int(t_selesai) if (t_selesai is not None and str(t_selesai).strip() != "") else None
        self.status = status

    @property
    def selesai_str(self):
        if self.t_selesai is None:
            return "-"
        h = self.t_selesai // 3600
        m = (self.t_selesai % 3600) // 60
        s = self.t_selesai % 60
        return f"{h:02d}:{m:02d}:{s:02d}"

    @property
    def masuk_str(self):
        if self.t_masuk is None:
            return "-"
        h = self.t_masuk // 3600
        m = (self.t_masuk % 3600) // 60
        s = self.t_masuk % 60
        return f"{h:02d}:{m:02d}:{s:02d}"

    @property
    def harga_str(self):
        return f"{self.harga:,}".replace(',', '.')

    def __repr__(self):
        return f"<Pesanan {self.oid} {self.harga} {self.selesai_str}>"


def parse_csv_line(line):
    """Mem-parse baris CSV tanpa library instan, mendukung nilai yang diapit tanda petik ganda."""
    fields = []
    curr = []
    in_quotes = False
    for char in line:
        if char == '"':
            in_quotes = not in_quotes
        elif char == ',' and not in_quotes:
            fields.append(''.join(curr).strip())
            curr = []
        else:
            curr.append(char)
    fields.append(''.join(curr).strip())
    return fields


def ambil_kunci(item, kunci):
    """
    Mengambil nilai kunci perbandingan dari item.
    Mendukung item berupa objek Pesanan maupun nilai primitif.
    """
    if isinstance(item, Pesanan):
        if kunci == 'oid':
            return item.oid
        elif kunci == 'harga':
            return item.harga
        elif kunci == 'selesai':
            # Jika t_selesai None (belum selesai/batal), letakkan di urutan paling belakang
            return item.t_selesai if item.t_selesai is not None else 999999999
        return item.oid
    # Jika item adalah tuple, list, atau primitif
    return item


def insertion_sort(A, kunci='harga'):
    """
    Insertion Sort bekerja di tempat dan STABIL: O(n^2).
    Syarat penggeseran memakai lebih besar (>), bukan lebih besar atau sama dengan (>=).
    Mengembalikan: (array_terurut, jumlah_perbandingan, jumlah_pemindahan)
    """
    n = len(A)
    # Buat salinan larik agar tidak mengubah larik asli
    hasil = [A[idx] for idx in range(n)]
    
    comps = 0
    moves = 0
    
    for i in range(1, n):
        key_item = hasil[i]
        key_val = ambil_kunci(key_item, kunci)
        j = i - 1
        
        # Bandingkan dan geser ke kanan jika elemen di kiri lebih besar (STABIL: >)
        while j >= 0:
            comps += 1
            if ambil_kunci(hasil[j], kunci) > key_val:
                hasil[j + 1] = hasil[j]
                moves += 1
                j -= 1
            else:
                break
                
        hasil[j + 1] = key_item
        moves += 1  # Penempatan key_item pada posisi akhir
        
    return hasil, comps, moves


def merge_sort(A, kunci='harga'):
    """
    Merge Sort membelah dan menggabungkan secara STABIL: O(n log n).
    Syarat penggabungan memakai <= agar elemen dari bagian kiri selalu didahulukan saat kuncinya sama.
    Mengembalikan: (array_terurut, jumlah_perbandingan, jumlah_pemindahan)
    """
    comps = 0
    moves = 0
    
    def sort_rec(arr):
        nonlocal comps, moves
        length = len(arr)
        if length <= 1:
            return arr
            
        mid = length // 2
        left = sort_rec(arr[:mid])
        right = sort_rec(arr[mid:])
        
        merged = [None] * length
        i = 0
        j = 0
        k = 0
        len_l = len(left)
        len_r = len(right)
        
        while i < len_l and j < len_r:
            comps += 1
            # STABIL: pakai <= agar elemen kiri didahulukan saat nilai kuncinya sama
            if ambil_kunci(left[i], kunci) <= ambil_kunci(right[j], kunci):
                merged[k] = left[i]
                moves += 1
                i += 1
            else:
                merged[k] = right[j]
                moves += 1
                j += 1
            k += 1
            
        while i < len_l:
            merged[k] = left[i]
            moves += 1
            i += 1
            k += 1
            
        while j < len_r:
            merged[k] = right[j]
            moves += 1
            j += 1
            k += 1
            
        return merged

    hasil = sort_rec([A[idx] for idx in range(len(A))])
    return hasil, comps, moves


def linear_search(A, target):
    """
    Linear Search: menelusuri elemen satu per satu dari indeks 0: O(n).
    Target dicocokkan dengan target (oid jika Pesanan).
    Mengembalikan: (indeks_ditemukan, jumlah_perbandingan)
    Jika tidak ditemukan, indeks bernilai -1.
    """
    comps = 0
    for idx in range(len(A)):
        comps += 1
        curr_val = A[idx].oid if isinstance(A[idx], Pesanan) else A[idx]
        if curr_val == target:
            return idx, comps
    return -1, comps


def binary_search(A, target):
    """
    Binary Search: mencari pada larik yang SUDAH TERURUT: O(log n).
    Kondisi perulangan: lo <= hi.
    Mengembalikan: (indeks_ditemukan, jumlah_perbandingan)
    Jika tidak ditemukan, indeks bernilai -1.
    """
    lo = 0
    hi = len(A) - 1
    comps = 0
    
    while lo <= hi:
        mid = (lo + hi) // 2
        comps += 1
        curr_val = A[mid].oid if isinstance(A[mid], Pesanan) else A[mid]
        
        if curr_val == target:
            return mid, comps
        elif curr_val < target:
            lo = mid + 1
        else:
            hi = mid - 1
            
    return -1, comps
