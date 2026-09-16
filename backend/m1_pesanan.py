class Array:
    """
    Struktur data Array dengan alokasi memori manual menggunakan list primitif Python.
    Kapasitas awal adalah 4, dan akan digandakan ketika penuh.
    """
    def __init__(self, capacity=4):
        self.capacity = capacity
        self.size = 0
        # Inisialisasi sepetak memori dengan ukuran tetap
        self.data = [None] * self.capacity

    def _resize(self):
        """Menggandakan kapasitas array ketika penuh (Amortized O(1))."""
        self.capacity *= 2
        new_data = [None] * self.capacity
        # Salin seluruh isi array ke memori baru
        for i in range(self.size):
            new_data[i] = self.data[i]
        self.data = new_data

    def get(self, i):
        """Lihat pesanan ke-i (O(1))."""
        if 0 <= i < self.size:
            return self.data[i]
        return None

    def append(self, v):
        """Tambah REGULER: masuk barisan paling belakang (Amortized O(1))."""
        if self.size == self.capacity:
            self._resize()
        self.data[self.size] = v
        self.size += 1

    def insert(self, i, v):
        """
        Sisipkan pada index ke-i (O(n)).
        Digunakan untuk Tambah PRIORITAS (tengah) dan VIP (depan).
        """
        if i < 0 or i > self.size:
            return
        if self.size == self.capacity:
            self._resize()
        
        # Geser elemen ke kanan untuk memberi ruang kosong
        for j in range(self.size, i, -1):
            self.data[j] = self.data[j-1]
            
        self.data[i] = v
        self.size += 1

    def delete(self, i):
        """Hapus pesanan ke-i (O(n))."""
        if 0 <= i < self.size:
            removed = self.data[i]
            # Geser elemen ke kiri untuk menutupi ruang yang dihapus
            for j in range(i, self.size - 1):
                self.data[j] = self.data[j+1]
            self.data[self.size - 1] = None
            self.size -= 1
            return removed
        return None


class Node:
    """Simpul untuk Linked List."""
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkList:
    """
    Struktur data Linked List dengan penunjuk head dan tail.
    Tail digunakan agar operasi append (Tambah Reguler) bisa berjalan O(1).
    """
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def get(self, i):
        """Lihat pesanan ke-i (O(n))."""
        if i < 0 or i >= self.size:
            return None
        current = self.head
        for _ in range(i):
            current = current.next
        return current.data

    def append(self, v):
        """Tambah REGULER: masuk barisan paling belakang (O(1))."""
        new_node = Node(v)
        if self.size == 0:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        self.size += 1

    def insert(self, i, v):
        """
        Sisipkan pada index ke-i (O(n) telusur, O(1) sisip).
        Digunakan untuk Tambah PRIORITAS (tengah) dan VIP (depan).
        Tambah VIP ke index 0 akan memakan waktu O(1).
        """
        if i < 0 or i > self.size:
            return
            
        new_node = Node(v)
        if i == 0:  # Tambah VIP
            new_node.next = self.head
            self.head = new_node
            if self.size == 0:
                self.tail = new_node
        else:
            current = self.head
            # Telusuri sampai simpul sebelum posisi sisipan
            for _ in range(i - 1):
                current = current.next
            
            new_node.next = current.next
            current.next = new_node
            
            # Jika disisipkan di posisi paling belakang, perbarui tail
            if new_node.next is None:
                self.tail = new_node
                
        self.size += 1

    def delete(self, i):
        """Hapus pesanan ke-i (O(n) telusur, O(1) hapus)."""
        if i < 0 or i >= self.size:
            return None
            
        if i == 0:
            removed = self.head.data
            self.head = self.head.next
            if self.head is None:
                self.tail = None
            self.size -= 1
            return removed
            
        current = self.head
        for _ in range(i - 1):
            current = current.next
            
        removed = current.next.data
        current.next = current.next.next
        
        # Jika yang dihapus adalah elemen terakhir, perbarui tail
        if current.next is None:
            self.tail = current
            
        self.size -= 1
        return removed
