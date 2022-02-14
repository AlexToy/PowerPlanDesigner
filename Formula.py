class Formula():
    def __init__(self, string):
        voltage_input, voltage_output, split, formula_1, formula_2 = string.split("/")
        self.voltage_input = float(voltage_input)
        self.voltage_output = float(voltage_output)
        self.split = float(split)
        self.formula_1 = formula_1
        self.formula_2 = formula_2
        print(self.voltage_input)
        print(self.voltage_output)
        print(self.split)
        print(self.formula_1)
        print(self.formula_2)

    def get_formula_efficiency(self, current_output: float) -> str:
        if current_output <= self.split:
            return self.formula_1
        else:
            print(self.formula_2)
            return self.formula_2
