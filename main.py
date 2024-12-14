import math


class DistillationColumn:
    def __init__(self, diameter, Dmole_flow, Bmole_flow, Dmass_flow, Bmass_flow, reflux_ratio,
                 boilup_ratio, liquid_density, vapor_density, molecular_weight, surface_tension):
        self.diameter = diameter  # Column diameter in meters
        self.Dmole_flow = Dmole_flow  # Distillate mole flow (mole/hr)
        self.Bmole_flow = Bmole_flow  # Bottoms mole flow (mole/hr)
        self.Dmass_flow = Dmass_flow  # Distillate mass flow (kg/hr)
        self.Bmass_flow = Bmass_flow  # Bottoms mass flow (kg/hr)
        self.reflux_ratio = reflux_ratio  # Reflux ratio
        self.boilup_ratio = boilup_ratio  # Boilup ratio

        # User-specified properties
        self.liquid_density = liquid_density  # Liquid density (kg/m^3)
        self.vapor_density = vapor_density  # Vapor density (kg/m^3)
        self.molecular_weight = molecular_weight  # Average molecular weight (kg/kmole)
        self.surface_tension = surface_tension  # Surface tension (mN/m)

        # Calculated column cross-sectional area
        self.cross_sectional_area = 0.85 * (math.pi * self.diameter ** 2) / 4

    def calculate_flow_rates(self):
        """Calculate the actual flow rates based on reflux and boilup ratios."""
        Vmole_flow = self.Dmole_flow * (self.reflux_ratio + 1)  # mole/hr
        Bmole_flow = self.Bmole_flow * (self.boilup_ratio + 1)  # mole/hr
        Vmass_flow = self.Dmass_flow * (self.reflux_ratio + 1)  # kg/hr
        Bmass_flow = self.Bmass_flow * (self.boilup_ratio + 1)  # kg/hr
        return Vmole_flow, Bmole_flow, Vmass_flow, Bmass_flow

    def calculate_opt_velocity(self, Vmole_flow):
        """Calculate the operating velocity (v_opt) in ft/s."""
        v_opt = Vmole_flow * self.molecular_weight / (self.vapor_density * self.cross_sectional_area * 3600)  # m/s
        return v_opt / 0.3048  # Convert to ft/s

    def calculate_flooding_velocity(self, Bmass_flow, Vmass_flow):
        """Calculate the flooding velocity (v_flood) in ft/s."""
        # Calculate the flooding factor (Flv)
        Flv = (Bmass_flow / Vmass_flow) * math.sqrt(self.vapor_density / self.liquid_density)

        # Calculate Csbf
        Csbf = 10 ** (-1.0262 - 0.63513 * math.log10(Flv) - 0.20097 * (math.log10(Flv) ** 2))

        # Calculate v_flood
        v_flood = Csbf * ((self.surface_tension / 20) ** 0.2) * math.sqrt(
            (self.liquid_density - self.vapor_density) / self.vapor_density)

        return v_flood

    def simulate(self):
        """Simulate the distillation column."""
        Vmole_flow, Bmole_flow, Vmass_flow, Bmass_flow = self.calculate_flow_rates()
        v_opt = self.calculate_opt_velocity(Vmole_flow)
        v_flood = self.calculate_flooding_velocity(Bmass_flow, Vmass_flow)
        flooding_percentage = v_opt / v_flood * 100  # Percentage

        return {
            "flooding_velocity": v_flood,
            "operating_velocity": v_opt,
            "flooding_percentage": flooding_percentage
        }


# Example usage
if __name__ == "__main__":
    # Base column ------------------------------------------------------------------------------------
    Dmole_flow = 103.75  # mole/hr
    Bmole_flow = 86.087  # mole/hr
    Dmass_flow = 5700  # kg/hr
    Bmass_flow = 4300  # kg/hr

    reflux = 2.25
    boilup = 3.77
    column_diameter = 1.8  # meters

    liquid_density = 723.15  # kg/m^3
    vapor_density = 2.9  # kg/m^3
    molecular_weight = 54.93  # kg/kmole (average molecular weight)
    surface_tension = 25.9  # mN/m

    # Scaled-up base collumn ----------------------------------------------------------------------
    Dmole_flow2 = 103.75 * 1.33  # mole/hr
    Bmole_flow2 = 86.087 * 1.33  # mole/hr
    Dmass_flow2 = 5700 * 1.33  # kg/hr
    Bmass_flow2 = 4300 * 1.33  # kg/hr

    reflux2 = 2.25
    boilup2 = 3.78
    column_diameter2 = 1.8  # meters

    liquid_density2 = 723.15  # kg/m^3
    vapor_density2 = 2.9  # kg/m^3
    molecular_weight2 = 54.93  # kg/kmole (average molecular weight)
    surface_tension2 = 25.9  # mN/m

    # Optimal Scheme ----------------------------------------------------------------------
    Dmole_flow3 = 103.75 * 1.33  # mole/hr
    Bmole_flow3 = 86.087 * 1.33  # mole/hr
    Dmass_flow3 = 5700 * 1.33  # kg/hr
    Bmass_flow3 = 4300 * 1.33  # kg/hr

    reflux3 = 1.05
    boilup3 = 2.378
    column_diameter3 = 1.8  # meters

    liquid_density3 = 742  # kg/m^3
    vapor_density3 = 2.09  # kg/m^3
    molecular_weight3 = 54.93  # kg/kmole (average molecular weight)
    surface_tension3 = 29.6  # mN/m

    # Instantiate the distillation columns
    column = DistillationColumn(column_diameter, Dmole_flow, Bmole_flow, Dmass_flow, Bmass_flow,
                                reflux, boilup, liquid_density, vapor_density, molecular_weight, surface_tension)

    column2 = DistillationColumn(column_diameter2, Dmole_flow2, Bmole_flow2, Dmass_flow2, Bmass_flow2,
                                 reflux2, boilup2, liquid_density2, vapor_density2, molecular_weight2, surface_tension2)

    column3 = DistillationColumn(column_diameter3, Dmole_flow3, Bmole_flow3, Dmass_flow3, Bmass_flow3,
                                 reflux3, boilup3, liquid_density3, vapor_density3, molecular_weight3, surface_tension3)

    # Simulate the columns
    result = column.simulate()
    print("Base Column Simulation Results:")
    print(f"Flooding Velocity (ft/s): {result['flooding_velocity']:.2f}")
    print(f"Operating Velocity (ft/s): {result['operating_velocity']:.2f}")
    print(f"Flooding Percentage: {result['flooding_percentage']:.2f}%\n")

    result = column2.simulate()
    print("Scaled Column Simulation Results:")
    print(f"Flooding Velocity (ft/s): {result['flooding_velocity']:.2f}")
    print(f"Operating Velocity (ft/s): {result['operating_velocity']:.2f}")
    print(f"Flooding Percentage: {result['flooding_percentage']:.2f}%")

    print("")
    result = column3.simulate()
    print("Scaled Column Simulation Results:")
    print(f"Flooding Velocity (ft/s): {result['flooding_velocity']:.2f}")
    print(f"Operating Velocity (ft/s): {result['operating_velocity']:.2f}")
    print(f"Flooding Percentage: {result['flooding_percentage']:.2f}%")


