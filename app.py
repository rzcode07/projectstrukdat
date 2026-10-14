import tkinter as tk
import sys
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(base_dir, 'backend'))
sys.path.append(os.path.join(base_dir, 'frontend'))

try:
    import m1_pesanan
    import m2_antrean
    import m3_pencarian
    from ui import AppUI
except ImportError as e:
    print(f"Error import module: {e}")
    sys.exit(1)

def main():
    root = tk.Tk()
    app = AppUI(root, m1_pesanan, m2_antrean, m3_pencarian)
    root.mainloop()

if __name__ == "__main__":
    main()
