import sys
import argparse
from vasppy.summary import find_vasp_calculations
from lazy_vasping.calc_rattle import rattle_structure

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--initialstructure', default='POSCAR',
                        help='structure to rattle')
    parser.add_argument('-p', '--perturbation', type=float,
                        help='std of perturbation to apply to ionic positions', default = 0.15)
    parser.add_argument('-o', '--outfile',
                        help='name of structure to write')
    args = parser.parse_args()
    
    rattle_structure(args.initialstructure, args.perturbation, args.outfile)

if __name__ == "__main__":
    main()
