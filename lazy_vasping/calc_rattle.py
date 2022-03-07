import os
from pymatgen.io.vasp import Poscar

def rattle_structure(structure_file = 'POSCAR', perturbation = 0.15, outfile = 'POSCAR_rattled'):
   """
   apply a random perturbation to a structure
   args:
       structure file (string): structure to rattle
       perturbation (float): std of perturbation to apply 
       outfile (string): outfile saved name 
   """
   structure = Poscar.from_file(structure_file).structure
   structure.perturb(perturbation)
   structure.to(filename = outfile)
