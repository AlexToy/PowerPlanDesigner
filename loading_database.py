import openpyxl
from typing import List
from DcdcWidget import DcdcWidget
from PsuWidget import PsuWidget
from ConsumerWidget import ConsumerWidget
from LdoWidget import LdoWidget
from Formula import Formula

# DCDC DATABASE
DCDC_REF_COMPONENT = 1
DCDC_SUPPLIER = 2
DCDC_CURRENT_MAX = 3
DCDC_MODE = 4
DCDC_EQUIVALENCE_CODE = 5
DCDC_VOLTAGE_INPUT_MIN = 6
DCDC_VOLTAGE_INPUT_MAX = 7
DCDC_VOLTAGE_OUTPUT_MIN = 8
DCDC_VOLTAGE_OUTPUT_MAX = 9
DCDC_EFFICIENCY = 10

# DCDC DATABASE
LDO_REF_COMPONENT = 1
LDO_SUPPLIER = 2
LDO_CURRENT_MAX = 3
LDO_EQUIVALENCE_CODE = 4
LDO_VOLTAGE_INPUT_MIN = 5
LDO_VOLTAGE_INPUT_MAX = 6
LDO_VOLTAGE_OUTPUT = 7

# PSU DATABASE
PSU_REF_COMPONENT = 1
PSU_SUPPLIER = 2
PSU_EQUIVALENCE_CODE = 3
PSU_CURRENT_MAX = 4
PSU_VOLTAGE_IN = 5
PSU_VOLTAGE_OUT = 6
PSU_JACK = 7

# CONSUMER DATABASE
CONSUMER_TYPE = 1
CONSUMER_SUPPLIER = 2
CONSUMER_REF_COMPONENT = 3
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
        elif sheet.title == "LDO":
            sheet_ldo = sheet

    print("Loading database ...")

    # Loading DCDC DATABASE
    dcdc_list = []
    dcdc_formula_list = []
    line = 1
    for _ in sheet_dcdc:
        line = line + 1
        if str(sheet_dcdc.cell(line, 1).value) != "None":
            ref_component = str(sheet_dcdc.cell(line, DCDC_REF_COMPONENT).value)
            supplier = str(sheet_dcdc.cell(line, DCDC_SUPPLIER).value)
            current_max = float(sheet_dcdc.cell(line, DCDC_CURRENT_MAX).value)
            mode = str(sheet_dcdc.cell(line, DCDC_MODE).value)
            equivalence_code = str(sheet_dcdc.cell(line, DCDC_EQUIVALENCE_CODE).value)
            voltage_input_min = float(sheet_dcdc.cell(line, DCDC_VOLTAGE_INPUT_MIN).value)
            voltage_input_max = float(sheet_dcdc.cell(line, DCDC_VOLTAGE_INPUT_MAX).value)
            voltage_output_min = float(sheet_dcdc.cell(line, DCDC_VOLTAGE_OUTPUT_MIN).value)
            voltage_output_max = float(sheet_dcdc.cell(line, DCDC_VOLTAGE_OUTPUT_MAX).value)
            if str(sheet_dcdc.cell(line, DCDC_EFFICIENCY).value) != "None":
                dcdc_formula_list.append(Formula(str(sheet_dcdc.cell(line, DCDC_EFFICIENCY).value)))

            dcdc_list.append(DcdcWidget(ref_component, supplier, current_max, mode, equivalence_code, voltage_input_min,
                                        voltage_input_max, voltage_output_min, voltage_output_max, dcdc_formula_list))

    # Loading PSU DATABASE
    psu_list = []
    line = 1
    for _ in sheet_psu:
        line = line + 1
        if str(sheet_psu.cell(line, 1).value) != "None":
            ref_component = str(sheet_psu.cell(line, PSU_REF_COMPONENT).value)
            supplier = str(sheet_psu.cell(line, PSU_SUPPLIER).value)
            equivalence_code = str(sheet_psu.cell(line, PSU_EQUIVALENCE_CODE).value)
            current_max = float(sheet_psu.cell(line, PSU_CURRENT_MAX).value)
            voltage_input = float(sheet_psu.cell(line, PSU_VOLTAGE_IN).value)
            voltage_output = float(sheet_psu.cell(line, PSU_VOLTAGE_OUT).value)
            jack = str(sheet_psu.cell(line, PSU_JACK).value)

            psu_list.append(PsuWidget(ref_component, supplier, equivalence_code, current_max, voltage_input,
                                      voltage_output, jack))

    # Loading LDO DATABASE
    ldo_list = []
    line = 1
    for _ in sheet_ldo:
        line = line + 1
        if str(sheet_ldo.cell(line, 1).value) != "None":
            ref_component = str(sheet_ldo.cell(line, LDO_REF_COMPONENT).value)
            supplier = str(sheet_ldo.cell(line, LDO_SUPPLIER).value)
            current_max = float(sheet_ldo.cell(line, LDO_CURRENT_MAX).value)
            equivalence_code = str(sheet_ldo.cell(line, LDO_EQUIVALENCE_CODE).value)
            voltage_input_min = float(sheet_ldo.cell(line, LDO_VOLTAGE_INPUT_MIN).value)
            voltage_input_max = float(sheet_ldo.cell(line, LDO_VOLTAGE_INPUT_MAX).value)
            voltage_output = float(sheet_ldo.cell(line, LDO_VOLTAGE_OUTPUT).value)

            ldo_list.append(LdoWidget(ref_component, supplier, current_max, equivalence_code, voltage_input_min,
                                      voltage_input_max, voltage_output))

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
                type = str(sheet_consumer.cell(line, CONSUMER_TYPE).value)
                supplier = str(sheet_consumer.cell(line, CONSUMER_SUPPLIER).value)
                ref_component = str(sheet_consumer.cell(line, CONSUMER_REF_COMPONENT).value)
                equivalence_code = str(sheet_consumer.cell(line, CONSUMER_EQUIVALENCE_CODE).value)
                info = str(sheet_consumer.cell(line, CONSUMER_INFO).value)
                voltage_input = float(sheet_consumer.cell(line, CONSUMER_VOLTAGE_INPUT).value)
                current_theoretical = float(sheet_consumer.cell(line, CONSUMER_CURRENT_THEORETICAL).value)
                current_min_measure = str(sheet_consumer.cell(line, CONSUMER_CURRENT_MIN_MEASURE).value)
                current_max_measure = str(sheet_consumer.cell(line, CONSUMER_CURRENT_MAX_MEASURE).value)
                current_peak_measure = str(sheet_consumer.cell(line, CONSUMER_CURRENT_PEAK_MEASURE).value)

                consumer_list.append(ConsumerWidget(str(sheet_consumer.title), type, supplier, ref_component,
                                                    equivalence_code, info, voltage_input, current_theoretical,
                                                    current_min_measure, current_max_measure, current_peak_measure))

    print("Database loaded !")
    return dcdc_list, psu_list, ldo_list, consumer_list
