from pymatgen.io.vasp import Vasprun
import json
import pandas as pd
from tqdm import tqdm

def main():
    df = pd.read_csv('calc_data.csv')
    converged = df['converged'] == True
    few_steps = df['ionic_steps'] < 10 

    to_scrape = list(df[converged & few_steps].iloc[:, 0]) 
 
    converged_calculations = []
    for converged_calculation in tqdm(to_scrape):
        vr = Vasprun(f'{converged_calculation}/vasprun.xml')
        entry = vr.get_computed_entry()
        converged_calculations.append(entry.as_dict())
    
    with open('calculation_data.json', 'w') as calc_data:
        json.dump(converged_calculations, calc_data)

    print(f'{len(converged_calculations)} calculations scraped')
if __name__ == "__main__":
    main()
