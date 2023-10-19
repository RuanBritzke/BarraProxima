import os

from tools import functions
from model import datastoragemanager as dsm
from collections import defaultdict, namedtuple
from icecream import ic


class Model:
    def init(self):
        if os.path.exists("data\\SES.pickle"):
            self.data = dsm.load_internal_pickle_file()
        elif os.path.exists("data\\SES.json"):
            self.data = dsm.load_internal_json_file()
        else:
            self.data = None

    def update_data(self):
        self.data = dsm.import_from_extraction_collection(
            r"K:\DPEP_DVPE\2 - Distribuicao\10 - Interplan\0 - Extracoes\2023\09 - Setembro"
        )
        dsm.save_to_internal_pickle_file(self.data)

    def get_closest_bars_to_point(self, point: tuple[float, float], n: int) -> list:
        unsorted_output = defaultdict(list)
        SortedOutput = namedtuple("SortedOutput", ["CIRC", "DIST", "COD"])
        for key in self.data:
            if key == "DATE":
                continue
            for se in self.data[key]:
                for bar in self.data[key][se]["BARRA"]:
                    updated_bar = {
                        "DIST": functions.distance(point, (bar["X"], bar["Y"])),
                        "COD": bar["COD"],
                    }
                    unsorted_output[
                        next(
                            circuit["COD"]
                            for circuit in self.data[key][se]["CIRCUITO"]
                            if circuit["ID"] == bar["ID_CIRCUITO"]
                        )
                    ].append(updated_bar)

        # getting the closest bar by circuit
        for circuit, bars in unsorted_output.items():
            closest_bar = sorted(bars, key=lambda bar: bar["DIST"])[
                0
            ]  # bars is a list os bar, and bar is a dict
            unsorted_output[circuit] = closest_bar

        # getting the top n closest circuits
        sorted_circuits = sorted(
            unsorted_output, key=lambda x: unsorted_output[x]["DIST"]
        )[0:n]
        ic(sorted_circuits)
        return [
            SortedOutput(circuit, **unsorted_output[circuit])
            for circuit in sorted_circuits
        ]
