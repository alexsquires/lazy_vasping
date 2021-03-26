from lazy_vasping.calc_storage import calc_store
import os
import pandas as pd
from tqdm import tqdm

def main():
    os.mkdir('vasp_store')
    df = pd.read_csv('calc_data.csv')
    converged = df['converged'] == True
    to_store = list(df[converged].iloc[:, 0]) 
    to_store = [i[2:] for i in to_store] # cut "./" off the start of each file path
    
    for converged_calculation in tqdm(to_store): 
        calc_store(converged_calculation,f'vasp_store/{converged_calculation}')
       
    print(f'{len(converged_calculations)} calculations stored')
if __name__ == "__main__":
    main()
