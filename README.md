# PyPep3

A Python implementation of [ProPep](http://www.propep.com/), a rocket propulsion performance prediction software. PyPep3 provides a simplified, Pythonic interface for performing chemical equilibrium calculations and analyzing rocket propellant combustion.

## Overview

PyPep3 is designed to calculate thermodynamic properties of propellant combustion products, making it useful for:
- Rocket propulsion analysis and design
- Combustion chamber performance prediction
- Propellant selection and optimization
- Educational purposes in aerospace engineering

The package leverages the powerful [Cantera](https://cantera.org/) library for chemical kinetics and thermodynamics calculations, while providing a user-friendly API similar to ProPep.

## About ProPep

[ProPep](http://www.propep.com/) is a widely-used software tool in the rocket propulsion community for predicting the performance of rocket propellants. It calculates chemical equilibrium compositions and thermodynamic properties of combustion products. PyPep3 aims to provide similar functionality in a modern, open-source Python environment.

## How It Works

### Cantera Integration

PyPep3 is built on top of [Cantera](https://cantera.org/), an open-source suite of tools for problems involving chemical kinetics, thermodynamics, and transport processes. Cantera provides:

- **Chemical equilibrium calculations**: Determines the equilibrium composition of reaction products by minimizing Gibbs free energy
- **Thermodynamic properties**: Calculates temperature, pressure, enthalpy, entropy, specific heats, and other properties
- **Species database**: Includes extensive thermodynamic data for hundreds of chemical species
- **Phase models**: Supports gas, liquid, solid, and mixed-phase systems

PyPep3 wraps Cantera's core classes (`Solution` and `Quantity`) to provide a more intuitive interface for rocket propulsion applications. The wrapper classes add convenient properties like:
- `k` (γ): Specific heat ratio (cp/cv)
- `Rs`: Specific gas constant
- `M`: Mean molecular weight
- `cstar` (c*): Ideal characteristic velocity
- `comp`: Easy-to-use composition interface

### Input Files

PyPep3 uses Cantera's YAML input files, which contain thermodynamic data for chemical species. The package includes several standard input files in the `data/cantera/` directory, including:
- `gri30.yaml`: GRI-Mech 3.0 natural gas combustion mechanism
- `air.yaml`: Air and its components
- `h2o2.yaml`: Hydrogen-oxygen system
- And many more...

You can also create custom input files with your own species and thermodynamic data.

## Installation

Install PyPep3 directly from GitHub using pip:

```bash
pip install git+https://github.com/Clopeq/PyPep3.git
```

### Dependencies

PyPep3 requires the following packages:
- `numpy`: Numerical computing
- `scipy`: Scientific computing and constants
- `cantera`: Chemical kinetics and thermodynamics library
- `Rocketry_formulas`: Additional rocket propulsion formulas

These dependencies will be installed automatically when you install PyPep3.

## Usage

### Basic Example

Here's a minimal example calculating the adiabatic flame temperature of hydrogen and oxygen combustion:

```python
import PyPep3 as pep

# Initialize solution and phases
solution = pep.Solution()  # Uses default gri30.yaml
fuel = pep.Phase(solution)
ox = pep.Phase(solution)

# Set propellant composition and initial state
fuel.comp = "H2:1"              # Pure hydrogen
ox.comp = "O2:1"                # Pure oxygen
fuel.TP = 100, 40e5             # Temperature (K), Pressure (Pa)
ox.TP = 170, 42e5               

# Calculate combustion products (adiabatic, constant pressure)
gas = solution.solve(fuel, 5*ox)  # OF ratio = 5

# Access results
print(f"Adiabatic flame temperature: {gas.T:.1f} K")
print(f"Mean molecular weight: {gas.M:.2f} g/mol")
print(f"Specific heat ratio (γ): {gas.k:.3f}")
print(f"Characteristic velocity (c*): {gas.cstar:.1f} m/s")
```

### Step-by-Step Workflow

#### 1. Create a Solution Object

The `Solution` object manages thermodynamic calculations:

```python
import PyPep3 as pep

solution = pep.Solution()               # Default input file
solution = pep.Solution("gri30.yaml")   # Specify custom input file
```

#### 2. Define Reactants

Create `Phase` objects for each reactant (typically fuel and oxidizer):

```python
fuel = pep.Phase(solution)
ox = pep.Phase(solution)
```

#### 3. Set Composition

Define the chemical composition using the `comp` attribute:

```python
# As a string (species:proportion)
fuel.comp = "CH4:1"
ox.comp = "O2:0.21, N2:0.79"

# As a dictionary (species:proportion)
fuel.comp = {"CH4": 1.0}
ox.comp = {"O2": 0.21, "N2": 0.79}
```

**Note**: Values represent proportions (ratios) that are automatically normalized to mass fractions. They don't need to sum to 1.

#### 4. Set Initial Conditions

Specify temperature (K) and pressure (Pa):

```python
fuel.TP = 298, 101325  # 298 K, 1 atm
ox.TP = 298, 101325
```

#### 5. Set Oxidizer-to-Fuel Ratio

Control the mixture ratio:

```python
# Method 1: Set masses directly
fuel.mass = 1  # kg
ox.mass = 5    # kg (OF ratio = 5)

# Method 2: Use arithmetic operations
gas = solution.solve(fuel, 5*ox)  # OF ratio = 5

# Method 3: Use helper method
solution.set_of_ratio(fuel, ox, 5)  # Sets fuel.mass=1, ox.mass=5
```

#### 6. Calculate Equilibrium

Solve for combustion products:

```python
gas = solution.solve(fuel, ox)
```

This performs adiabatic combustion at constant enthalpy and pressure.

#### 7. Access Results

The returned `Phase` object contains all combustion properties:

```python
# Thermodynamic properties
print(f"Temperature: {gas.T} K")
print(f"Pressure: {gas.P} Pa")
print(f"Density: {gas.density} kg/m³")
print(f"Enthalpy: {gas.h} J/kg")

# Composition
print(f"Composition: {gas.comp}")  # Dictionary of species:mass_fraction

# Performance parameters
print(f"Specific heat ratio (γ): {gas.k}")
print(f"Specific gas constant: {gas.Rs} J/kg-K")
print(f"Mean molecular weight: {gas.M} g/mol")
print(f"Characteristic velocity: {gas.cstar} m/s")

# Specific heats
print(f"cp: {gas.cp} J/kg-K")
print(f"cv: {gas.cv} J/kg-K")
```

### Complete Example: N₂O/ABS Hybrid Rocket

```python
import PyPep3 as pep

# Initialize
solution = pep.Solution()
fuel = pep.Phase(solution)
ox = pep.Phase(solution)

# N2O/ABS hybrid rocket propellant
fuel.comp = "C:8, H:8"  # Simplified ABS composition
ox.comp = "N2O:1"       # Nitrous oxide

# Initial conditions
fuel.TP = 298, 10e5     # Room temp, 10 bar
ox.TP = 298, 50e5       # Room temp, 50 bar

# Set OF ratio to 8
solution.set_of_ratio(fuel, ox, 8)

# Calculate combustion
gas = solution.solve(fuel, ox)

# Display results
print("=" * 50)
print("COMBUSTION ANALYSIS RESULTS")
print("=" * 50)
print(f"Adiabatic flame temperature: {gas.T:.1f} K")
print(f"Combustion pressure: {gas.P/1e5:.1f} bar")
print(f"γ (gamma): {gas.k:.3f}")
print(f"Mean molecular weight: {gas.M:.2f} g/mol")
print(f"c* (characteristic velocity): {gas.cstar:.1f} m/s")
print(f"Specific gas constant: {gas.Rs:.1f} J/kg-K")
print(f"cp: {gas.cp:.1f} J/kg-K")
print(f"cv: {gas.cv:.1f} J/kg-K")
```

## Project Structure

```
PyPep3/
├── src/
│   └── PyPep3/
│       ├── __init__.py
│       └── PyPep.py         # Main module with Solution and Phase classes
├── data/
│   └── cantera/             # Thermodynamic input files
│       ├── gri30.yaml
│       ├── air.yaml
│       └── ...
├── tests/
│   └── tests.ipynb          # Usage examples and tests
├── setup.py                 # Installation configuration
└── README.md
```

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

This project is licensed under the MIT License.

## Acknowledgments

- [Cantera](https://cantera.org/) - The chemical kinetics library powering PyPep3
- [ProPep](http://www.propep.com/) - The original inspiration for this project
- [Rocketry_formulas](https://github.com/Clopeq/Rocketry_formulas) - Additional rocket propulsion calculations

## Related Resources

- [Cantera Documentation](https://cantera.org/documentation/index.html)
- [Cantera Python Examples](https://cantera.org/examples/python/index.html)
- [NASA CEA](https://www.grc.nasa.gov/www/CEAWeb/) - Another popular chemical equilibrium tool
- [ProPep Manual](http://www.propep.com/)