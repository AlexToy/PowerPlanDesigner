class Formula():
    def __init__(self, string):
        self.voltage_input, self.voltage_output, self.split, self.formula_1, self.formula_2 = string.split("/")
        print(self.voltage_input)
        print(self.voltage_output)
        print(self.split)
        print(self.formula_1)
        print(self.formula_2)

    def get_formula_efficiency(self, current_output : float) -> str :
        if current_output <= self.split:
            return self.formula_1
        else:
            return self.formula_2