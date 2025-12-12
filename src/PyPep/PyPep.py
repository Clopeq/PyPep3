import cantera as ct


class Solution:
    def __init__(self, infile: str = "gri30.yaml") -> None: 
        self._solution = ct.Solution(infile)
        self._OF = 1

    def __call__(self) -> ct.Solution:
        return self._solution
        
    def solve(self, fuel: ct.Quantity, ox: ct.Quantity) -> None:
        mix = fuel+self._OF*ox
        mix.equilibrate("HP")
        self._solution()

    def summarise(self):
        self._solution()

    
    ######## Methods to get/set the complete thermodynamic state ########

    @property
    def OF(self) -> float: return self._OF
    @OF.setter
    def OF(self, value: float | None):
        if(value != None): 
            self._OF = value      


    @property
    def TP(self) -> tuple[float, float]: return self._solution.TP
    @TP.setter
    def TP(self, value: tuple[float | None, float | None]) -> None: 
        ...
    @property
    def T(self) -> float: return self._solution.T
    @T.setter
    def T(self, value: float | None) -> None: 
        ...
    @property
    def P(self) -> float: return self._solution.P
    @P.setter
    def P(self, value: float | None) -> None: 
        ...

    @property
    def k(self) -> float: return self._solution.cp/self._solution.cv

    @property
    def cp(self) -> float: return self._solution.cp
    @property
    def cp_mass(self) -> float: return self._solution.cp_mass
    @property 
    def cp_mole(self) -> float: return self._solution.cp_mole
    @property
    def cv(self) -> float: return self._solution.cv
    @property
    def cv_mass(self) -> float: return self._solution.cv_mass
    @property 
    def cv_mole(self) -> float: return self._solution.cv_mole

    _temperature = 0
    _pressure = 0
    

class Phase():
    def __init__(self, solution: ct.Solution, mass = None, moles = None, constant = "UV") -> None: 
        self.state = solution.state
        self._solution = solution
        self._phase = ct.Quantity(solution)

        # A unique key to prevent adding phases with different species
        # definitions
        self._id = hash((solution.name,) + tuple(solution.species_names))

        if mass is not None:
            self._mass = mass
        elif moles is not None:
            self._moles = moles
        else:
            self._mass = 1.0

        if constant not in ('TP','TV','HP','SP','SV','UV'):
            raise ValueError(
                f"Constant {constant} is invalid. "
                "Must be one of 'TP','TV','HP','SP','SV', or 'UV'")
        self._constant = constant


    def __call__(self) -> ct.Quantity:
        return self._phase
    
    def equilibrate(self, XY=None, *args, **kwargs):
        """
        Set the state to equilibrium. By default, the property pair
        `self.constant` is held constant. See `ThermoPhase.equilibrate`.
        """
        if XY is None:
            XY = self._constant
        self._solution.equilibrate(XY, *args, **kwargs)
        self.state = self._phase.state

        
    ######## Methods to get/set the complete thermodynamic state ########      

    @property
    def phase(self):
        self._phase.state = self.state
        return self._phase

    @property
    def comp(self) -> dict: return self._phase.mass_fraction_dict()
    @comp.setter
    def comp(self, value: str | None) -> None: 
        if(value != None): 
            self._phase.Y = value            
    @property
    def comp_mole(self) -> dict: return self._phase.mole_fraction_dict()
    @comp_mole.setter
    def comp_mole(self, value: str | None) -> None: 
        if(value != None): 
            self._phase.X = value        
    @property
    def TP(self) -> tuple[float, float]: return self._phase.TP
    @TP.setter
    def TP(self, value: tuple[float | None, float | None]) -> None:
        self._phase.TP = value

    @property
    def k(self) -> float: return self._phase.cp/self._phase.cv

    @property
    def cp(self) -> float: return self._phase.cp
    @property
    def cp_mass(self) -> float: return self._phase.cp_mass
    @property 
    def cp_mole(self) -> float: return self._phase.cp_mole
    @property
    def cv(self) -> float: return self._phase.cv
    @property
    def cv_mass(self) -> float: return self._phase.cv_mass
    @property 
    def cv_mole(self) -> float: return self._phase.cv_mole


    def __imul__(self, other):
        self._mass *= other
        return self
    
    def __mul__(self, other):
        return Phase(self._solution, mass=self._mass * other, constant=self._constant)
    
    def __rmul__(self, other):
        return Phase(self._solution, mass=self._mass * other, constant=self._constant)
    
    def __iadd__(self, other):
        if self._id != other._id:
            raise ValueError(
                'Cannot add Quantities with different phase '
                f'definitions. {self._id} != {other._id}')
        if self._constant != other._constant:
            raise ValueError(
                "Cannot add Quantities with different "
                f"constant values. {self._constant} != {other._constant}")

        m = self._mass + other._mass
        Y = (self._phase.Y * self._mass + other._phase.Y * other._mass)
        if self._constant == 'UV':
            U = self._phase.int_energy + other._phase.int_energy
            V = self._phase.volume + other._phase.volume
            if self._phase.basis == 'mass':
                self._solution.UVY = U / m, V / m, Y
            else:
                n = self._moles + other._moles
                self._solution.UVY = U / n, V / n, Y
        else:  # self.constant == 'HP'
            dp_rel = 2 * abs(self.P - other.P) / (self.P + other.P)
            if dp_rel > 1.0e-7:
                raise ValueError(
                    'Cannot add Quantities at constant pressure when '
                    f'pressure is not equal ({self.P} != {other.P})')

            H = self._phase.enthalpy + other._phase.enthalpy
            if self._phase.basis == 'mass':
                self._solution.HPY = H / m, None, Y
            else:
                n = self._moles + other._moles
                self._solution.HPY = H / n, None, Y

        self.state = self._solution.state
        self._mass = m
        return self

    def __add__(self, other):
        newquantity = Phase(self._solution, mass=self._mass, constant=self._constant)
        newquantity += other
        return newquantity