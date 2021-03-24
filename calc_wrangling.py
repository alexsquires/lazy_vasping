import os
from pymatgen.io.vasp import Incar

def wrangle_incar(directory, calculation_parameters_to_update):
   """
   updating an incar file in a given directory, with a given set of flags and values
   args:
       directory (str): directory to update INCAR in
       calculation_parameters_to_update (dict): dictionary of calc paramters to be changed, where the key
       is the relevant VASP flag, and the values are the incar values.
   """
    home=os.getcwd()
    incar = Incar.from_file(f'{home}/{directory}/INCAR')
    incar.update(calculation_parameters_to_update)
    incar.write_file(f'{home}/{directory}/INCAR')
