from pymatgen.io.vasp import Vasprun, Outcar
import json
import pandas as pd
from tqdm import tqdm

def main():
    df = pd.read_csv('calc_data.csv')
    converged = df[df["converged"] == True]

    print(df)
    print(f"""

    ------------
    ------------
    
    {len([i for i in df["converged"] if i == True])} / {len(df["converged"])} calculations converged
    {len([i for i in df["errors"] if len(list(i)) > 2])} calculations reporting an error

    {len([i for i in converged["ionic_steps"] if i <= 10])} / {len(df["converged"])} calculations ready to scrape

    """)
if __name__ == "__main__":
    main()
