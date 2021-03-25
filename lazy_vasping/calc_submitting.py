import os, re, glob

def find_new_vasp_calculations():
    """
    Returns a list of all subdirectories that contain an INCAR file, a job.sh,
    but then don't contain a vasprun.xml
    Args:
        None
    Returns:
        (List): list of all new VASP calculation subdirectories.
    """
    incar_list = [ './' + re.sub( r'INCAR', '', path ) for path in glob.iglob( '**/INCAR', recursive=True ) ]
    job_list = [ './' + re.sub( r'job.sh', '', path ) for path in glob.iglob( '**/job.sh', recursive=True ) ]
    vr_list = [ './' + re.sub( r'vasprun\.xml', '', path ) for path in glob.iglob( '**/vasprun.xml', recursive=True ) ] 
    incar_job_not_vr = [item for item in incar_list + job_list if item not in vr_list and item in incar_list and item in job_list]
    return list(set(incar_job_not_vr))

def restart_job(directory):
    """
    restart jobs from a previous stable run
    args:
        - directory (str): directory containing the calculation to resubmit
    returns:
        - None
    """
    home=os.getcwd()
    os.chdir(directory)
    if os.path.exists(f'queued'):
        os.chdir(home)
    else:
        os.system('touch queued ; mv CONTCAR POSCAR; qsub job.sh')
        os.chdir(home)

def submit_job(directory):
    """
    restart jobs from a previous stable run
    args:
        - directory (str): directory containing the calculation to resubmit
    returns:
        - None
    """
    home=os.getcwd()
    os.chdir(directory)
    if os.path.exists(f'queued'):
        os.chdir(home)
    else:
        os.system('touch queued ; qsub job.sh')
        os.chdir(home)
