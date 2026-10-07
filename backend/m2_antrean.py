class Stack:
    """Tumpukan (stack) di atas Larik: push, pop, peek, kosong."""
    def __init__(self, capacity=10):
        self.capacity = capacity
        self.data = [None] * capacity
        self.top = -1
        
    def push(self, x):
        if self.top == self.capacity - 1:
            self._resize()
        self.top += 1
        self.data[self.top] = x
        
    def pop(self):
        if self.is_empty():
            return None
        x = self.data[self.top]
        self.data[self.top] = None
        self.top -= 1
        return x
        
    def peek(self):
        if self.is_empty():
            return None
        return self.data[self.top]
        
    def is_empty(self):
        return self.top == -1
        
    def clear(self):
        self.top = -1
        self.data = [None] * self.capacity
        
    def _resize(self):
        new_cap = self.capacity * 2
        new_data = [None] * new_cap
        for i in range(self.top + 1):
            new_data[i] = self.data[i]
        self.data = new_data
        self.capacity = new_cap


# --- PEMROSESAN STRUK KASIR ---

def tokenize(ekspresi):
    """Memecah string ekspresi menjadi array token."""
    tokens = []
    i = 0
    while i < len(ekspresi):
        if ekspresi[i].isspace():
            i += 1
        elif ekspresi[i].isdigit():
            num = ""
            while i < len(ekspresi) and ekspresi[i].isdigit():
                num += ekspresi[i]
                i += 1
            tokens.append(num)
        else:
            tokens.append(ekspresi[i])
            i += 1
    return tokens

def prioritas(op):
    """Menentukan tingkat prioritas operator."""
    if op in ('*', '/'): return 2
    if op in ('+', '-'): return 1
    return 0

def ke_postfix(ekspresi):
    """Mengubah struk infix menjadi postfix memakai stack operator."""
    tokens = tokenize(ekspresi)
    output = []
    s = Stack()
    
    for token in tokens:
        if token.isdigit():
            output.append(token)
        elif token == '(':
            s.push(token)
        elif token == ')':
            while not s.is_empty() and s.peek() != '(':
                output.append(s.pop())
            if not s.is_empty() and s.peek() == '(':
                s.pop() # buang '('
        else:
            while not s.is_empty() and prioritas(s.peek()) >= prioritas(token):
                output.append(s.pop())
            s.push(token)
            
    while not s.is_empty():
        output.append(s.pop())
        
    return output

def hitung(postfix):
    """Mengevaluasi postfix memakai stack angka, mengembalikan totalnya."""
    s = Stack()
    for token in postfix:
        if token.isdigit():
            s.push(int(token))
        else:
            b = s.pop()
            a = s.pop()
            if a is None or b is None:
                continue
            if token == '+': s.push(a + b)
            elif token == '-': s.push(a - b)
            elif token == '*': s.push(a * b)
            elif token == '/': s.push(a // b)
    return s.pop()


# --- ANTREAN NAIF & MELINGKAR ---

class AntreanNaif:
    """Antrean naif di atas larik biasa. Geser ke kiri setiap kali dequeue."""
    def __init__(self, capacity=10):
        self.capacity = capacity
        self.data = [None] * capacity
        self.size = 0
        self.geseran = 0 # Menyimpan jumlah geseran untuk statistik
        
    def enqueue(self, x):
        """Menempel di belakang."""
        if self.size == self.capacity:
            self._resize()
        self.data[self.size] = x
        self.size += 1
        
    def dequeue(self):
        """Mengambil indeks 0 dan menggeser seluruh sisa elemen."""
        if self.size == 0: return None
        x = self.data[0]
        for i in range(1, self.size):
            self.data[i-1] = self.data[i]
            self.geseran += 1 # 1 elemen digeser
        self.data[self.size - 1] = None
        self.size -= 1
        return x
        
    def dequeue_back(self):
        """Untuk undo enqueue: keluarkan dari belakang antrean."""
        if self.size == 0: return None
        x = self.data[self.size - 1]
        self.data[self.size - 1] = None
        self.size -= 1
        return x
        
    def enqueue_front(self, x):
        """Untuk undo dequeue: kembalikan isinya ke depan antrean."""
        if self.size == self.capacity:
            self._resize()
        # Geser ke kanan untuk memberi ruang di depan
        for i in range(self.size, 0, -1):
            self.data[i] = self.data[i-1]
            self.geseran += 1
        self.data[0] = x
        self.size += 1
        
    def _resize(self):
        new_cap = self.capacity * 2
        new_data = [None] * new_cap
        for i in range(self.size):
            new_data[i] = self.data[i]
        self.data = new_data
        self.capacity = new_cap


class AntreanMelingkar:
    """Antrean melingkar dengan data, front, rear, dan count."""
    def __init__(self, capacity=4): # Kapasitas awal kecil sesuai perintah (K=4)
        self.capacity = capacity
        self.data = [None] * capacity
        self.front = 0
        self.rear = 0
        self.count = 0
        self.geseran = 0 # circular queue = 0 geseran saat dequeue
        
    def enqueue(self, x):
        if self.count == self.capacity:
            self._resize()
        self.data[self.rear] = x
        self.rear = (self.rear + 1) % self.capacity
        self.count += 1
        
    def dequeue(self):
        if self.count == 0: return None
        x = self.data[self.front]
        self.data[self.front] = None
        self.front = (self.front + 1) % self.capacity
        self.count -= 1
        return x
        
    def dequeue_back(self):
        """Untuk undo enqueue: keluarkan lagi dari belakang antrean."""
        if self.count == 0: return None
        self.rear = (self.rear - 1) % self.capacity
        x = self.data[self.rear]
        self.data[self.rear] = None
        self.count -= 1
        return x
        
    def enqueue_front(self, x):
        """Untuk undo dequeue: kembalikan seluruh isinya ke depan antrean."""
        if self.count == self.capacity:
            self._resize()
        self.front = (self.front - 1) % self.capacity
        self.data[self.front] = x
        self.count += 1
        
    def _resize(self):
        new_cap = self.capacity * 2
        new_data = [None] * new_cap
        for i in range(self.count):
            new_data[i] = self.data[(self.front + i) % self.capacity]
        self.data = new_data
        self.front = 0
        self.rear = self.count
        self.capacity = new_cap
