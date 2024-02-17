import tkinter as tk
from tkinter import filedialog
from tkinter.font import *
from tkinter.messagebox import *
from tkinter.filedialog import *

class ai:
    def __init__(self, master):
        self.ai_window = master
        self.ai_window.title("ASK AI")

class Notepad(ai):
    def __init__(self, root):
        self.root = root
        self.root.title("Untitled - Notepad")

        self.text = tk.Text(self.root)
        self.text.pack(expand=True, fill='both')

        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)

        self.file_menu = tk.Menu(self.menu, tearoff=False)
        self.menu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="New", command=self.new_file)
        self.file_menu.add_command(label="Open", command=self.open_file)
        self.file_menu.add_command(label="Save", command=self.save_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.exit_app)

        self.edit_menu = tk.Menu(self.menu, tearoff=False)
        self.menu.add_cascade(label="Edit", menu=self.edit_menu)
        self.edit_menu.add_command(label="Cut", command=self.cut)
        self.edit_menu.add_command(label="Copy", command=self.copy)
        self.edit_menu.add_command(label="Paste", command=self.paste)

        self.format_menu = tk.Menu(self.menu, tearoff=False)
        self.menu.add_cascade(label="Format", menu=self.format_menu)
        self.format_menu.add_command(label="Font", command=self.font)

        self.help_menu = tk.Menu(self.menu, tearoff=False)
        self.menu.add_cascade(label="Help", menu=self.help_menu)
        self.help_menu.add_command(label="About", command=self.about)

    def new_file(self):
        self.root.title("Untitled - Notepad")
        self.text.delete(1.0, 'end')

    def open_file(self):
        file = filedialog.askopenfilename(defaultextension=".txt",filetypes=[("All Files", "*.*"),("Text Files", "*.txt")])
        if file:
            self.root.title(os.path.basename(file) + " - Notepad")
            self.text.delete(1.0, 'end')
            with open(file, 'r') as f:
                self.text.insert(1.0, f.read())

    def save_file(self):
        file = filedialog.asksaveasfilename(defaultextension=".txt",filetypes=[("All Files", "*.*"),("Text Files", "*.txt")])
        if file:
            with open(file, 'w') as f:
                f.write(self.text.get(1.0, 'end'))

    def exit_app(self):
        self.root.quit()

    def cut(self):
        self.text.event_generate("<<Cut>>")

    def copy(self):
        self.text.event_generate("<<Copy>>")

    def paste(self):
        self.text.event_generate("<<Paste>>")

    def font(self):
        font = tk.font.nametofont("TkFixedFont")
        font_size = font.cget("size")
        new_size = tk.font.Font(size=font_size,
                                family="Arial",
                                weight="normal")
        self.text.configure(font=new_size)

    def about(self):
        tk.messagebox.showinfo("Notepad", "This is a simple Notepad app made using Python and Tkinter")

if __name__ == "__main__":
    root = tk.Tk()
    Notepad(root)
    root.mainloop()