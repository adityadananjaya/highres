import pandas as pd

def get_results():
    results_4mp = pd.read_csv('data/4mpresults.csv')
    results_16mp = pd.read_csv('data/16mpresults.csv')
    results_64mp = pd.read_csv('data/64mpresults.csv')
    results = pd.concat([results_16mp, results_4mp, results_64mp])
    return results

def get_labeled_results():
    metrics = pd.read_csv('data/16mp-labeled-results.csv')
    curves = pd.read_json('data/16mp-labeled-results.json')
    return (metrics, curves)