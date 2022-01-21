import openpyxl
from typing import List
from Dcdc import Dcdc
from Psu import Psu
from Consumer import Consumer


# DCDC DATABASE
REF_COMPONENT = 1
SUPPLIER = 2
CURRENT_MAX = 3
EQUIVALENCE_CODE = 4
VOLTAGE_INPUT_MIN = 5
VOLTAGE_INPUT_MAX = 6
VOLTAGE_OUTPUT_MIN = 7
VOLTAGE_OUTPUT_MAX = 8

# PSU DATABASE
NAME = 1
VOLTAGE_IN = 2
VOLTAGE_OUT = 3
CURRENT = 4

FILE_DATABASE = "DATA_BASE.xlsx"


def loading_database() -> List[Dcdc] and List[Psu] and List[Consumer]:

    input_file = openpyxl.load_workbook(FILE_DATABASE, read_only=True)
    for sheet in input_file:
        if sheet.title == "DCDC":
            sheet_dcdc = sheet
        elif sheet.title == "PSU":
            sheet_psu = sheet
        elif sheet.title == "CONSUMER":
            sheet_consumer = sheet

    print("Loading database ...")

    # Loading DCDC DATABASE
    dcdc_list = []
    column = 1
    for _ in sheet_dcdc:
        column = column + 1
        if str(sheet_dcdc.cell(1, column).value) != "None":
            ref_component = str(sheet_dcdc.cell(REF_COMPONENT, column).value)
            supplier = str(sheet_dcdc.cell(SUPPLIER, column).value)
            current_max = str(sheet_dcdc.cell(CURRENT_MAX, column).value)
            equivalence_code = str(sheet_dcdc.cell(EQUIVALENCE_CODE, column).value)
            voltage_input_min = str(sheet_dcdc.cell(VOLTAGE_INPUT_MIN, column).value)
            voltage_input_max = str(sheet_dcdc.cell(VOLTAGE_INPUT_MAX, column).value)
            voltage_output_min = str(sheet_dcdc.cell(VOLTAGE_OUTPUT_MIN, column).value)
            voltage_output_max = str(sheet_dcdc.cell(VOLTAGE_OUTPUT_MAX, column).value)

            print(ref_component)
            dcdc_list.append(Dcdc(ref_component, supplier, current_max, equivalence_code, voltage_input_min,
                                  voltage_input_max, voltage_output_min, voltage_output_max))

    # Loading PSU DATABASE
    psu_list = []
    column = 1
    for _ in sheet_psu:
        column = column + 1
        if str(sheet_psu.cell(1, column).value) != "None":
            name = str(sheet_psu.cell(NAME, column).value)
            voltage_input = str(sheet_psu.cell(VOLTAGE_IN, column).value)
            voltage_output = str(sheet_psu.cell(VOLTAGE_OUT, column).value)
            current = str(sheet_psu.cell(CURRENT, column).value)

            print(name)
            psu_list.append(Psu(name, voltage_input, voltage_output, current))

    # Loading CONSUMER DATABASE
    consumer_list = []
    column = 1
    for _ in sheet_consumer:
        column = column + 1
        if str(sheet_consumer.cell(1, column).value) != "None":
            name = str(sheet_consumer.cell(1, column).value)
            text = str(sheet_consumer.cell(2, column).value)
            voltage = str(sheet_consumer.cell(3, column).value)
            current = str(sheet_consumer.cell(4, column).value)

            print(name)
            consumer_list.append(Consumer(name, text, voltage, current))

    print("Database loaded !")
    return dcdc_list, psu_list, consumer_list
