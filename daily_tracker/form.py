"""
The form for the pop-up box.
"""
import tkinter
import tkinter.ttk


def main() -> None:
    """"""
    root = tkinter.Tk()
    frm = tkinter.ttk.Frame(root, padding=10)
    frm.grid()
    tkinter.ttk.Label(frm, text="Hello World!").grid(column=0, row=0)
    tkinter.ttk.Button(frm, text="Quit", command=root.destroy).grid(column=1, row=0)
    root.mainloop()
