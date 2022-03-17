class Formula():
    def __init__(self, string):
        if string == "None":
            self.formula_is_empty = True
        else:
            self.formula_is_empty = False
            voltage_input, voltage_output, split, formula_1, formula_2 = string.split("/")
            self.voltage_input = float(voltage_input)
            self.voltage_output = float(voltage_output)
            self.split = float(split)
            self.formula_1 = formula_1
            self.formula_2 = formula_2

    def get_formula_efficiency(self, current_output: float) -> str:
        if not self.formula_is_empty:
            if current_output <= self.split:
                return self.formula_1
            else:
                print(self.formula_2)
                return self.formula_2
