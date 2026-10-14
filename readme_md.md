# 2EZ4U APP - Struktur Data & Algoritma Backend

Repositori ini berisi implementasi backend murni berbasis struktur data dan algoritma untuk aplikasi **2EZ4U**, yang dibangun dari nol tanpa menggunakan fungsi bawaan Python (manual implementation constraint). Proyek ini dirancang untuk memenuhi studi kasus manajemen pesanan restoran dan kasir cerdas.

---

## 📂 Struktur Proyek & Modul

```text
projectstrukdat/
│
├── backend/
│   ├── m1_pesanan.py       # Milestone 1: Array Dinamis & Linked List
│   ├── m2_antrean.py       # Milestone 2: Stack, Infix-Postfix, & Queue (Naif & Melingkar)
│   └── m3_laporan.py       # Milestone 3: Sorting (Insertion/Merge) & Searching (Linear/Binary)
│
├── data/
│   └── pesanan.csv         # Sumber data simulasi pesanan restoran
│
├── frontend/
│   └── (Antarmuka GUI Tkinter / antarmuka pengguna)
│
├── app.py                  # Berkas utama untuk menjalankan aplikasi
└── README.md               # Dokumentasi proyek
```

---

## 🚀 Rincian Milestone & Implementasi Algoritma

### 1. Milestone 1 (M1) — Manajemen Data & Memori Dasar
* **Array Dinamis Manual:** Mengelola alokasi memori array secara manual dengan fitur otomatis pembesaran ukuran (*auto-resizing*) ketika kapasitas penuh tanpa bergantung pada fungsi bawaan tingkat tinggi.
* **Linked List:** Implementasi simpul (*node*) dan pointer penghubung untuk penambahan serta penghapusan data secara dinamis.

### 2. Milestone 2 (M2) — Stack, Mesin Kasir, & Antrean (Queue)
* **Stack (Tumpukan / LIFO):** Digunakan untuk evaluasi ekspresi matematika dan fitur *Undo/Redo* dengan prinsip *Last In, First Out*.
* **Konversi Infix ke Postfix & Kalkulator:** 
  * Menggunakan fungsi `tokenize()` untuk memecah string input.
  * Mengubah ekspresi matematika manusia (*infix*) ke format *postfix* (`ke_postfix`) menggunakan aturan prioritas operator (`+`, `-`, `*`, `/`).
  * Mengevaluasi hasil akhir rupiah secara efisien via fungsi `hitung()`.
* **Antrean Naif (`AntreanNaif`):** Antrean berbasis array biasa dengan kompleksitas $O(n)$ di mana setiap penghapusan data di depan mewajibkan pergeseran seluruh elemen belakang.
* **Antrean Melingkar (`AntreanMelingkar` / Circular Queue):** Implementasi antrean tingkat lanjut yang memanfaatkan operasi aritmatika modulo (`% capacity`) untuk mencapai efisiensi $O(1)$ tanpa perlu menggeser data fisik.

### 3. Milestone 3 (M3) — Sorting & Searching Berbasis Analitik
* **Insertion Sort:** Pengurutan data secara *in-place* dan stabil ($O(n^2)$) yang cocok untuk data kecil atau hampir terurut.
* **Merge Sort:** Algoritma *Divide and Conquer* berbasis rekursif ($O(n \log n)$) untuk pengurutan data dalam skala besar secara stabil.
* **Linear Search:** Pencarian data beruntun satu per satu dari awal indeks ($O(n)$).
* **Binary Search:** Pencarian kilat berbasis pembagian dua wilayah ($O(log n)$) pada data yang sudah terurut.
* **Metrik Analitik:** Dilengkapi pencatatan jumlah perbandingan (`comps`) dan pemindahan (`moves`) untuk mengukur performa efisiensi algoritma secara langsung.

---

## ⚙️ Cara Menjalankan Aplikasi

1. Pastikan Python sudah terinstal di komputer Anda.
2. Clone atau unduh repositori ini ke direktori lokal Anda:
   ```bash
   git clone https://github.com/rzcode07/projectstrukdat.git
   cd projectstrukdat
   ```
3. Jalankan aplikasi utama melalui terminal:
   ```bash
   python app.py
   ```

---
*Dikembangkan sebagai bagian dari pembelajaran Struktur Data dan Algoritma.*