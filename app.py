import tkinter as tk
import sys
import os

# Menambahkan path backend dan frontend agar import berjalan mulus
base_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(base_dir, 'backend'))
sys.path.append(os.path.join(base_dir, 'frontend'))

try:
    import m1_pesanan
    from ui import AppUI
except ImportError as e:
    print(f"Error import module: {e}")
    sys.exit(1)

def main():
    root = tk.Tk()
    app = AppUI(root, m1_pesanan)
    root.mainloop()

if __name__ == "__main__":
    main()
