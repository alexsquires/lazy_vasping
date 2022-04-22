import sys
import argparse
from vasppy.summary import find_vasp_calculations
from lazy_vasping.calc_wrangling import wrangle_incar

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--directories', default='all',
                        help='directories (containing INCARs) to edit')
    parser.add_argument('-k', '--key', type=str,
                        help='key of flag to update')
    parser.add_argument('-v', '--value',
                        help='value of flag to update')
    args = parser.parse_args()

    directories = args.directories
    parameters_to_update = {args.key : args.value}
    
    if directories == 'all':
        directories = find_vasp_calculations()
    
    for directory in directories:
        wrangle_incar(directory, parameters_to_update)

if __name__ == "__main__":
    main()
