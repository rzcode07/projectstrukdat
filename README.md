2EZ4U APP - Struktur Data & Algoritma Backend
---
Repositori ini berisi implementasi backend struktur data dan algoritma untuk aplikasi 2EZ4U. 
Proyek ini dibuat untuk memecahkan studi kasus manajemen pesanan restoran dan kasir cerdas.

Struktur Proyek & Modul
```text
projectstrukdat/
│
├── backend/
│   ├── m1_pesanan.py       # Milestone 1: Array & Linked List
│   ├── m2_antrean.py       # Milestone 2: Stack, Infix-Postfix, & Queue (Naif & Melingkar)
│   └── m3_laporan.py       # Milestone 3: Sort (Insertion/Merge) & Search (Linear/Binary)
│
├── data/
│   └── pesanan.csv         # Data pesanan
│
├── frontend/
│   └── (UI menggunakan TKinter)
│
├── app.py                  # aplikasi utama
└── README.md               # penjelasan
```
---
Penjelasan Milestone (1,2,3) & Algoritma
1. Milestone 1 (M1) — Manajemen Data & Memori Dasar
Array : Mengelola alokasi memori array secara manual dengan fitur otomatis pembesaran ukuran (auto-resizing) ketika kapasitas penuh tanpa bergantung pada fungsi bawaan tingkat tinggi.
Linked List: Implementasi simpul (node) dan pointer penghubung untuk penambahan serta penghapusan data secara dinamis.
2. Milestone 2 (M2) — Stack, Mesin Kasir, & Antrean
Stack (Tumpukan / LIFO): Digunakan untuk evaluasi ekspresi matematika dan fitur Undo/Redo dengan prinsip Last In, First Out.
Konversi Infix ke Postfix & Kalkulator:
Menggunakan fungsi `tokenize()` untuk memecah string input.
Mengubah ekspresi matematika manusia (infix) ke format postfix (`ke_postfix`) menggunakan aturan prioritas operator (`+`, `-`, `*`, `/`).
Mengevaluasi hasil akhir rupiah secara efisien via fungsi `hitung()`.
Antrean Naif (`AntreanNaif`): Antrean berbasis array biasa dengan kompleksitas $O(n)$ di mana setiap penghapusan data di depan mewajibkan pergeseran seluruh elemen belakang.
Antrean Melingkar (`AntreanMelingkar` / Circular Queue): Implementasi antrean tingkat lanjut yang memanfaatkan operasi aritmatika modulo (`% capacity`) untuk mencapai efisiensi $O(1)$ tanpa perlu menggeser data fisik.
3. Milestone 3 (M3) — Sorting & Searching
Insertion Sort: Pengurutan data secara in-place dan stabil ($O(n^2)$) yang cocok untuk data kecil atau hampir terurut.
Merge Sort: Algoritma Divide and Conquer berbasis rekursif ($O(n \log n)$) untuk pengurutan data dalam skala besar secara stabil.
Linear Search: Pencarian data beruntun satu per satu dari awal indeks ($O(n)$).
Binary Search: Pencarian kilat berbasis pembagian dua wilayah ($O(log n)$) pada data yang sudah terurut.
Metrik Analitik: Dilengkapi pencatatan jumlah perbandingan (`comps`) dan pemindahan (`moves`) untuk mengukur performa efisiensi algoritma secara langsung.
---
Cara Menjalankan Aplikasi
Gunakan Python.
Download atau clone repositori ini ke file lokal Anda:
```bash
   git clone https://github.com/rzcode07/projectstrukdat.git
   cd projectstrukdat
   ```
Jalankan aplikasi utama melalui terminal:
```bash
   python app.py
   ```
---
