# Proyek "2EZ4U APP" - Studi Kasus Proyek Akhir
**Struktur Data & Analisa Algoritma (EC234303)**  
Departemen Teknik Komputer, FTEIC - Institut Teknologi Sepuluh Nopember (ITS)  
Dosen: Ir. Arta Kusuma Hernanda, S.T., M.T.

---

## 1. Deskripsi Proyek
Proyek **2EZ4U APP** adalah implementasi *backend engine* layanan antar makanan/barang mini (serupa GoFood / ShopeeFood) menggunakan **Python 3.11+** dan antarmuka desktop **Tkinter**. Seluruh modul struktur data dan algoritma dibangun secara mandiri tanpa menggunakan *built-in function* terlarang (tanpa `dict`, `set`, `sorted()`, `.sort()`, `heapq`, `bisect`, `collections.*`, dsb).

---

## 2. Struktur Repositori
```text
setrukdat/
|-- README.md              <- Laporan teknis & analisis
|-- app.py                 <- Titik masuk aplikasi Tkinter
|-- data/
|   |-- pesanan.csv        <- 200.000 baris data pesanan
|   `-- peta.csv           <- Data node dan relasi graf lokasi
|-- backend/
|   |-- m1_pesanan.py      <- M1: Array Dinamis & Doubly/Singly Linked List (Head & Tail)
|   |-- m2_antrean.py      <- M2: Stack (Mesin Kasir Postfix + Undo/Redo) & Queue (Naif vs Melingkar)
|   `-- m3_pencarian.py    <- M3: Insertion Sort, Merge Sort, Linear Search, Binary Search
`-- frontend/
    `-- ui.py              <- Antarmuka Tkinter (Sidebar menu, Parameter Form, Treeview, Command Log)
```

---

## 3. Milestone 3: Sort & Search

### 3.1 Empat Algoritma Inti
1. **`insertion_sort(A, kunci)`**: 
   - Kompleksitas Waktu: $O(n^2)$ rata-rata & kasus terburuk, $O(n)$ kasus terbaik (hampir terurut).
   - Sifat: Bekerja di tempat (*in-place*) dan **STABIL** (menggunakan operator `>` saat penggeseran).
   - Pengaman: Menolak data berukuran lebih dari 20.000 baris untuk mencegah aplikasi membeku (*freeze*).
2. **`merge_sort(A, kunci)`**:
   - Kompleksitas Waktu: $O(n \log n)$ pada semua kasus (termasuk 200.000 baris penuh).
   - Sifat: **STABIL** (menggunakan operator `<=` pada tahap penggabungan sehingga elemen kiri didahulukan).
3. **`linear_search(A, target)`**:
   - Kompleksitas Waktu: $O(n)$ penelusuran sekuensial dari indeks 0.
   - Sifat: Tidak menuntut data terurut; cocok untuk pencarian acak sekali jalan.
4. **`binary_search(A, target)`**:
   - Kompleksitas Waktu: $O(\log n)$.
   - Syarat Mutlak: Memerlukan data yang sudah terurut menurut kunci pencarian (`oid`). Dibangun sekali menggunakan `merge_sort`.

---

### 3.2 Tabel Perbandingan Sort ($n$ vs Jumlah Perbandingan & Waktu)
Diuji pada dataset riil `pesanan.csv` dengan kunci pengurutan `harga`:

| $n$ (Jumlah Data) | Insertion Sort (Perbandingan) | Insertion Sort (Waktu ms) | Merge Sort (Perbandingan) | Merge Sort (Waktu ms) |
|---|---|---|---|---|
| **10** | 24 | 0.02 ms | 21 | 0.02 ms |
| **1.000** | 233.802 | 35.88 ms | 8.650 | 2.48 ms |
| **2.000** | 962.430 | 153.01 ms | 19.240 | 7.32 ms |
| **4.000** | 3.831.520 | 609.85 ms | 42.355 | 11.40 ms |
| **8.000** | 15.058.881 | 2.484.37 ms | 92.616 | 28.00 ms |
| **20.000** | 93.982.937 | 17.559.80 ms | 257.442 | 81.24 ms |
| **200.000** | **DITOLAK** (> 20.000) | - | 3.226.139 | 1.046.26 ms (~1,05 s) |

