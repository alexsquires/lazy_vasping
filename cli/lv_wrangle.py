import sys
import argparse
from vasppy.summary import find_vasp_calculations
from lazy_vasping.calc_wrangling import wrangle_incar

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--directories', default='all', type=list
                        help='directories (containing INCARs) to edit')
    parser.add_argument('-p', '--params', type=dict,
                        help='dictionary of parameters to update')
    args = parser.parse_args()

    directories = args.directories
    parameters_to_update = args.params
    
    if directories == 'all':
        directories = find_vasp_calculations()
    for directory in directories:
        wrange_incar(directory, paramters_to_updata)

if __name__ == "__main__":
    main()
