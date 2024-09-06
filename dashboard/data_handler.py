import pandas as pd

def get_results():
    results_4mp = pd.read_csv('data/4mpresults.csv')
    results_16mp = pd.read_csv('data/16mpresults.csv')
    results_64mp = pd.read_csv('data/64mpresults.csv')
    results = pd.concat([results_16mp, results_4mp, results_64mp])
    return results