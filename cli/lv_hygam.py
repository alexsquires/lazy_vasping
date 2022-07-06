import sys, os, argparse
from pymatgen.io.vasp import Incar, Poscar, Kpoints
from vasppy.summary import find_vasp_calculations
from copy import deepcopy

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--directories', default='all',
                        help='directories (containing INCARs) to edit')
    args = parser.parse_args()

    directories = args.directories
    parameters_to_update = {"GGA" : "PE",
                            "ISYM" : 3,
                            "PRECFOCK" : "Fast",
                            "LMAXFOCK" : 4,
                            "TIME" : 0.30,
                            "LHFCALC": True,
                            "AEXX" : 0.25,
                            "HFSCREEN": 0.2}

    if directories == 'all':
        directories = find_vasp_calculations()
    
    for directory in directories:
        incar = Incar.from_file(f"{directory}/INCAR").as_dict()
        incar = deepcopy(incar)  
        to_del = [i for i in incar.keys() if "LDA" in i]
        for d in to_del:
            incar.pop(d)
        new_incar = Incar.from_dict(incar | parameters_to_update) 
        os.mkdir(f"{directory}/hygam")
        new_incar.write_file(f"{directory}/hygam/INCAR")
        structure = Poscar.from_file(f"{directory}/CONTCAR").structure
        structure.to(filename = f"{directory}/hygam/POSCAR")
        os.system(f"cp {directory}/POTCAR {directory}/hygam/POTCAR")
        Kpoints().write_file(f"{directory}/hygam/KPOINTS")

if __name__ == "__main__":
    main()
