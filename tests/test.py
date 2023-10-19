import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Tabular Data")

# Create a Treeview widget
tree = ttk.Treeview(root)
tree.pack()

tree["columns"] = ("ID", "Name", "  Age")
tree.column("#0", width=0, stretch=tk.NO)
tree.column("ID", anchor=tk.W, width=100)
tree.column("Name", anchor=tk.W, width=150)
tree.column("Age", anchor=tk.W, width=50)

tree.heading("#0", text="", anchor=tk.W)
tree.heading("ID", text="ID", anchor=tk.W)
tree.heading("Name", text="Name", anchor=tk.W)
tree.heading("Age", text="Age", anchor=tk.W)

data = [
    ("1", "John Doe", "30"),
    (
        "2",
        "Jane Smith",
    ),
    ("3", "Bob Johnson", "35"),
]

for item in data:
    tree.insert("", tk.END, values=item)

tree.tag_configure("selected", background="yellow")


def on_select(event):
    item = tree.selection()[0]
    tree.item(item, tags=("selected",))
    values = tree.item(item)["values"]
    str_values = [str(value) for value in values]
    copied_data = "\t".join(str_values)
    root.clipboard_clear()
    root.clipboard_append(copied_data)


tree.bind("<<TreeviewSelect>>", on_select)

root.mainloop()
