import time, os
import numpy as np
from vasppy.summary import find_vasp_calculations
from pymatgen.io.vasp import Poscar, Xdatcar, Vasprun

def assess_stdout(directory):
    """
    Parses the std_out (it is assumed it is named "vasp_out") and reports any found errors.
    """
    with open('/home/mmm0558/templates/errors.yaml') as all_errors:
        all_errors = yaml.load(all_errors)
    errors = []
    errors_subset_to_catch = list(all_errors.keys())
    with open(f'{directory}/vasp_out') as handler:
        for line in tqdm(handler):
            l = line.strip()  #pylint: disable=invalid-name
            for err, msgs in all_errors.items():
                for msg in msgs:
                    if l.find(msg) != -1:
                        errors.append(err)
    #if any(errors) == False:
    #    errors = False
    return errors

def assess_OUTCAR(directory):
    if os.path.exists(f'{directory}/OUTCAR'):
        try:
            outcar = file_age(f'{directory}/OUTCAR')
        except:
            outcar = None
    else:
        outcar = None
    return outcar
  
def file_age(filepath):
    """
    given a file, determines the last time that file was updated in seconds
    args:
        - filepath (str): path to file
    returns:
        - time (float): time since file last modified in seconds
    """
    time = time.time() - os.path.getmtime(filepath)
    return time
  
def assess_CONTCAR(directory):
  """
  asseses whether a directory contains a properly formatted vasp contcar
  args:
      - directory (str): directory to check for CONTCAR
  returns:
      - contcar (bool): whether the directory contains a readable CONTCAR
  """
  if os.path.exists(f'{directory}/CONTCAR'):
      try:
          Poscar.from_file(f'{directory}/CONTCAR')
          contcar = True
      except:
          contcar = False
  else:
      contcar = False
  return contcar
  
def assess_XDATCAR(directory):
  """
  reports how many ionic steps a calculation has run for by reading the XDATCAR (cannot always rely on vasprun, as it is unreadable if the caluclation is unfinished)
  args:
      - directory (str): directory to check for XDATCAR
  returns:
      - xdatcar (int): the number of steps saved to the XDATCAR
  """
  if os.path.exists(f'{directory}/XDATCAR'):
      try:
          xdatcar = len(Xdatcar(f'{directory}/XDATCAR').structures)
      except:
          xdatcar = None
  else:
      xdatcar = None
  return xdatcar

def assess_vasprun(directory):
    """
    checks whether calculations completed, and converged
    args:
      - directory (str): directory to check for vasprun.xml
    returns:
      - contcar (bool): whether the directory contains a converged vasprun
    """
    if os.path.exists(f'{directory}/vasprun.xml'):
        try:
            vasprun = Vasprun(f'{directory}/vasprun.xml', parse_eigen=False, parse_dos=False).converged
        except:
            vasprun = False
    else:
        vasprun = False
    return vasprun

def parse_calcs():
    calculation_status = {}
    home = os.getcwd()
    entries = []
    calculations = find_vasp_calculations()
    for calc_dir in calculations:
        calc_status = {'converged':assess_vasprun(f'{home}/{calc_dir}'),
                       'errors':assess_stdout(f'{home}/{calc_dir}'),
                       'contcar':assess_CONTCAR(f'{home}/{calc_dir}'),
                       'ionic_steps':assess_XDATCAR(f'{home}/{calc_dir}'),
                       'last_updated': assess_OUTCAR(f'{home}/{calc_dir}')}
        calculation_status.update({calc_dir:calc_status})
    df = pd.DataFrame.from_dict(calculation_status, orient='index')
    df.to_csv('calc_data.csv')
