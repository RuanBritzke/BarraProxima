import tkinter as tk


def show_tooltop(widget: tk.Widget, event, text):
    x, y, _, _ = widget.winfo_geometry().split("+")
    x = int(x)
    y = int(y)
    tooltip = tk.Toplevel(widget)
    tooltip.wm_overrideredirect(True)
    tooltip.wm_geometry(f"+{x}+{y+25}")
    label = tk.Label(tooltip, text=text)
    label.pack
