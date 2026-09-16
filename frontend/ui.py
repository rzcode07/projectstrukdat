import tkinter as tk
from tkinter import ttk, messagebox
import time

class AppUI:
    def __init__(self, root, backend_m1):
        self.root = root
        self.root.title("2EZ4U Food Delivery")
        self.root.geometry("900x600")
        
        self.backend_m1 = backend_m1
        self.array_db = self.backend_m1.Array()
        self.ll_db = self.backend_m1.LinkList()
        
        self.setup_ui()
        
    def setup_ui(self):
        self.paned = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.paned.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.left_frame = ttk.Frame(self.paned)
        self.paned.add(self.left_frame, weight=1)
        
        ttk.Label(self.left_frame, text="DATA", font=("Segoe UI", 10, "bold")).pack(anchor=tk.W)
        self.btn_load = ttk.Button(self.left_frame, text="Load Data", state=tk.DISABLED) # Akan dipakai nanti untuk M2 dst (load CSV)
        self.btn_load.pack(fill=tk.X, pady=5)
        
        ttk.Label(self.left_frame, text="M1 - DATA PESANAN", font=("Segoe UI", 10, "bold")).pack(anchor=tk.W, pady=(10, 5))
        
        self.menus = [
            "ARRAY - LIHAT PESANAN",
            "ARRAY - TAMBAH PESANAN REGULER",
            "ARRAY - TAMBAH PESANAN PRIORITAS",
            "ARRAY - TAMBAH PESANAN VIP",
            "ARRAY - HAPUS PESANAN",
            "LINKEDLIST - LIHAT PESANAN",
            "LINKEDLIST - TAMBAH PESANAN REGULER",
            "LINKEDLIST - TAMBAH PESANAN PRIORITAS",
            "LINKEDLIST - TAMBAH PESANAN VIP",
            "LINKEDLIST - HAPUS PESANAN"
        ]

        self.menu_listbox = tk.Listbox(self.left_frame, font=("Segoe UI", 9), selectbackground="#0078D7")
        for menu in self.menus:
            self.menu_listbox.insert(tk.END, menu)
        self.menu_listbox.pack(fill=tk.BOTH, expand=True)
        self.menu_listbox.bind('<<ListboxSelect>>', self.on_menu_select)

        self.right_frame = ttk.Frame(self.paned)
        self.paned.add(self.right_frame, weight=3)

        self.form_frame = ttk.LabelFrame(self.right_frame, text="Form Parameter")
        self.form_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.lbl_title = ttk.Label(self.form_frame, text="Pilih menu di kiri", font=("Segoe UI", 10, "bold"))
        self.lbl_title.pack(anchor=tk.W, padx=10, pady=(5, 0))
        
        self.lbl_desc = ttk.Label(self.form_frame, text="", font=("Segoe UI", 9, "italic"))
        self.lbl_desc.pack(anchor=tk.W, padx=10)
        
        self.input_frame = ttk.Frame(self.form_frame)
        self.input_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.lbl_input = ttk.Label(self.input_frame, text="Data:")
        self.lbl_input.pack(side=tk.LEFT)
        self.entry_input = ttk.Entry(self.input_frame, width=50)
        self.entry_input.pack(side=tk.LEFT, padx=5)
        
        self.btn_execute = ttk.Button(self.input_frame, text="Eksekusi", command=self.execute_action)
        self.btn_execute.pack(side=tk.LEFT, padx=5)

        self.result_frame = ttk.LabelFrame(self.right_frame, text="Hasil / View")
        self.result_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.txt_result = tk.Text(self.result_frame, font=("Consolas", 10), state=tk.DISABLED)
        self.txt_result.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.log_frame = ttk.LabelFrame(self.right_frame, text="COMMAND LOG (Mencatat Waktu Eksekusi)")
        self.log_frame.pack(fill=tk.X)
        
        self.txt_log = tk.Text(self.log_frame, height=6, font=("Consolas", 9), bg="#F0F0F0", state=tk.DISABLED)
        self.txt_log.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.current_menu = None

    def on_menu_select(self, event):
        selection = self.menu_listbox.curselection()
        if not selection:
            return
            
        self.current_menu = self.menu_listbox.get(selection[0])
        self.lbl_title.config(text=self.current_menu)
        
        self.entry_input.delete(0, tk.END)
        
        if "LIHAT" in self.current_menu or "HAPUS" in self.current_menu:
            self.lbl_desc.config(text="Masukkan indeks (contoh: 0, 1, 2) dari barisan pesanan.")
            self.lbl_input.config(text="Indeks:")
        else:
            if "REGULER" in self.current_menu:
                self.lbl_desc.config(text="Tambah di belakang barisan.")
            elif "PRIORITAS" in self.current_menu:
                self.lbl_desc.config(text="Menyerobot ke tengah barisan.")
            elif "VIP" in self.current_menu:
                self.lbl_desc.config(text="Langsung masuk ke urutan pertama.")
            self.lbl_input.config(text="Data Pesanan:")

    def log_command(self, command, target_ds, elapsed_ms):
        self.txt_log.config(state=tk.NORMAL)
        log_text = f"{'COMMAND':<10} -> {target_ds:<12} | {command:<25} | {elapsed_ms:.4f} ms\n"
        self.txt_log.insert(tk.END, log_text)
        self.txt_log.see(tk.END)
        self.txt_log.config(state=tk.DISABLED)

    def show_result(self, text, update_view=True):
        self.txt_result.config(state=tk.NORMAL)
        self.txt_result.delete("1.0", tk.END)
        self.txt_result.insert(tk.END, f"[INFO] {text}\n\n")
        
        if update_view:
            ds_type = "Array" if "ARRAY" in self.current_menu else "Linked List"
            db = self.array_db if ds_type == "Array" else self.ll_db
            
            self.txt_result.insert(tk.END, f"--- State {ds_type} Saat Ini (Ukuran: {db.size}) ---\n")
            
            if ds_type == "Array":
                for i in range(db.size):
                    self.txt_result.insert(tk.END, f"[{i}] {db.get(i)}\n")
            else:
                curr = db.head
                idx = 0
                while curr:
                    self.txt_result.insert(tk.END, f"[{idx}] {curr.data}\n")
                    curr = curr.next
                    idx += 1
                    
        self.txt_result.config(state=tk.DISABLED)

    def execute_action(self):
        if not self.current_menu:
            messagebox.showwarning("Perhatian", "Pilih menu aksi terlebih dahulu di panel kiri!")
            return
            
        user_input = self.entry_input.get().strip()
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
            if "LIHAT" in self.current_menu:
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

        self.show_result(result_msg, update_view=db.size <= 100)
