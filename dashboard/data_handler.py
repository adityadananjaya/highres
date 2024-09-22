import pandas as pd

def get_results():
    results_4mp = pd.read_csv('data/4mpresults.csv')
    results_16mp = pd.read_csv('data/16mpresults.csv')
    results_64mp = pd.read_csv('data/64mpresults.csv')
    results = pd.concat([results_16mp, results_4mp, results_64mp])
    return results

def get_labeled_results():
    metrics_4mp = pd.read_csv('data/4mp-labeled-results.csv')
    curves_4mp = pd.read_json('data/4mp-labeled-results.json')
    
    metrics_16mp = pd.read_csv('data/16mp-labeled-results.csv')
    curves_16mp = pd.read_json('data/16mp-labeled-results.json')

    metrics_4mp['resolution'] = 4
    metrics_16mp['resolution'] = 16

    metrics = pd.concat([metrics_4mp, metrics_16mp])
    curves = pd.concat([curves_4mp, curves_16mp])

    return (metrics, curves)