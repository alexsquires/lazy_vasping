import pandas as pd
from lazy_vasping.calc_submitting import restart_job, submit_job, find_new_vasp_calculations
import os


def main():
    df = pd.read_csv('calc_data.csv')
    converged = df['converged'] == True
    not_converged = df['converged'] == False
    contcar = df['contcar'] == True
    not_contcar = df['contcar'] == False
    many_steps = df['ionic_steps'] >= 10
    not_running = df['last_updated'] >= 1800

    home=os.getcwd()

    to_restart = list(df[contcar & many_steps & not_running].iloc[:, 0]) + list(df[not_converged & contcar & not_running].iloc[:, 0])
    to_submit = list(df[not_converged & not_contcar & not_running].iloc[:, 0]) + list(df[many_steps & not_running & not_contcar].iloc[:, 0])
 
    for directory in to_restart:
        restart_job(directory)
    for directory in to_submit:
        submit_job(directory)
    for directory in find_new_vasp_calculations():
        submit_job(directory)

if __name__ == "__main__":
    main()
