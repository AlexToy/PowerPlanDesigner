import openpyxl
from typing import List
from DcdcWidget import DcdcWidget
from PsuWidget import PsuWidget
from ConsumerWidget import ConsumerWidget
from Formula import Formula


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
CONSUMER_REF_COMPONENT_1 = 2
CONSUMER_REF_COMPONENT_2 = 3
CONSUMER_EQUIVALENCE_CODE = 4
CONSUMER_INFO = 5
CONSUMER_VOLTAGE_INPUT = 6
CONSUMER_CURRENT_THEORETICAL = 7
CONSUMER_CURRENT_MIN_MEASURE = 8
CONSUMER_CURRENT_MAX_MEASURE = 9
CONSUMER_CURRENT_PEAK_MEASURE = 10

FILE_DATABASE = "DATA_BASE.xlsx"
FILE_CONSUMER_DATA_BASE = "Consumer_DATA_BASE.xlsx"


def loading_database() -> List[DcdcWidget] and List[PsuWidget] and List[ConsumerWidget]:

    input_file_database = openpyxl.load_workbook(FILE_DATABASE, read_only=True)
    for sheet in input_file_database:
        if sheet.title == "DCDC":
            sheet_dcdc = sheet
        elif sheet.title == "PSU":
            sheet_psu = sheet

    print("Loading database ...")

    # Loading DCDC DATABASE
    dcdc_list = []
    dcdc_formula_list = []
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

            line = DCDC_VOLTAGE_OUTPUT_MAX + 1
            while str(sheet_dcdc.cell(line, column).value) != "None":
                dcdc_formula_list.append(Formula(str(sheet_dcdc.cell(line, column).value)))
                line = line + 1

            print(ref_component)
            dcdc_list.append(DcdcWidget(ref_component, supplier, current_max, equivalence_code, voltage_input_min,
                             voltage_input_max, voltage_output_min, voltage_output_max, dcdc_formula_list))

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

            psu_list.append(PsuWidget(ref_component, supplier, equivalence_code, current_max, voltage_input,
                            voltage_output, jack))

    # Loading CONSUMER DATABASE
    input_file_consumer_database = openpyxl.load_workbook(FILE_CONSUMER_DATA_BASE, read_only=True)
    consumer_list = []
    line = 1
    for sheet_consumer in input_file_consumer_database:
        print("sheet : " + str(sheet_consumer.title))
        line = 1
        for _ in sheet_consumer:
            line = line + 1
            print("     line : " + str(line))
            if str(sheet_consumer.cell(line, 1).value) != "None":
                name = str(sheet_consumer.cell(line, CONSUMER_NAME).value)
                ref_component_1 = str(sheet_consumer.cell(line, CONSUMER_REF_COMPONENT_1).value)
                ref_component_2 = str(sheet_consumer.cell(line, CONSUMER_REF_COMPONENT_2).value)
                equivalence_code = str(sheet_consumer.cell(line, CONSUMER_EQUIVALENCE_CODE).value)
                info = str(sheet_consumer.cell(line, CONSUMER_INFO).value)
                voltage_input = float(sheet_consumer.cell(line, CONSUMER_VOLTAGE_INPUT).value)
                current_theoretical = float(sheet_consumer.cell(line, CONSUMER_CURRENT_THEORETICAL).value)
                current_min_measure = str(sheet_consumer.cell(line, CONSUMER_CURRENT_MIN_MEASURE).value)
                current_max_measure = str(sheet_consumer.cell(line, CONSUMER_CURRENT_MAX_MEASURE).value)
                current_peak_measure = str(sheet_consumer.cell(line, CONSUMER_CURRENT_PEAK_MEASURE).value)

                consumer_list.append(ConsumerWidget(name, ref_component_1, ref_component_2, equivalence_code, info,
                                                    voltage_input, current_theoretical, current_min_measure,
                                                    current_max_measure, current_peak_measure))

    print("Database loaded !")
    return dcdc_list, psu_list, consumer_list