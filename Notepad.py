from doctest import master
from tkinter import *
from tkinter import filedialog, messagebox, colorchooser


class MyNotepad:
    current_file = "no-file"

    def change_back_color(self):
        c = colorchooser.askcolor()
        self.txt_area.configure(background=c[1])

    def change_fore_color(self):
        c = colorchooser.askcolor()
        self.txt_area.configure(foreground=c[1])

    def exit_file(self):
        s = self.txt_area.get(1.0, END)
        if not s.strip():
            quit()
        else:
            result = messagebox.askyesnocancel("Save Dialog Box", "Do you want to save this file")
            if result == True:
                self.saveas_file()
                quit()
            elif result == False:
                quit()

    def clear(self):
        self.txt_area.delete(1.0, END)

    def new_file(self):
        s = self.txt_area.get(1.0, END)
        if not s.strip():
            pass
        else:
            result = messagebox.askyesnocancel("Save Dialog Box", "Do you want to save this file")
            if result == True:
                self.saveas_file()
                self.clear()
            elif result == False:
                self.clear()

    def saveas_file(self):
        f = filedialog.asksaveasfile(mode="w", defaultextension="*.txt")
        data = self.txt_area.get(1.0, END)
        f.write(data)
        self.current_file = f.name
        f.close()

    def save_file(self):
        if self.current_file == "no-file":
            self.saveas_file()
        else:
            f = open(self.current_file, mode="w")
            f.write(self.txt_area.get(1.0, END))
            f.close()

    def open_file(self, event=""):
        result = filedialog.askopenfile(initialdir='/', title="Open File dialog",
                                        filetypes=(("Text File", "*.txt"), ("All file", "*.*")))
        # print(result)

        for data in result:
            self.txt_area.insert(INSERT, data)
        self.current_file = result.name

    def cut_file(self):
        self.copy_file()
        self.txt_area.delete('sel.first', 'sel.last')

    def del_file(self):
        self.txt_area.delete('sel.first', 'sel.last')

    def copy_file(self):
        self.txt_area.clipboard_clear()
        self.txt_area.clipboard_append(self.txt_area.selection_get())

    def paste_file(self):
        self.txt_area.insert(INSERT, self.txt_area.clipboard_get())

    def __init__(self, master):
        self.master = master
        master.title("My Notepad")
        # master.wm_iconbitmap("ibooks.png")
        master.bind("<Control-o>", self.open_file)
        master.bind("<Control-O>", self.open_file)
        self.txt_area = Text(master, padx=5, pady=5, wrap=WORD, selectbackground="red", bd=2, insertwidth=3, undo=True)
        self.txt_area.pack(fill=BOTH, expand=1)
        self.main_menu = Menu()
        self.master.config(menu=self.main_menu)

        # creating file menu
        self.file_menu = Menu(self.main_menu, tearoff=False)
        self.main_menu.add_cascade(label="FILE", menu=self.file_menu)
        self.file_menu.add_command(label="new", accelerator="Ctrl+N", command=self.new_file)
        self.file_menu.add_command(label="Open", accelerator="Ctrl+O", command=self.open_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Save", accelerator="Ctrl+S", command=self.save_file)
        self.file_menu.add_command(label="Save As", command=self.saveas_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.exit_file)

        ##########################################

        # creating edit menu
        self.edit_menu = Menu(self.main_menu, tearoff=False)
        self.main_menu.add_cascade(label="EDIT", menu=self.edit_menu)
        self.edit_menu.add_command(label="Undo", command=self.txt_area.edit_undo)
        self.edit_menu.add_command(label="Redo", command=self.txt_area.edit_redo)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Cut", command=self.cut_file)
        self.edit_menu.add_command(label="Copy", command=self.copy_file)
        self.edit_menu.add_command(label="Paste", command=self.paste_file)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Delete", command=self.del_file)

        # creating format menu
        self.color_menu = Menu(self.main_menu, tearoff=False)
        self.main_menu.add_cascade(label="FORMAT", menu=self.color_menu)
        self.color_menu.add_command(label="BackGround Color", command=self.change_back_color)
        self.color_menu.add_command(label="ForeGround Color", command=self.change_fore_color)


root = Tk()
b = MyNotepad(root)
root.mainloop()
