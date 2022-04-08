class Pmic():

    def __init__(self, ref_component: str, supplier: str, equivalence_code: str):

        self.ref_component = ref_component
        self.supplier = supplier
        self.equivalence_code = equivalence_code
        self.list_dcdc = []
        self.list_ldo = []

    def add_dcdc(self, dcdc):
        self.list_dcdc.append(dcdc)

    def add_ldo(self, ldo):
        self.list_ldo.append(ldo)