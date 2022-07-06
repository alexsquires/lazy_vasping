from pymatgen.io.vasp import Vasprun, Outcar
import json
import pandas as pd
from tqdm import tqdm
from vasppy.summary import find_vasp_calculations

def main(): 
    
    calculations = find_vasp_calculations()
    recovered_calcs = []
    for converged_calculation in tqdm(calculations):
        vr = Vasprun(f'{converged_calculation}/vasprun.xml', parse_potcar_file=False, parse_eigen = False, parse_dos = False)
        entry = vr.get_computed_entry()
        entry.entry_id = converged_calculation
        entry_dict = entry.as_dict()
       
        
        if vr.parameters['LORBIT'] == 11:
            outcar = Outcar(f'{converged_calculation}/OUTCAR')
            entry_dict.update({'MAGMOMS': outcar.magnetization})
        
        recovered_calcs.append(entry_dict)

    with open('restored_data.json', 'w') as calc_data:
        json.dump(recovered_calcs, calc_data)

if __name__ == "__main__":
    main()