#### Analisis Grafik & Pertumbuhan Kompleksitas:
- **Insertion Sort ($O(n^2)$)**: Ketika ukuran data $n$ dilipatduakan dari 2.000 ke 4.000, jumlah perbandingan melonjak sekitar **4 kali lipat** ($962.430 \times 4 \approx 3.831.520$). Pada $n = 20.000$, jumlah operasi mencapai 93 juta perbandingan.
- **Merge Sort ($O(n \log n)$)**: Ketika $n$ dilipatduakan dari 2.000 ke 4.000, perbandingan hanya naik sekitar **2,2 kali lipat** ($19.240 \rightarrow 42.355$). Pada $n = 200.000$, Merge Sort mampu menyelesaikan pengurutan hanya dalam 3,2 juta perbandingan (~1 detik).

```text
Pertumbuhan Perbandingan:
Perbandingan
   ^
90M|                                     * (Insertion Sort: O(n^2))
   |                                    /
   |                                   /
40M|                                  /
   |                                 /
   |                                /
 3M|                              /  ----------------- * (Merge Sort: O(n log n))
   +--------------------------------------------------------> n
   0            4.000         8.000           20.000       200.000
```

---

### 3.3 Tabel Perbandingan Pencarian (Linear Search vs Binary Search)
Diuji untuk mencari pesanan dengan `oid = "O-199999"` pada 200.000 data:

| Algoritma | Waktu Setup / Bangun Indeks | Baris Ditemukan | Jumlah Perbandingan | Waktu Cari |
|---|---|---|---|---|
| **Linear Search** | 0.00 ms (Langsung cari) | 199.999 (Indeks 199.998) | 199.999 | 13.26 ms |
| **Binary Search** | 640.43 ms (Merge Sort `oid`) | 199.999 (Indeks 199.998) | **17** | **0.02 ms** |

> **Kesimpulan Search**: Linear Search unggul jika pencarian hanya dilakukan satu atau dua kali (karena tidak butuh *overhead* pengurutan awal). Namun, jika pencarian dilakukan berkali-kali pada aplikasi dengan trafik tinggi, Binary Search memberikan efisiensi eksponensial (hanya butuh 17-18 langkah untuk 200.000 data).

---

### 3.4 Alasan Pemilihan Algoritma
1. **Insertion Sort**: Dipilih untuk data kecil ($n \le 50$) atau data yang sudah hampir terurut (misalnya penambahan berkala pada laporan harian). Algoritma ini hemat memori karena bekerja *in-place* tanpa alokasi larik baru.
2. **Merge Sort**: Dipilih untuk memproses seluruh data database (200.000 baris) karena memiliki jaminan performa $O(n \log n)$ yang tidak terpengaruh oleh susunan awal data (acak, terbalik, maupun duplikat), serta mempertahankan urutan kronologis data yang memiliki nilai kunci kembar (*stable sort*).
3. **Linear Search**: Dipilih saat data belum terurut atau ketika operasi pencarian bersifat sesekali (*ad-hoc*).
4. **Binary Search**: Dipilih untuk pencarian pesanan rutin berdasarkan ID unik (`oid`). Setelah tabel diurutkan sekali di awal, setiap pencarian berikutnya berjalan instan ($O(\log n)$).

---

## 4. Cara Menjalankan Aplikasi
1. Buka terminal pada direktori `C:\CODE\setrukdat`.
2. Jalankan aplikasi:
   ```powershell
   python app.py
   ```
3. Klik tombol **Load Data CSV** pada pojok kiri atas untuk memuat 200.000 data dari `data/pesanan.csv`.
4. Pilih menu di sidebar kiri:
   - **M1**: Penambahan & Penghapusan Pesanan (Array vs Linked List).
   - **M2**: Mesin Kasir Postfix, Undo, Redo, Dequeue Naif vs Melingkar.
   - **M3**: Pengujian Sorting (Insertion Sort vs Merge Sort) & Pencarian (Linear vs Binary Search).
