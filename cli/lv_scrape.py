from pymatgen.io.vasp import Vasprun, Outcar
import json
import pandas as pd
import argparse
import numpy as np
from tqdm import tqdm

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--force')
    parser.add_argument('-d', '--dos')
    parser.add_argument("-ei", "--eps_i") 
    args = parser.parse_args()

    df = pd.read_csv('calc_data.csv')
    converged = df['converged'] == True
    few_steps = df['ionic_steps'] < 10

    if args.force:
        to_scrape = df.iloc[:, 0]
    else:
        to_scrape = list(df[converged & few_steps].iloc[:, 0])

    converged_calculations = []
    for converged_calculation in tqdm(to_scrape): 
        vr = Vasprun(f'{converged_calculation}/vasprun.xml', parse_potcar_file=False)
        
        data = ["incar"]
        if args.dos:
           data.append("complete_dos")
        if args.eps_i:
           data.append("epsilon_ionic")
        entry = vr.get_computed_entry(data = data)
        entry.entry_id = converged_calculation
        entry_dict = entry.as_dict()
        
        if vr.parameters['LORBIT'] == 11:
            outcar = Outcar(f'{converged_calculation}/OUTCAR')
            entry_dict.update({'MAGMOMS': outcar.magnetization})
        
        if vr.parameters["LOPTICS"] == True:
            outcar = Outcar(f'{converged_calculation}/OUTCAR')
            outcar.read_freq_dielectric()
            eps_elec = np.real(outcar.dielectric_tensor_function[0]).tolist()
            entry_dict.update({'eps': eps_elec}) 
            
        converged_calculations.append(entry_dict)

    with open('calculation_data.json', 'w') as calc_data:
        json.dump(converged_calculations, calc_data)

if __name__ == "__main__":
    main()
