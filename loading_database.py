import openpyxl
from typing import List
from Dcdc import Dcdc
from Psu import Psu
from Consumer import Consumer


# DCDC DATABASE
DCDC_REF_COMPONENT = 1
DCDC_SUPPLIER = 2
DCDC_CURRENT_MAX = 3
DCDC_EQUIVALENCE_CODE = 4
DCDC_VOLTAGE_INPUT_MIN = 5
DCDC_VOLTAGE_INPUT_MAX = 6
DCDC_VOLTAGE_OUTPUT_MIN = 7
DCDC_VOLTAGE_OUTPUT_MAX = 8

# PSU DATABASE
PSU_REF_COMPONENT = 1
PSU_SUPPLIER = 2
PSU_EQUIVALENCE_CODE = 3
PSU_CURRENT_MAX = 4
PSU_VOLTAGE_IN = 5
PSU_VOLTAGE_OUT = 6
PSU_JACK = 7

# CONSUMER DATABASE
CONSUMER_NAME = 1
CONSUMER_REF_COMPONENT = 2
CONSUMER_INFO = 3
CONSUMER_EQUIVALENCE_CODE = 4
CONSUMER_VOLTAGE_INPUT = 5
CONSUMER_CURRENT_INPUT = 6

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
            ref_component = str(sheet_dcdc.cell(DCDC_REF_COMPONENT, column).value)
            supplier = str(sheet_dcdc.cell(DCDC_SUPPLIER, column).value)
            current_max = float(sheet_dcdc.cell(DCDC_CURRENT_MAX, column).value)
            equivalence_code = str(sheet_dcdc.cell(DCDC_EQUIVALENCE_CODE, column).value)
            voltage_input_min = float(sheet_dcdc.cell(DCDC_VOLTAGE_INPUT_MIN, column).value)
            voltage_input_max = float(sheet_dcdc.cell(DCDC_VOLTAGE_INPUT_MAX, column).value)
            voltage_output_min = float(sheet_dcdc.cell(DCDC_VOLTAGE_OUTPUT_MIN, column).value)
            voltage_output_max = float(sheet_dcdc.cell(DCDC_VOLTAGE_OUTPUT_MAX, column).value)

            print(ref_component)
            dcdc_list.append(Dcdc(ref_component, supplier, current_max, equivalence_code, voltage_input_min,
                                  voltage_input_max, voltage_output_min, voltage_output_max))

    # Loading PSU DATABASE
    psu_list = []
    column = 1
    for _ in sheet_psu:
        column = column + 1
        if str(sheet_psu.cell(1, column).value) != "None":
            ref_component = str(sheet_psu.cell(PSU_REF_COMPONENT, column).value)
            supplier = str(sheet_psu.cell(PSU_SUPPLIER, column).value)
            equivalence_code = str(sheet_psu.cell(PSU_EQUIVALENCE_CODE, column).value)
            current_max = float(sheet_psu.cell(PSU_CURRENT_MAX, column).value)
            voltage_input = float(sheet_psu.cell(PSU_VOLTAGE_IN, column).value)
            voltage_output = float(sheet_psu.cell(PSU_VOLTAGE_OUT, column).value)
            jack = str(sheet_psu.cell(PSU_JACK, column).value)

            psu_list.append(Psu(ref_component, supplier, equivalence_code, current_max, voltage_input,
                                voltage_output, jack))

    # Loading CONSUMER DATABASE
    consumer_list = []
    column = 1
    for _ in sheet_consumer:
        column = column + 1
        if str(sheet_consumer.cell(1, column).value) != "None":
            name = str(sheet_consumer.cell(CONSUMER_NAME, column).value)
            ref_component = str(sheet_consumer.cell(CONSUMER_REF_COMPONENT, column).value)
            info = str(sheet_consumer.cell(CONSUMER_INFO, column).value)
            equivalence_code = str(sheet_consumer.cell(CONSUMER_EQUIVALENCE_CODE, column).value)
            voltage_input = float(sheet_consumer.cell(CONSUMER_VOLTAGE_INPUT, column).value)
            current_input = float(sheet_consumer.cell(CONSUMER_CURRENT_INPUT, column).value)

            consumer_list.append(Consumer(name, ref_component, info, equivalence_code, voltage_input, current_input))

    print("Database loaded !")
    return dcdc_list, psu_list, consumer_list
