import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
from PIL import Image, ImageTk
import fitz  # PyMuPDF
import io

__version__ = "0.2.1"

class MyTinyDesk:
    def __init__(self, root):
        self.root = root
        self.root.title(f"myTinyDesk v{__version__}")
        self.root.geometry("900x700")
        
        self.pdf_document = None
        self.current_page = 0
        self.total_pages = 0
        self.zoom_level = 1.0
        
        self.setup_ui()
    
    def setup_ui(self):
        # Top Frame - Toolbar
        toolbar = tk.Frame(self.root, bg="#2c3e50", height=50)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        
        # Buttons im Toolbar
        ttk.Button(toolbar, text="📂 Öffnen", command=self.open_pdf).pack(side=tk.LEFT, padx=5, pady=5)
        
        ttk.Button(toolbar, text="◀ Zurück", command=self.previous_page).pack(side=tk.LEFT, padx=2, pady=5)
        
        # Seiteneingabe-Feld
        self.page_entry = tk.Entry(toolbar, width=5, font=("Arial", 10))
        self.page_entry.pack(side=tk.LEFT, padx=2, pady=5)
        self.page_entry.bind('<Return>', self.goto_page)
        
        self.page_label = tk.Label(toolbar, text="/ -", bg="#2c3e50", fg="white", font=("Arial", 10))
        self.page_label.pack(side=tk.LEFT, padx=2)
        
        ttk.Button(toolbar, text="Vor ▶", command=self.next_page).pack(side=tk.LEFT, padx=2, pady=5)
        
        tk.Label(toolbar, text="|", bg="#2c3e50", fg="white").pack(side=tk.LEFT, padx=5)
        
        ttk.Button(toolbar, text="🔍+", command=self.zoom_in).pack(side=tk.LEFT, padx=2, pady=5)
        ttk.Button(toolbar, text="🔍-", command=self.zoom_out).pack(side=tk.LEFT, padx=2, pady=5)
        
        self.zoom_label = tk.Label(toolbar, text="100%", bg="#2c3e50", fg="white", font=("Arial", 10))
        self.zoom_label.pack(side=tk.LEFT, padx=10)
        
        # Main Frame mit Scrollbar
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Canvas für PDF-Anzeige
        self.canvas = tk.Canvas(main_frame, bg="#34495e")
        
        # Scrollbars
        v_scrollbar = tk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        h_scrollbar = tk.Scrollbar(main_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        
        self.canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Status Bar
        self.status_bar = tk.Label(self.root, text="Bereit | myTinyDesk", relief=tk.SUNKEN, anchor=tk.W, bg="#ecf0f1")
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Keyboard Shortcuts
        self.root.bind('<Left>', lambda e: self.previous_page())
        self.root.bind('<Right>', lambda e: self.next_page())
        self.root.bind('<Prior>', lambda e: self.previous_page())  # Page Up
        self.root.bind('<Next>', lambda e: self.next_page())  # Page Down
        self.root.bind('<plus>', lambda e: self.zoom_in())
        self.root.bind('<minus>', lambda e: self.zoom_out())
    
    def open_pdf(self):
        pdf_path = filedialog.askopenfilename(
            title="PDF-Datei öffnen",
            filetypes=[("PDF Dateien", "*.pdf"), ("Alle Dateien", "*.*")]
        )
        
        if not pdf_path:
            return
        
        try:
            # Altes PDF schließen
            if self.pdf_document:
                self.pdf_document.close()
            
            # Neues PDF laden
            self.pdf_document = fitz.open(pdf_path)
            self.total_pages = len(self.pdf_document)
            self.current_page = 0
            self.zoom_level = 1.0
            
            file_name = Path(pdf_path).name
            self.root.title(f"myTinyDesk - {file_name}")
            self.status_bar.config(text=f"✓ Geladen: {file_name} | {self.total_pages} Seiten")
            
            self.render_page()
            
        except Exception as e:
            messagebox.showerror("Fehler", f"Konnte PDF nicht öffnen:\n{str(e)}")
            self.status_bar.config(text="✗ Fehler beim Laden")
    
    def render_page(self):
        if not self.pdf_document:
            return
        
        try:
            # Aktuelle Seite laden
            page = self.pdf_document[self.current_page]
            
            # Mit Zoom rendern
            mat = fitz.Matrix(self.zoom_level, self.zoom_level)
            pix = page.get_pixmap(matrix=mat, alpha=False)
            
            # In PIL Image konvertieren
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            
            # In Tkinter PhotoImage konvertieren
            self.photo = ImageTk.PhotoImage(img)
            
            # Canvas aktualisieren
            self.canvas.delete("all")
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)
            self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))
            
            # Labels aktualisieren
            self.page_label.config(text=f"/ {self.total_pages}")
            self.page_entry.delete(0, tk.END)
            self.page_entry.insert(0, str(self.current_page + 1))
            self.zoom_label.config(text=f"{int(self.zoom_level * 100)}%")
            
        except Exception as e:
            messagebox.showerror("Fehler", f"Konnte Seite nicht rendern:\n{str(e)}")
    
    def next_page(self):
        if self.pdf_document and self.current_page < self.total_pages - 1:
            self.current_page += 1
            self.render_page()
    
    def previous_page(self):
        if self.pdf_document and self.current_page > 0:
            self.current_page -= 1
            self.render_page()
    
    def goto_page(self, event=None):
        if not self.pdf_document:
            return
        
        try:
            page_num = int(self.page_entry.get())
            if 1 <= page_num <= self.total_pages:
                self.current_page = page_num - 1
                self.render_page()
            else:
                messagebox.showwarning("Ungültige Seitennummer", 
                                      f"Bitte eine Zahl zwischen 1 und {self.total_pages} eingeben.")
        except ValueError:
            messagebox.showwarning("Ungültige Eingabe", "Bitte eine gültige Seitennummer eingeben.")
    
    def zoom_in(self):
        if self.pdf_document and self.zoom_level < 3.0:
            self.zoom_level += 0.2
            self.render_page()
    
    def zoom_out(self):
        if self.pdf_document and self.zoom_level > 0.4:
            self.zoom_level -= 0.2
            self.render_page()
    
    def __del__(self):
        if self.pdf_document:
            self.pdf_document.close()

# Hauptfenster erstellen
if __name__ == "__main__":
    root = tk.Tk()
    app = MyTinyDesk(root)
    root.mainloop()
