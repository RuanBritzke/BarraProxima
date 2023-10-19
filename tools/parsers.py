from datetime import date
from icecream import ic
from os import PathLike
from collections import defaultdict, namedtuple
from itertools import zip_longest, accumulate


fields = {
    "SE": {
        "ID": int,
        "COD": str,
        "NOME": str,
        "REG": str,
        "LOC_TEC": float,
        "X": float,
        "Y": float,
        "COD_SE_MAE": str,
        "COD_CIRC_PAI": str,
    },
    "TRAFO_SE": {
        "ID": int,
        "COD": str,
        "ID_SE": int,
        "TIPO": int,
        "SNOM": float,
        "SNOMVENT": float,
        "VALTA": float,
        "VMEDIA": float,
        "VOP": float,
        "R0": float,
        "X0": float,
        "R1": float,
        "X1": float,
        "PERDA_FE": float,
        "PERDA_CU": float,
        "COD_BAR_MT": float,
        "TIPO_LIG": int,
        "ID_BAR_PRI": int,
        "ID_BAR_SEC": int,
        "ID_BAR_TER": int,
    },
    "CIRCUITO": {
        "ID": int,
        "COD": str,
        "ID_SE": float,
        "ID_TRAFO_SE": int,
        "VNOM": float,
        "VOP": float,
        "COD_BAR_MT": str,
        "NOME": str,
        "ID_BAR_MT": int,
        "ID_BARRA_INIT": str,
    },
    "DESPACHO_MAX": {
        "HORA": float,
        "P_KW": float,
        "Q_VAR": float,
        "I_A": float,
        "V_KV": float,
    },
    "SUPERVISAO": {
        "DATA_MAX": str,
        "HORA_MAX": str,
        "PMAX_KW": float,
        "QMAX_KVAR": float,
        "IMAX_A": float,
        "VMAX_KV": float,
        "DATA_MIN": str,
        "HORA_MIN": str,
        "PMIN_KW": float,
        "QMIN_KVAR": float,
        "IMIN_A": float,
        "VMIN_KV": float,
    },
    "BARRA": {"ID": int, "COD": int, "ID_CIRCUITO": int, "X": float, "Y": float},
    "TRECHO": {
        "ID": int,
        "COD": str,
        "ID_CIRCUITO": int,
        "ID_BARR0": int,
        "ID_BARR1": int,
        "MULT": int,
        "CABO_FASE": str,
        "CABO_NEUTRO": str,
        "FASES": str,
        "COMP": float,
        "ARRANJO": str,
    },
    "INSTAL_TRAFO": {},
    "UTC": {},
    "CHAVE": {},
    "PONTO_SERVICO_MT": {},
    "CONSUMIDOR_MT": {},
    "CONS_MT_DMD": {},
    "BARRA_BT": {},
    "GERADOR": {},
    "TRECHO_BT": {},
    "PONTO_SERVICO_BT": {},
    "CONSUMIDOR_BT": {},
    "GERADOR_BT": {},
    "CONSUMIDOR_IP": {},
    "CAPACITOR": {},
    "SOCO": {},
}


def converted_named_tuple(
    name: str, field_names_converters: dict, data: list | tuple
) -> namedtuple:
    field_names = list(field_names_converters.keys())
    newtuple = namedtuple(name, field_names)
    converted_data = [
        field_names_converters[field_name](elemnt) if elemnt != "" else None
        for field_name, elemnt in zip(field_names, data)
    ]
    return newtuple(*converted_data)._asdict()


def extraction_parser(content):
    extraction = defaultdict(list)
    current_header = None
    line: str
    for line in content:
        line = line.strip("\r\n")
        if line.strip(";") == "END":
            return extraction
        if line.strip(";") in fields.keys():
            current_header = line.strip(";")
            continue
        if current_header:
            if len(fields[current_header]) == 0:
                continue
            data = line.split(";")
            extraction[current_header].append(
                converted_named_tuple(current_header, fields[current_header], data)
            )

    return extraction


def make_fwf_parser(fieldwidths):
    cuts = tuple(cut for cut in accumulate(abs(fw) for fw in fieldwidths))
    pads = tuple(fw < 0 for fw in fieldwidths)  # bool flags for padding fields
    flds = tuple(zip_longest(pads, (0,) + cuts, cuts))[:-1]  # ignore final one
    slcs = ", ".join("line[{}:{}]".format(i, j) for pad, i, j in flds if not pad)
    parse = eval("lambda line: ({})\n".format(slcs))  # Create and compile source code.

    # Optional informational function attributes.
    parse.size = sum(abs(fw) for fw in fieldwidths)
    parse.fmtstring = " ".join(
        "{}{}".format(abs(fw), "x" if fw < 0 else "s") for fw in fieldwidths
    )
    return parse
