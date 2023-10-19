import os
import zipfile
import json
import pickle
from collections import defaultdict
from tools import parsers, functions
from tqdm import tqdm
from icecream import ic


def save_to_internal_json_file(data: dict):
    """Salva dados manipulados pelo progama na memoria persistente no formato `json`"""

    with open("data\\SES.json", "w") as json_file:
        json_file.write(json.dumps(data, indent=4))


def load_internal_json_file():
    with open("data\\SES.json", "r") as data_file:
        data = json.load(data_file)
    return data


def save_to_internal_pickle_file(data: dict):
    """Salva dados manipulados pelo progama na memoria persistente no formato `pickle`"""

    with open("data\\SES.pickle", "wb") as pickle_file:
        pickle.dump(data, pickle_file)


def load_internal_pickle_file():
    with open("data\\SES.pickle", "rb") as data_file:
        data = pickle.load(data_file)
    return data


def import_from_extraction_collection(extraction_dir: os.PathLike):
    """Abre e importa para a memoria do programa os dados das extrações salvos em
    `K:\\DPEP_DVPE\\2 - Distribuicao\\10 - Interplan\\Extracoes\\$Ano$`
    """
    data = defaultdict(dict)

    year, month = functions.extract_year_month(extraction_dir)
    data["DATE"] = f"{year}-{month:02d}"

    files = [
        os.path.join(dirpath, f)
        for (dirpath, _, filenames) in os.walk(extraction_dir)
        for f in filenames
    ]

    for file in files:
        new_data = import_from_zipfile(file)
        for reg, value in new_data.items():
            for se in value.keys():
                data[reg][se] = value[se]
    return data


def import_from_zipfile(zipdir: os.PathLike):
    data = defaultdict(lambda: dict())
    with zipfile.ZipFile(zipdir, "r") as zip_file:
        file_list = zip_file.namelist()

        for file_name in file_list:
            reg, _, _, _, se = file_name.split(".")[0].split("_")
            with zip_file.open(file_name) as file:
                data[reg][se] = parsers.extraction_parser(
                    [line.decode("ANSI") for line in file.readlines()]
                )
    return data
