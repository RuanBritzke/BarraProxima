import os
import utm

from datetime import datetime
from model import datastoragemanager as dsm
from model.model import Model
from icecream import ic


class Controller:
    def __init__(self, model: Model) -> None:
        self.model = Model()

    def init(self, view) -> None:
        self.view = view
        self.view.status_bar.set("Carregando dados")
        self.model.init()
        if self.model.data:
            self.view.status_bar.set("Dados Carregados")
            self.check_data_uptades()
        else:
            self.view.status_bar.clear()
            self.no_data_warning()

    ## Warnings
    def no_data_warning(self):
        pass

    ## Model Controll ##
    def check_data_uptades(self):
        ic(self.model.data["DATE"])

    ## callable from view ##

    def importing_controll(self):
        self.model.update_data()

    def calculate_closest(self, values: dict, format):
        if any([value == "" for kw, value in values.items()]):
            return "EmptyEntry"

        n = int(values["N"])

        if format == "UTM":
            point = (float(values["X"]), float(values["Y"]))
        else:  # format == "LatLong"
            lat, long = (float(values["Lat"]), float(values["Long"]))
            x, y, _, _ = utm.from_latlon(lat, long)
            point = (x, y)

        result = ic(self.model.get_closest_bars_to_point(point, n))
        self.view.update_output(data=result)
