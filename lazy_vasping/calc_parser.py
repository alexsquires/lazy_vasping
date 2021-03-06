import time, os, yaml
import pandas as pd
from tqdm import tqdm
from vasppy.summary import find_vasp_calculations
from pymatgen.io.vasp import Poscar, Xdatcar, Vasprun
from pathlib import Path
from monty.serialization import loadfn

MODULE_DIR = Path(__file__).resolve().parent

def load_yaml_config(fname):
    config = loadfn(str(MODULE_DIR / ("%s" % fname)))
    if "PARENT" in config:
        parent_config = _load_yaml_config(config["PARENT"])
        for k, v in parent_config.items():
            if k not in config:
                config[k] = v
            elif isinstance(v, dict):
                v_new = config.get(k, {})
                v_new.update(v)
                config[k] = v_new
    return config

def assess_stdout(directory):
    """
    Parses the std_out (it is assumed it is named "vasp_out") and reports any found errors.
    args:
        - directory (str): directory to look for "vasp_out"
    returnes:
        - errors (list): list of error codes
    """  
    all_errors = load_yaml_config("errors.yaml")
    errors = []
    errors_subset_to_catch = list(all_errors.keys())
    with open(f'{directory}/vasp_out') as handler:
        for line in handler:
            l = line.strip() 
            for err, msgs in all_errors.items():
                for msg in msgs:
                    if l.find(msg) != -1:
                        errors.append(err)
    return errors
  
def file_age(filepath):
    """
    given a file, determines the last time that file was updated in seconds
    args:
        - filepath (str): path to file
    returns:
        - m_time (float): time since file last modified in seconds
    """
    m_time = time.time() - os.path.getmtime(filepath)
    return m_time

def assess_OUTCAR(directory):
    """
    asseses whether a directory contains an OUTCAR file
    args:
        - directory (str): directory to check for OUTCAR
    returns:
        - outcar_update_time (float): time in seconds since the OUTCAR was modified
    """
    if os.path.exists(f'{directory}/OUTCAR'):
        try:
            outcar_update_time = file_age(f'{directory}/OUTCAR')
        except:
            outcar_update_time = None
    else:
        outcar_update_time = None
    return outcar_update_time
  
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
    """
    find all vasp caluclations in directories "below" current directory and generate a ".csv"
    summarising the status of these calculations ("calc_data.csv")
    args:
        - None
    returns:
       - None
    """
    calculation_status = {}
    home = os.getcwd()
    entries = []
    calculations = find_vasp_calculations()
    for calc_dir in tqdm(calculations):
        calc_status = {'converged':assess_vasprun(f'{home}/{calc_dir}'),
                       'errors':assess_stdout(f'{home}/{calc_dir}'),
                       'contcar':assess_CONTCAR(f'{home}/{calc_dir}'),
                       'ionic_steps':assess_XDATCAR(f'{home}/{calc_dir}'),
                       'last_updated': assess_OUTCAR(f'{home}/{calc_dir}')}
        calculation_status.update({calc_dir:calc_status})
    df = pd.DataFrame.from_dict(calculation_status, orient='index')
    df.to_csv('calc_data.csv')
