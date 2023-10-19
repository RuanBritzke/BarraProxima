import tkinter as tk

from view.customs import *
from tkinter import ttk
from icecream import ic
from controller.controller import Controller


class App(tk.Tk):
    def __init__(self, controller: Controller | None = None):
        super().__init__()

        self.title("TBD - CELESC")
        self.state("iconic")

        self.controller = controller

        self.create_importing_menu()
        self.create_coord_format_selection_frame()
        self.create_outputs_frame()
        self.create_status_bar()
        self.controller.init(self)

    def create_importing_menu(self):
        menubar = tk.Menu(self, tearoff=False)

        self.config(menu=menubar)
        menubar.add_command(label="Importar", command=self.importing)

    def importing(self):
        if self.controller == None:
            return
        self.controller.importing_controll()

    def create_coord_format_selection_frame(self):
        coord_format_selection_frame = tk.Frame(self)
        coord_format_selection_frame.pack(side="top", anchor="nw", padx=5, pady=(2, 0))

        self.coord_formart_selected = tk.StringVar(value="UTM")
        self.utm = ttk.Radiobutton(
            coord_format_selection_frame,
            text="UTM",
            variable=self.coord_formart_selected,
            value="UTM",
            command=self.on_coord_format_selection,
            style="TButton",
        )
        self.latlong = ttk.Radiobutton(
            coord_format_selection_frame,
            text="Lat. Long.",
            variable=self.coord_formart_selected,
            value="LatLong",
            command=self.on_coord_format_selection,
            style="TButton",
        )
        self.utm.grid(row=0, column=0)
        self.latlong.grid(row=0, column=1)
        self.on_coord_format_selection()

    def on_coord_format_selection(self, *args):
        if hasattr(self, "inputs_field") and self.inputs_field.winfo_exists():
            self.inputs_field.destroy()
        if self.coord_formart_selected.get() == "UTM":
            self.create_inputs_frame("UTM")
        elif self.coord_formart_selected.get() == "LatLong":
            self.create_inputs_frame("LatLong")

    def create_inputs_frame(self, option):
        self.inputs_field = tk.Frame(self, background="white")
        self.inputs_field.pack(side="top", anchor="nw", fill="x", expand=True)
        if option == "UTM":
            self.entries = Form(
                self.inputs_field,
                background="white",
                prompts={
                    "X": {"text": "X", "default": "746916,95"},
                    "Y": {"text": "X", "default": "6945830,93"},
                    "N": {"text": "N. Alimentadores", "default": "10"},
                },
            )
            self.entries.pack(side="top", anchor="nw", fill="x", expand=True)
        else:  # option == "LatLong"
            self.entries = Form(
                self.inputs_field,
                background="white",
                prompts={
                    "Lat": {"text": "Latitute", "default": "-27,58898"},
                    "Long": {"text": "Longitude", "default": "-48,49855"},
                    "N": {"text": "N. Alimentadores", "default": "10"},
                },
            )
            self.entries.pack(side="top", anchor="nw", fill="x", expand=True)
        self.create_send_button(self.inputs_field)

    def create_send_button(self, master):
        self.send_button = tk.Button(master, text="Calcular", command=self.send_coords)
        self.send_button.pack(
            side="top", after=self.entries, anchor="se", padx=5, pady=5
        )

    def send_coords(self):
        if self.controller == None:
            return
        self.controller.calculate_closest(
            self.entries.get_entry_values(), self.coord_formart_selected.get()
        )

    def create_outputs_frame(self, *, data: list | None = None):
        self.outputs_frame = tk.Frame(self, background="white")
        self.outputs_frame.pack(
            side="top",
            after=self.send_button,
            anchor="nw",
            padx=5,
            pady=(5, 0),
            fill="both",
            expand=True,
        )
        table = Table(self.outputs_frame, data=data)
        table.pack(anchor="nw", fill="both", expand=True)

    def create_status_bar(self):
        self.status_bar = StatusBar(self, bg="white")

    def update_output(self, data):
        self.outputs_frame.destroy()
        self.create_outputs_frame(data=data)
