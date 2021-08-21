from pymatgen.io.vasp import Outcar, Vasprun, Poscar, Incar, Potcar
from pymatgen.io.vasp.sets import DictSet
import json, os
import pandas as pd
from tqdm import tqdm

static_params = {'ISIF':2, 'ISMEAR': -5, 'LREAL':False, 'NSW':0, 'IBRION':-1}
home = os.getcwd()

def main():
    df = pd.read_csv('calc_data.csv')
    converged = df['converged'] == True
    few_steps = df['ionic_steps'] < 10

    to_run = list(df[converged & few_steps].iloc[:, 0])

    converged_calculations = []
    for converged_calculation in tqdm(to_run):
        if os.path.exists(f'mkdir {converged_calculation}/../run.final') == False:
            os.system(f'mkdir {converged_calculation}/../run.final')
            outcar = Outcar(f'{converged_calculation}/OUTCAR')
            mags = [i['tot'] for i in outcar.magnetization]
            structure = Poscar.from_file(f'{converged_calculation}/CONTCAR').structure
            structure.add_site_property('magmom',mags)
            incar = Incar.from_file(f'{converged_calculation}/INCAR')
            incar.update(static_params)
            try:
                del incar['MAGMOM']
            except:
                None
            potcar = Potcar.from_file(f'{converged_calculation}/POTCAR')
            calculation = DictSet(structure,{'INCAR':incar,'POTCAR':potcar})
            calculation.incar.write_file(f'{converged_calculation}/../run.final/INCAR')
            calculation.poscar.write_file(f'{converged_calculation}/../run.final/POSCAR')
            os.system(f'cp {converged_calculation}/POTCAR {converged_calculation}/../run.final ; cp {converged_calculation}/job.sh {converged_calculation}/../run.final')
            os.system(f'touch {converged_calculation}/../run.final/vasp_out ; touch {converged_calculation}/../run.final/vasprun.xml')


if __name__ == "__main__":
    main()
