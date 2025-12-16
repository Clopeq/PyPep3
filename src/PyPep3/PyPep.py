from __future__ import annotations
import cantera as ct
import Rocketry_formulas as rf
import scipy.constants as const


# Phase is a wrapper for quantity
# Solution is a wrapper for Solution

class Solution:
    def __init__(self, infile="gri30.yaml", *args, **kwargs):
        self._solution = ct.Solution(infile, *args, **kwargs)
        self.__doc__ = self._solution.__doc__  # copies C-extension docstring

    def __getattr__(self, name):
        return getattr(self._solution, name)
    
    @property
    def n_species(self):
        """Number of species in the solution"""
        return self._solution.n_species
    
    def equilibrate(self, XY = "HP", *args, **kwargs):
        """Equilibrate the solution."""
        return self._solution.equilibrate(XY, *args, **kwargs)

    def solve(self, fuel: Phase, ox: Phase) -> Phase:
        fuel + ox
        self._solution.equilibrate("HP")
        #elf._solution()
        return Phase(self)
    
    def ct_solution(self) -> ct.Solution:
        return self._solution


class Phase(ct.Quantity):
    def __init__(self, solution: Solution, *args, **kwargs):
        super().__init__(solution.ct_solution(), *args, **kwargs)
    
    
    def __getattr__(self, name):
        return getattr(super(), name)
    
    @property
    def k(self):
        return self.cp/self.cv
    
    @property
    def Rs(self):
        return const.R/self.mean_molecular_weight*1000
    
    @property
    def M(self):
        return self.mean_molecular_weight

    @property
    def cstar(self):
        return rf.calculate_cstar_ideal(self.k, self.Rs, self.T)
    
    @property
    def comp(self):
        return self.mass_fraction_dict()