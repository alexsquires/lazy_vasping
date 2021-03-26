import shutil, os
import yaml
from pymatgen.io.vasp import Incar, Potcar

def calc_store(init_directory, final_directory, files=['INCAR','POSCAR','OUTCAR','vasprun.xml'], potcar_spec=True):
    """
    move minimal vasp io from an initial directory to
    target directory. Will automatically determine if KSPACING was used, and
    if not, also copy KPOINTS file.
    args: 
        - init_directory (str): dicrectory to copy from
        - final_directory (str): directory to copy to
        - files (list): list of files to copy (default is INCAR, POSCAR, OUTCAR, and vasprun)
        - potcar_space (bool): set to False if you want the POTCAR itself copied.
                               if you would prefer a POTCAR.spec, leave as True
    returns:
        - None
    """
    os.makedirs(final_directory)
 
    incar = Incar.from_file(f'{init_directory}/INCAR')
    for k in incar.keys():
        if k == 'KSPACING':
            kspacing = True
            break
        else:
            kspacing = False
    if kspacing == False:
        files += ['KPOINTS']
    
    if potcar_spec == True:
        potcar = Potcar.from_file(f'{init_directory}/POTCAR')
        spec = potcar.spec
        with open(f'{init_directory}/POTCAR_spec.yaml', 'w') as outfile:
            yaml.dump(spec, outfile, default_flow_style=False)
        files += ['POTCAR_spec.yaml']
    else: 
        files += ['POTCAR'] 
    for file_to_copy in files:
        shutil.copy(f'{init_directory}/{file_to_copy}', final_directory)
