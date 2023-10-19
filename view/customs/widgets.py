import re
import tkinter as tk

from tkinter import ttk
from typing import Literal
from collections import namedtuple

prompt = str
key = str
entry_type = Literal["Any", "float"]


class Form(tk.Frame):
    def __init__(self, master, prompts: dict[key:dict], **kwargs) -> None:
        super().__init__(master, **kwargs)
        self.columnconfigure(0, weight=8, minsize=80)
        self.columnconfigure(1, weight=1, minsize=35)
        self.bind("<Configure>", self.on_container_configure)

        self.labels = []
        self.entries = []
        self.values = dict()

        for i, (key, items) in enumerate(prompts.items()):
            label = tk.Label(
                self,
                text=items["text"],
                anchor="w",
                justify="left",
            )

            self.labels.append(label)

            string_var = tk.StringVar()

            entry = FloatEntry(
                self,
                default_text=items["default"] if "default" in items.keys() else None,
                textvariable=string_var,
            )

            self.entries.append(entry)
            self.values[key] = entry

            label.grid(row=i, column=0, sticky="nsew", padx=5, pady=5)
            entry.grid(row=i, column=1, sticky="nsew", padx=(0, 5), pady=5)

    def on_container_configure(self, event):
        self.after(1, self.update_wraplengths)

    def update_wraplengths(self):
        label: tk.Label
        for label in self.labels:
            label.config(wraplength=label.winfo_width())

    def get_entry_values(self):
        return {key: value.get_value() for key, value in self.values.items()}


class FloatEntry(ttk.Entry):
    def __init__(self, *args, default_text: str | None = None, **kwargs):
        super().__init__(*args, validate="key", **kwargs)
        self.default_text = default_text

        vcmd = (self.register(self.on_validate), "%P")
        self.config(validatecommand=vcmd)

        self.bind("<FocusIn>", self.on_entry_focus_in)
        self.bind("<FocusOut>", self.on_entry_focus_out)

        if self.default_text:
            self.after_idle(self.insert_default_text)

    def insert_default_text(self):
        if self.get() == "":
            self.insert(0, self.default_text)
            self.config(foreground="gray")

    def on_entry_focus_in(self, event):
        if not self.default_text:
            return
        if self.get() == self.default_text:
            self.delete(0, "end")
            self.config(foreground="black")

    def on_entry_focus_out(self, event):
        if not self.default_text:
            return
        if self.get() == "":
            self.insert(0, self.default_text)
            self.config(foreground="gray")

    def on_validate(self, P):
        return self.validate(P)

    def validate(self, string):
        regex = re.compile(r"(\+|\-)?[0-9,]*$")
        result = regex.match(string)
        return string == "" or (
            string.count("+") <= 1
            and string.count("-") <= 1
            and string.count(",") <= 1
            and result is not None
            and result.group(0) != ""
        )

    def get_value(self):
        if self.get() == "":
            return ""
        return self.get().replace(",", ".")


class StatusBar(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.config(highlightbackground="black", highlightthickness=1)
        self.label = tk.Label(self, text="", bg="white")
        self.label.pack(side="left")
        self.pack(side="bottom", fill="both")

    def blink(self, color):
        pass

    def set(self, newText):
        self.label.config(text=newText)

    def clear(self):
        self.label.config(text="")


class Table(ttk.Treeview):
    """Create a table like widget"""

    def __init__(self, master, *, data: list[namedtuple] | None = None, **kwargs):
        super().__init__(master=master)
        self.create_table(data)

    def create_table(self, data: list[namedtuple] | None):
        if data is None or len(data) == 0:
            return

        keys = list()
        for d in data:
            d = {field: getattr(d, field) for field in d._fields}
            for key, value in d.items():
                keys.append(f"_{key}") if f"_{key}" not in keys else None

        self["columns"] = tuple(keys)

        self.column("#0", width=0, stretch=tk.NO)
        self.heading("#0", text="", anchor=tk.W)

        for key in keys:
            self.column(key, anchor=tk.E)
            self.heading(key, text=key.replace("_", ""), anchor=tk.E)

        for item in data:
            values = [getattr(item, key.replace("_", "")) for key in keys]
            self.insert("", tk.END, values=values)
