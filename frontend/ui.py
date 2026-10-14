import tkinter as tk
from tkinter import ttk, messagebox
import time
import os

class AppUI:
    def __init__(self, root, backend_m1, backend_m2=None, backend_m3=None):
        self.root = root
        self.root.title("2EZ4U Food Delivery")
        self.root.geometry("1024x720")
        self.root.minsize(900, 600)
        
        # Simpan backend
        self.backend_m1 = backend_m1
        self.backend_m2 = backend_m2
        self.backend_m3 = backend_m3
        
        # Struktur data M1
        self.array_db = self.backend_m1.Array()
        self.ll_db = self.backend_m1.LinkList()
        
        # Struktur data M2
        if self.backend_m2:
            self.m2_queue_naif = self.backend_m2.AntreanNaif()
            self.m2_queue_circular = self.backend_m2.AntreanMelingkar()
            self.m2_undo_stack = self.backend_m2.Stack()
            self.m2_redo_stack = self.backend_m2.Stack()
            
        # Data M3 (List objek Pesanan)
        self.pesanan_list = []
        self.sorted_oid_cache = None
        self.oid_build_time_ms = 0.0

        self.current_menu = None
        self.setup_ui()
        
    def setup_ui(self):
        # 1. Top Header Banner
        self.header_frame = tk.Frame(self.root, bg="#1E3A8A", height=40)
        self.header_frame.pack(fill=tk.X, side=tk.TOP)
        self.lbl_app_title = tk.Label(
            self.header_frame, 
            text="2EZ4U Food Delivery", 
            font=("Segoe UI", 13, "bold"), 
            bg="#1E3A8A", 
            fg="white", 
            padx=15, 
            pady=8
        )
        self.lbl_app_title.pack(side=tk.LEFT)
        
        # 2. Main PanedWindow (Kiri: Menu Navigasi, Kanan: Form & Hasil)
        self.paned = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.paned.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)
        
        # =========================================================================
        # PANEL KIRI (SIDEBAR MENU)
        # =========================================================================
        self.left_frame = ttk.Frame(self.paned, width=280)
        self.paned.add(self.left_frame, weight=1)
        
        # Section DATA
        ttk.Label(self.left_frame, text="DATA", font=("Segoe UI", 9, "bold")).pack(anchor=tk.W, pady=(2, 2))
        self.btn_load = ttk.Button(self.left_frame, text="Load Data CSV", command=self.load_csv_data)
        self.btn_load.pack(fill=tk.X, pady=(0, 8))
        
        self.menu_items = [
            # M1
            ("HEADER", "M1 - DATA PESANAN"),
            ("ITEM", "ARRAY - LIHAT PESANAN"),
            ("ITEM", "ARRAY - TAMBAH PESANAN REGULER"),
            ("ITEM", "ARRAY - TAMBAH PESANAN PRIORITAS"),
            ("ITEM", "ARRAY - TAMBAH PESANAN VIP"),
            ("ITEM", "ARRAY - HAPUS PESANAN"),
            ("ITEM", "LINKEDLIST - LIHAT PESANAN"),
            ("ITEM", "LINKEDLIST - TAMBAH PESANAN REGULER"),
            ("ITEM", "LINKEDLIST - TAMBAH PESANAN PRIORITAS"),
            ("ITEM", "LINKEDLIST - TAMBAH PESANAN VIP"),
            ("ITEM", "LINKEDLIST - HAPUS PESANAN"),
            # M2
            ("HEADER", "M2 - STACK DAN QUEUE"),
            ("ITEM", "STACK - POSTFIX (MESIN KASIR)"),
            ("ITEM", "STACK - UNDO"),
            ("ITEM", "STACK - REDO"),
            ("ITEM", "QUEUE - ENQUEUE"),
            ("ITEM", "QUEUE - DEQUEUE NAIF"),
            ("ITEM", "QUEUE - DEQUEUE CIRCULAR"),
            # M3
            ("HEADER", "M3 - SORT DAN SEARCH"),
            ("ITEM", "SORT - INSERTION SORT"),
            ("ITEM", "SORT - MERGE SORT"),
            ("ITEM", "SEARCH - LINEAR SEARCH"),
            ("ITEM", "SEARCH - BINARY SEARCH")
        ]
        
        # Listbox Navigasi Menu
        self.listbox_frame = ttk.Frame(self.left_frame)
        self.listbox_frame.pack(fill=tk.BOTH, expand=True)
        
        self.menu_listbox = tk.Listbox(
            self.listbox_frame, 
            font=("Segoe UI", 9), 
            selectbackground="#0078D7", 
            activestyle="none",
            bd=1,
            relief=tk.SOLID
        )
        self.menu_scroll = ttk.Scrollbar(self.listbox_frame, orient=tk.VERTICAL, command=self.menu_listbox.yview)
        self.menu_listbox.configure(yscrollcommand=self.menu_scroll.set)
        
        self.menu_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.menu_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Populate menu
        for kind, text in self.menu_items:
            self.menu_listbox.insert(tk.END, text)
            if kind == "HEADER":
                # Warnai header agar menyerupai tampilan acuan
                idx = self.menu_listbox.size() - 1
                self.menu_listbox.itemconfig(idx, {'fg': '#4B5563', 'bg': '#F3F4F6'})
                
        self.menu_listbox.bind('<<ListboxSelect>>', self.on_menu_select)

        # =========================================================================
        # PANEL KANAN (KONTEN UTAMA: FORM, TABEL, COMMAND, CATATAN)
        # =========================================================================
        self.right_frame = ttk.Frame(self.paned)
        self.paned.add(self.right_frame, weight=4)
        
        # 1. Header Konten (Judul & Subjudul)
        self.content_header_frame = ttk.Frame(self.right_frame)
        self.content_header_frame.pack(fill=tk.X, padx=10, pady=(4, 6))
        
        self.lbl_title = ttk.Label(self.content_header_frame, text="Pilih menu di panel kiri", font=("Segoe UI", 12, "bold"))
        self.lbl_title.pack(anchor=tk.W)
        self.lbl_desc = ttk.Label(self.content_header_frame, text="", font=("Segoe UI", 9, "italic"), foreground="#4B5563")
        self.lbl_desc.pack(anchor=tk.W, pady=(2, 0))
        
        # 2. Form Parameter Container
        self.param_container = ttk.Frame(self.right_frame)
        self.param_container.pack(fill=tk.X, padx=10, pady=(0, 6))
        
        # 2a. Form Default (untuk M1 & M2)
        self.form_default = ttk.Frame(self.param_container)
        self.lbl_def_input = ttk.Label(self.form_default, text="Input:", font=("Segoe UI", 9))
        self.lbl_def_input.pack(side=tk.LEFT, padx=(0, 5))
        self.entry_def_input = ttk.Entry(self.form_default, width=45, font=("Segoe UI", 9))
        self.entry_def_input.pack(side=tk.LEFT, padx=(0, 8))
        self.btn_def_execute = ttk.Button(self.form_default, text="Eksekusi", command=self.execute_default_action)
        self.btn_def_execute.pack(side=tk.LEFT)
        
        # 2b. Form Sort (untuk M3 Insertion Sort & Merge Sort)
        self.form_sort = ttk.Frame(self.param_container)
        
        # Kolom 1: Jumlah baris
        col_sort_1 = ttk.Frame(self.form_sort)
        col_sort_1.pack(side=tk.LEFT, padx=(0, 20), anchor=tk.N)
        ttk.Label(col_sort_1, text="Jumlah baris diurutkan", font=("Segoe UI", 9, "bold")).pack(anchor=tk.W)
        self.entry_sort_n = ttk.Entry(col_sort_1, width=15, font=("Segoe UI", 9))
        self.entry_sort_n.insert(0, "10")
        self.entry_sort_n.pack(anchor=tk.W, pady=(2, 2))
        ttk.Label(col_sort_1, text="diambil dari awal data; coba 1.000 lalu 2.000 lalu 4.000", font=("Segoe UI", 8), foreground="#6B7280").pack(anchor=tk.W)
        
        # Kolom 2: Diurutkan menurut
        col_sort_2 = ttk.Frame(self.form_sort)
        col_sort_2.pack(side=tk.LEFT, padx=(0, 20), anchor=tk.N)
        ttk.Label(col_sort_2, text="Diurutkan menurut", font=("Segoe UI", 9, "bold")).pack(anchor=tk.W)
        self.combo_sort_key = ttk.Combobox(col_sort_2, values=["harga", "oid", "selesai"], state="readonly", width=15, font=("Segoe UI", 9))
        self.combo_sort_key.set("harga")
        self.combo_sort_key.pack(anchor=tk.W, pady=(2, 2))
        ttk.Label(col_sort_2, text="oid (teks), harga (angka), selesai (waktu selesai)", font=("Segoe UI", 8), foreground="#6B7280").pack(anchor=tk.W)
        
        # Kolom 3: Tombol URUTKAN
        col_sort_3 = ttk.Frame(self.form_sort)
        col_sort_3.pack(side=tk.LEFT, padx=(0, 10), pady=(16, 0), anchor=tk.N)
        self.btn_sort = tk.Button(
            col_sort_3, 
            text="URUTKAN", 
            font=("Segoe UI", 9, "bold"), 
            bg="#1E3A8A", 
            fg="white", 
            padx=16, 
            pady=4, 
            relief=tk.FLAT, 
            command=self.execute_sort
        )
        self.btn_sort.pack()

        # 2c. Form Search (untuk M3 Linear & Binary Search)
        self.form_search = ttk.Frame(self.param_container)
        col_srch_1 = ttk.Frame(self.form_search)
        col_srch_1.pack(side=tk.LEFT, padx=(0, 15), anchor=tk.N)
        ttk.Label(col_srch_1, text="Nomor pesanan (oid)", font=("Segoe UI", 9, "bold")).pack(anchor=tk.W)
        self.entry_search_oid = ttk.Entry(col_srch_1, width=22, font=("Segoe UI", 9))
        self.entry_search_oid.insert(0, "O-137442")
        self.entry_search_oid.pack(anchor=tk.W, pady=(2, 2))
        ttk.Label(col_srch_1, text="Format: O-000001 sampai O-200000", font=("Segoe UI", 8), foreground="#6B7280").pack(anchor=tk.W)
        
        col_srch_2 = ttk.Frame(self.form_search)
        col_srch_2.pack(side=tk.LEFT, padx=(0, 10), pady=(16, 0), anchor=tk.N)
        self.btn_search = tk.Button(
            col_srch_2, 
            text="CARI", 
            font=("Segoe UI", 9, "bold"), 
            bg="#1E3A8A", 
            fg="white", 
            padx=20, 
            pady=4, 
            relief=tk.FLAT, 
            command=self.execute_search
        )
        self.btn_search.pack()

        # 3. Hasil / Summary Label
        self.lbl_summary = ttk.Label(self.right_frame, text="", font=("Segoe UI", 9, "bold"))
        self.lbl_summary.pack(anchor=tk.W, padx=10, pady=(2, 4))
        
        # 4. View Area (Text Widget atau Table Treeview)
        self.view_container = ttk.Frame(self.right_frame)
        self.view_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 6))
        
        # 4a. Text Widget untuk M1 & M2
        self.txt_result = tk.Text(self.view_container, font=("Consolas", 9), state=tk.DISABLED, bd=1, relief=tk.SOLID)
        self.txt_scroll = ttk.Scrollbar(self.view_container, orient=tk.VERTICAL, command=self.txt_result.yview)
        self.txt_result.configure(yscrollcommand=self.txt_scroll.set)
        
        # 4b. Treeview Table untuk M3 Sort
        self.tree_sort_frame = ttk.Frame(self.view_container)
        self.tree_sort = ttk.Treeview(
            self.tree_sort_frame, 
            columns=("#", "oid", "harga", "selesai", "resto", "menu"), 
            show="headings", 
            selectmode="browse"
        )
        self.tree_sort.heading("#", text="#")
        self.tree_sort.heading("oid", text="oid")
        self.tree_sort.heading("harga", text="harga")
        self.tree_sort.heading("selesai", text="selesai")
        self.tree_sort.heading("resto", text="resto")
        self.tree_sort.heading("menu", text="menu")
        
        self.tree_sort.column("#", width=40, anchor=tk.CENTER)
        self.tree_sort.column("oid", width=90, anchor=tk.CENTER)
        self.tree_sort.column("harga", width=80, anchor=tk.E)
        self.tree_sort.column("selesai", width=80, anchor=tk.CENTER)
        self.tree_sort.column("resto", width=140, anchor=tk.W)
        self.tree_sort.column("menu", width=140, anchor=tk.W)
        
        self.sort_scroll_y = ttk.Scrollbar(self.tree_sort_frame, orient=tk.VERTICAL, command=self.tree_sort.yview)
        self.tree_sort.configure(yscrollcommand=self.sort_scroll_y.set)
        self.tree_sort.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.sort_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 4c. Treeview Table untuk M3 Search
        self.tree_search_frame = ttk.Frame(self.view_container)
        self.tree_search = ttk.Treeview(
            self.tree_search_frame, 
            columns=("kolom", "isi"), 
            show="headings", 
            selectmode="browse"
        )
        self.tree_search.heading("kolom", text="kolom")
        self.tree_search.heading("isi", text="isi")
        self.tree_search.column("kolom", width=150, anchor=tk.W)
        self.tree_search.column("isi", width=350, anchor=tk.W)
        self.tree_search.pack(fill=tk.BOTH, expand=True)

        # Standar awal: tampilkan txt_result
        self.txt_result.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.txt_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        # 5. Panel COMMAND Log
        self.log_container = ttk.Frame(self.right_frame)
        self.log_container.pack(fill=tk.X, padx=10, pady=(2, 4))
        
        ttk.Label(self.log_container, text="COMMAND", font=("Segoe UI", 8, "bold"), foreground="#4B5563").pack(anchor=tk.W)
        self.txt_log = tk.Text(self.log_container, height=4, font=("Consolas", 8), bg="#F8FAFC", bd=1, relief=tk.SOLID, state=tk.DISABLED)
        self.txt_log.pack(fill=tk.X, pady=(2, 2))
        
        # 6. Yellow Explanation Box (Kotak Catatan Kuning sesuai contoh)
        self.note_box = tk.Frame(self.right_frame, bg="#FEF9C3", bd=1, relief=tk.SOLID, padx=8, pady=6)
        self.note_box.pack(fill=tk.X, padx=10, pady=(2, 6))
        self.lbl_note = tk.Label(
            self.note_box, 
            text="", 
            font=("Segoe UI", 8), 
            bg="#FEF9C3", 
            fg="#854D0E", 
            wraplength=700, 
            justify=tk.LEFT
        )
        self.lbl_note.pack(anchor=tk.W)
        
        # 7. Bottom Status Bar
        self.status_bar_frame = tk.Frame(self.root, bg="#F1F5F9", height=26, bd=1, relief=tk.SOLID)
        self.status_bar_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        self.lbl_status_tag = tk.Label(
            self.status_bar_frame, 
            text="[2EZ4U APP Ready]", 
            font=("Consolas", 8, "bold"), 
            bg="#0F172A", 
            fg="white", 
            padx=8, 
            pady=2
        )
        self.lbl_status_tag.pack(side=tk.LEFT, padx=4, pady=2)

    # =========================================================================
    # EVENT HANDLING & MENU SELECTION
    # =========================================================================
    def on_menu_select(self, event):
        selection = self.menu_listbox.curselection()
        if not selection:
            return
            
        selected_text = self.menu_listbox.get(selection[0])
        # Abaikan klik pada Header
        for kind, text in self.menu_items:
            if text == selected_text and kind == "HEADER":
                return
                
        self.current_menu = selected_text
        self.lbl_summary.config(text="")
        
        # Sembunyikan semua frame form & view terlebih dahulu
        self.form_default.pack_forget()
        self.form_sort.pack_forget()
        self.form_search.pack_forget()
        self.txt_result.pack_forget()
        self.txt_scroll.pack_forget()
        self.tree_sort_frame.pack_forget()
        self.tree_search_frame.pack_forget()
        
        # Konfigurasi berdasarkan menu yang dipilih
        if "SORT - " in self.current_menu:
            self.form_sort.pack(fill=tk.X)
            self.tree_sort_frame.pack(fill=tk.BOTH, expand=True)
            
            if "INSERTION SORT" in self.current_menu:
                self.lbl_title.config(text="Sort: insertion sort, O(n²)")
                self.lbl_desc.config(text="Setiap elemen digeser mundur sampai menemukan tempatnya. Sederhana, tetapi kerjanya tumbuh kuadratik.")
                self.lbl_note.config(text="Setiap elemen digeser mundur sampai menemukan tempatnya, jadi biayanya tumbuh kuadratik: melipatduakan jumlah baris membuat kerjanya kira-kira empat kali lipat. Jalankan SORT - MERGE SORT pada jumlah dan kunci yang sama, lalu bandingkan angka perbandingannya.")
            else:
                self.lbl_title.config(text="Sort: merge sort, O(n log n)")
                self.lbl_desc.config(text="Larik dibelah dua terus-menerus, lalu potongan yang sudah terurut disatukan kembali.")
                self.lbl_note.config(text="Larik dibelah dua terus-menerus lalu potongan yang sudah terurut disatukan kembali. Kedalaman belahannya log n dan tiap lapis menyentuh n elemen, jadi O(n log n). Hasilnya sama persis dengan insertion sort karena keduanya stabil.")

        elif "SEARCH - " in self.current_menu:
            self.form_search.pack(fill=tk.X)
            self.tree_search_frame.pack(fill=tk.BOTH, expand=True)
            
            if "LINEAR SEARCH" in self.current_menu:
                self.lbl_title.config(text="Search: linear search, O(n)")
                self.lbl_desc.config(text="Memeriksa pesanan satu per satu dari depan. Tidak menuntut data terurut.")
                self.lbl_note.config(text="Data tidak perlu terurut, tetapi setiap pesanan diperiksa satu per satu dari depan. Kasus terburuk menyentuh seluruh 200.001 baris.")
            else:
                self.lbl_title.config(text="Search: binary search, O(log n)")
                self.lbl_desc.config(text="Membuang separuh sisa daftar pada setiap perbandingan. Menuntut daftar yang sudah terurut menurut oid.")
                self.lbl_note.config(text="Setiap perbandingan membuang separuh sisa daftar, jadi 200.001 baris habis dalam paling banyak 18 langkah. Syaratnya: daftar harus SUDAH terurut menurut kunci yang dicari; di sini terurut menurut oid.")
                
        else:
            # Menu M1 dan M2
            self.form_default.pack(fill=tk.X)
            self.txt_result.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            self.txt_scroll.pack(side=tk.RIGHT, fill=tk.Y)
            
            self.lbl_title.config(text=self.current_menu)
            self.entry_def_input.delete(0, tk.END)
            
            if "LIHAT" in self.current_menu or "HAPUS" in self.current_menu:
                self.lbl_desc.config(text="Masukkan indeks (contoh: 0, 1, 2) dari barisan pesanan.")
                self.lbl_def_input.config(text="Indeks:")
                self.lbl_note.config(text="Perhatikan perbandingan performa akses O(1) pada Array vs O(n) penelusuran simpul pada Linked List.")
            elif "STACK - POSTFIX" in self.current_menu:
                self.lbl_desc.config(text="Masukkan ekspresi infix, contoh: ( 3 * 12000 ) + ( 2 * 8500 ) - 5000")
                self.lbl_def_input.config(text="Ekspresi:")
                self.entry_def_input.insert(0, "( 3 * 12000 ) + ( 2 * 8500 ) - 5000")
                self.lbl_note.config(text="Mesin kasir mengubah infix ke postfix menggunakan Stack operator, lalu menghitung totalnya menggunakan Stack angka.")
            elif "UNDO" in self.current_menu or "REDO" in self.current_menu or "DEQUEUE" in self.current_menu:
                self.lbl_desc.config(text="Eksekusi aksi antrean/tumpukan.")
                self.lbl_def_input.config(text="-")
                self.entry_def_input.insert(0, "-")
                self.lbl_note.config(text="Queue naif menggeser semua elemen setiap dequeue, sedangkan queue melingkar hanya menggeser indeks (O(1)). Stack undo menyimpan riwayat aksi.")
            elif "ENQUEUE" in self.current_menu:
                self.lbl_desc.config(text="Masukkan data pesanan ke belakang antrean.")
                self.lbl_def_input.config(text="Data Pesanan:")
                self.lbl_note.config(text="Enqueue menambahkan elemen ke belakang kedua antrean sekaligus.")
            else:
                if "REGULER" in self.current_menu:
                    self.lbl_desc.config(text="Tambah di belakang barisan.")
                elif "PRIORITAS" in self.current_menu:
                    self.lbl_desc.config(text="Menyerobot ke tengah barisan.")
                elif "VIP" in self.current_menu:
                    self.lbl_desc.config(text="Langsung masuk ke urutan pertama.")
                self.lbl_def_input.config(text="Data Pesanan:")
                self.lbl_note.config(text="Penambahan VIP O(1) pada linked list vs O(n) geser pada array.")

    def log_command(self, command, target_ds, elapsed_ms):
        self.txt_log.config(state=tk.NORMAL)
        log_text = f"{command:<22} -> {target_ds:<22} {elapsed_ms:.2f} ms\n"
        self.txt_log.insert(tk.END, log_text)
        self.txt_log.see(tk.END)
        self.txt_log.config(state=tk.DISABLED)
        self.lbl_status_tag.config(text=f"[{target_ds}] {elapsed_ms:.2f} ms")

    # =========================================================================
    # LOAD CSV DATA
    # =========================================================================
    def load_csv_data(self):
        try:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            file_path = os.path.join(base_dir, 'data', 'pesanan.csv')
            
            if not os.path.exists(file_path):
                messagebox.showerror("Error", f"File pesanan.csv tidak ditemukan di {file_path}!")
                return
                
            start_load = time.perf_counter()
            self.pesanan_list = []
            
            with open(file_path, 'r', encoding='utf-8') as f:
                header = f.readline()
                for line in f:
                    line_str = line.strip()
                    if not line_str:
                        continue
                    # Parsing CSV
                    if self.backend_m3:
                        fields = self.backend_m3.parse_csv_line(line_str)
                    else:
                        fields = line_str.split(',')
                        
                    if len(fields) >= 9:
                        p = self.backend_m3.Pesanan(
                            fields[0], fields[1], fields[2], fields[3],
                            fields[4], fields[5], fields[6], fields[7], fields[8]
                        )
                        self.pesanan_list.append(p)
                        
                        # Populate M1 & M2
                        self.array_db.append(line_str)
                        self.ll_db.append(line_str)
                        if self.backend_m2 and fields[8] == 'ANTRE':
                            self.m2_queue_naif.enqueue(fields[0])
                            self.m2_queue_circular.enqueue(fields[0])
                            
            elapsed_ms = (time.perf_counter() - start_load) * 1000
            self.log_command(f"load {len(self.pesanan_list)} CSV", "System / Database", elapsed_ms)
            messagebox.showinfo("Sukses", f"Berhasil memuat {len(self.pesanan_list)} data dari pesanan.csv dalam {elapsed_ms:.2f} ms!")
            
        except Exception as e:
            messagebox.showerror("Error Load CSV", str(e))

    # =========================================================================
    # EKSEKUSI M3: SORT
    # =========================================================================
    def execute_sort(self):
        if not self.pesanan_list:
            messagebox.showwarning("Perhatian", "Data pesanan belum dimuat! Silakan klik 'Load Data CSV' terlebih dahulu.")
            return
            
        try:
            n = int(self.entry_sort_n.get().strip().replace('.', '').replace(',', ''))
        except ValueError:
            messagebox.showerror("Error", "Jumlah baris harus berupa angka!")
            return
            
        kunci = self.combo_sort_key.get().strip()
        data_to_sort = self.pesanan_list[:n]
        actual_n = len(data_to_sort)
        
        if "INSERTION SORT" in self.current_menu:
            # Sesuai aturan: batasan 20.000 baris untuk insertion sort
            if actual_n > 20000:
                self.lbl_summary.config(text="DITOLAK: batasnya 20.000 baris, pakai merge sort untuk data penuh")
                # Kosongkan tabel
                for item in self.tree_sort.get_children():
                    self.tree_sort.delete(item)
                return
                
            t0 = time.perf_counter()
            sorted_data, comps, moves = self.backend_m3.insertion_sort(data_to_sort, kunci=kunci)
            elapsed_ms = (time.perf_counter() - t0) * 1000
            cmd_name = "insertion_sort"
            mod_name = "M3 - insertion sort"
            
        else: # MERGE SORT
            t0 = time.perf_counter()
            sorted_data, comps, moves = self.backend_m3.merge_sort(data_to_sort, kunci=kunci)
            elapsed_ms = (time.perf_counter() - t0) * 1000
            cmd_name = "merge_sort"
            mod_name = "M3 - merge sort"
            
        self.log_command(cmd_name, mod_name, elapsed_ms)
        
        # Helper format ribuan
        def fmt(n):
            return f"{n:,}".replace(',', '.')

        # Update summary text
        summary_str = (
            f"{fmt(actual_n)} pesanan diurutkan menurut {kunci}.\n"
            f"{fmt(comps)} perbandingan, {fmt(moves)} pemindahan."
        )
        self.lbl_summary.config(text=summary_str)
        
        # Isi Treeview (dibatasi 100 baris pertama untuk kestabilan UI jika n sangat besar)
        for item in self.tree_sort.get_children():
            self.tree_sort.delete(item)
            
        display_limit = min(actual_n, 100)
        for idx in range(display_limit):
            p = sorted_data[idx]
            self.tree_sort.insert("", tk.END, values=(
                idx + 1,
                p.oid,
                p.harga_str,
                p.selesai_str,
                p.resto,
                p.menu
            ))

    # =========================================================================
    # EKSEKUSI M3: SEARCH
    # =========================================================================
    def execute_search(self):
        if not self.pesanan_list:
            messagebox.showwarning("Perhatian", "Data pesanan belum dimuat! Silakan klik 'Load Data CSV' terlebih dahulu.")
            return
            
        target_oid = self.entry_search_oid.get().strip()
        if not target_oid:
            messagebox.showwarning("Perhatian", "Masukkan nomor pesanan (oid) yang ingin dicari!")
            return
            
        for item in self.tree_search.get_children():
            self.tree_search.delete(item)
            
        def fmt(n):
            return f"{n:,}".replace(',', '.')

        if "LINEAR SEARCH" in self.current_menu:
            t0 = time.perf_counter()
            idx, comps = self.backend_m3.linear_search(self.pesanan_list, target_oid)
            elapsed_ms = (time.perf_counter() - t0) * 1000
            
            self.log_command("linear_search", "M3 - linear search", elapsed_ms)
            
            if idx != -1:
                p = self.pesanan_list[idx]
                summary = (
                    f"Ditemukan pada indeks {fmt(idx)}.\n"
                    f"{fmt(comps)} perbandingan."
                )
                self.lbl_summary.config(text=summary)
                self.display_pesanan_details(p)
            else:
                self.lbl_summary.config(text=f"Pesanan {target_oid} tidak ditemukan. ({fmt(comps)} perbandingan)")
                
        else: # BINARY SEARCH
            # Syarat: daftar harus SUDAH terurut menurut oid
            build_msg = ""
            if self.sorted_oid_cache is None:
                t_b0 = time.perf_counter()
                self.sorted_oid_cache, _, _ = self.backend_m3.merge_sort(self.pesanan_list, kunci='oid')
                self.oid_build_time_ms = (time.perf_counter() - t_b0) * 1000
                build_msg = f"Daftar terurut oid dibangun sekali dengan merge sort, {self.oid_build_time_ms:.2f} ms.\n"
            else:
                build_msg = f"Daftar terurut oid sudah siap (dibangun sekali dalam {self.oid_build_time_ms:.2f} ms).\n"
                
            t0 = time.perf_counter()
            idx, comps = self.backend_m3.binary_search(self.sorted_oid_cache, target_oid)
            elapsed_ms = (time.perf_counter() - t0) * 1000
            
            self.log_command("binary_search", "M3 - binary search", elapsed_ms)
            
            if idx != -1:
                p = self.sorted_oid_cache[idx]
                total_len = len(self.sorted_oid_cache)
                summary = (
                    f"{build_msg}"
                    f"Ditemukan pada baris ke-{fmt(idx + 1)} dari {fmt(total_len)} baris.\n"
                    f"{fmt(comps)} perbandingan, bandingkan dengan linear search."
                )
                self.lbl_summary.config(text=summary)
                self.display_pesanan_details(p)
            else:
                self.lbl_summary.config(text=f"{build_msg}Pesanan {target_oid} tidak ditemukan ({fmt(comps)} perbandingan).")

    def display_pesanan_details(self, p):
        details = [
            ("oid", p.oid),
            ("pelanggan", p.pelanggan),
            ("resto", p.resto),
            ("menu", p.menu),
            ("harga", p.harga_str),
            ("prioritas", p.prioritas),
            ("masuk", p.masuk_str),
            ("selesai", p.selesai_str),
            ("status", p.status)
        ]
        for col, val in details:
            self.tree_search.insert("", tk.END, values=(col, val))

    # =========================================================================
    # EKSEKUSI M1 & M2 (DEFAULT ACTIONS)
    # =========================================================================
    def execute_default_action(self):
        if not self.current_menu:
            messagebox.showwarning("Perhatian", "Pilih menu aksi terlebih dahulu di panel kiri!")
            return
            
        user_input = self.entry_def_input.get().strip()
        if not user_input:
            messagebox.showwarning("Perhatian", "Input data/indeks tidak boleh kosong!")
            return
            
        ds_type = "Array" if "ARRAY" in self.current_menu else "Linked List"
        db = self.array_db if ds_type == "Array" else self.ll_db
        
        command_log = ""
        result_msg = ""

        try:
            if "LIHAT" in self.current_menu or "HAPUS" in self.current_menu:
                idx = int(user_input)
            else:
                val = user_input
        except ValueError:
            messagebox.showerror("Error", "Indeks harus berupa angka integer!")
            return

        start_t = time.perf_counter()
        
        try:
            if "STACK" in self.current_menu or "QUEUE" in self.current_menu:
                ds_type = "M2 - " + self.current_menu.split("-")[0].strip()
                
                if "POSTFIX" in self.current_menu:
                    postfix = self.backend_m2.ke_postfix(val)
                    hasil = self.backend_m2.hitung(postfix)
                    command_log = f"hitung('{val}')"
                    result_msg = f"Infix: {val}\nPostfix: {' '.join(str(p) for p in postfix)}\nHasil (TOTAL): Rp {hasil:,}".replace(',', '.')
                    
                elif "ENQUEUE" in self.current_menu:
                    self.m2_queue_naif.enqueue(val)
                    self.m2_queue_circular.enqueue(val)
                    self.m2_undo_stack.push(("enqueue", val))
                    self.m2_redo_stack.clear()
                    command_log = f"enqueue('{val}')"
                    result_msg = f"Berhasil memasukkan '{val}' ke kedua antrean."
                    
                elif "DEQUEUE NAIF" in self.current_menu:
                    res = self.m2_queue_naif.dequeue()
                    command_log = "dequeue_naif()"
                    result_msg = f"Dequeue Naif melayani: '{res}'\nGeseran kali ini dilakukan."
                    
                elif "DEQUEUE CIRCULAR" in self.current_menu:
                    res = self.m2_queue_circular.dequeue()
                    self.m2_undo_stack.push(("dequeue", res))
                    self.m2_redo_stack.clear()
                    command_log = "dequeue_circular()"
                    result_msg = f"Dequeue Circular melayani: '{res}'\nTidak ada geseran."
                    
                elif "UNDO" in self.current_menu:
                    last_action = self.m2_undo_stack.pop()
                    if last_action is not None:
                        action, data = last_action
                        self.m2_redo_stack.push(last_action)
                        if action == "enqueue":
                            res1 = self.m2_queue_naif.dequeue_back()
                            res2 = self.m2_queue_circular.dequeue_back()
                            command_log = "stack_undo()"
                            result_msg = f"Undo enqueue: '{res1}' dikeluarkan dari belakang antrean."
                        elif action == "dequeue":
                            self.m2_queue_naif.enqueue_front(data)
                            self.m2_queue_circular.enqueue_front(data)
                            command_log = "stack_undo()"
                            result_msg = f"Undo dequeue: '{data}' dikembalikan ke depan antrean."
                    else:
                        command_log = "stack_undo()"
                        result_msg = "Tidak ada operasi yang bisa di-undo (stack kosong)."
                        
                elif "REDO" in self.current_menu:
                    next_action = self.m2_redo_stack.pop()
                    if next_action is not None:
                        action, data = next_action
                        self.m2_undo_stack.push(next_action)
                        if action == "enqueue":
                            self.m2_queue_naif.enqueue(data)
                            self.m2_queue_circular.enqueue(data)
                            command_log = "stack_redo()"
                            result_msg = f"Redo enqueue: '{data}' dimasukkan kembali ke antrean."
                        elif action == "dequeue":
                            res1 = self.m2_queue_naif.dequeue()
                            res2 = self.m2_queue_circular.dequeue()
                            command_log = "stack_redo()"
                            result_msg = f"Redo dequeue: melayani '{res1}' lagi."
                    else:
                        command_log = "stack_redo()"
                        result_msg = "Tidak ada operasi yang bisa di-redo (stack kosong)."
                        
            elif "LIHAT" in self.current_menu:
                res = db.get(idx)
                command_log = f"get({idx})"
                result_msg = f"Menemukan data: '{res}' di indeks {idx}" if res is not None else f"Data tidak ditemukan di indeks {idx}"
                
            elif "HAPUS" in self.current_menu:
                res = db.delete(idx)
                command_log = f"delete({idx})"
                result_msg = f"Menghapus data: '{res}' dari indeks {idx}" if res is not None else f"Gagal menghapus: Indeks {idx} di luar jangkauan"
                
            elif "TAMBAH" in self.current_menu:
                if "REGULER" in self.current_menu:
                    db.append(val)
                    command_log = f"append('{val}')"
                elif "PRIORITAS" in self.current_menu:
                    mid = db.size // 2
                    db.insert(mid, val)
                    command_log = f"insert({mid}, '{val}')"
                elif "VIP" in self.current_menu:
                    db.insert(0, val)
                    command_log = f"insert(0, '{val}')"
                result_msg = f"Berhasil menambahkan pesanan '{val}'"
                
        except Exception as e:
            messagebox.showerror("Error Execution", str(e))
            return
            
        end_t = time.perf_counter()
        elapsed_ms = (end_t - start_t) * 1000
        
        self.log_command(command_log, ds_type, elapsed_ms)
        self.show_default_result(result_msg, update_view=db.size <= 100 if hasattr(db, 'size') else True)

    def show_default_result(self, text, update_view=True):
        self.txt_result.config(state=tk.NORMAL)
        self.txt_result.delete("1.0", tk.END)
        self.txt_result.insert(tk.END, f"[INFO] {text}\n\n")
        
        if update_view:
            if "QUEUE" in self.current_menu or "STACK - UNDO" in self.current_menu or "STACK - REDO" in self.current_menu:
                self.txt_result.insert(tk.END, f"--- State Antrean Saat Ini ---\n")
                
                db_naif = self.m2_queue_naif
                self.txt_result.insert(tk.END, f"[Naif] Ukuran: {db_naif.size}, Geseran: {db_naif.geseran}\n")
                for i in range(min(db_naif.size, 50)):
                    self.txt_result.insert(tk.END, f"  [{i}] {db_naif.data[i]}\n")
                
                db_circ = self.m2_queue_circular
                self.txt_result.insert(tk.END, f"\n[Circular] Ukuran: {db_circ.count}, Geseran: {db_circ.geseran}\n")
                for i in range(min(db_circ.count, 50)):
                    idx = (db_circ.front + i) % db_circ.capacity
                    self.txt_result.insert(tk.END, f"  [{i}] {db_circ.data[idx]}\n")
                    
                self.txt_result.insert(tk.END, f"\n[Undo Stack] {self.m2_undo_stack.top + 1} item | [Redo Stack] {self.m2_redo_stack.top + 1} item\n")
            elif "STACK - POSTFIX" not in self.current_menu:
                ds_type = "Array" if "ARRAY" in self.current_menu else "Linked List"
                db = self.array_db if ds_type == "Array" else self.ll_db
                
                self.txt_result.insert(tk.END, f"--- State {ds_type} Saat Ini (Ukuran: {db.size}) ---\n")
                
                if ds_type == "Array":
                    for i in range(min(db.size, 50)):
                        self.txt_result.insert(tk.END, f"[{i}] {db.get(i)}\n")
                else:
                    curr = db.head
                    idx = 0
                    while curr and idx < 50:
                        self.txt_result.insert(tk.END, f"[{idx}] {curr.data}\n")
                        curr = curr.next
                        idx += 1
                        
        self.txt_result.config(state=tk.DISABLED)
