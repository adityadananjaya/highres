import pandas as pd

def get_results():
    results_4mp = pd.read_csv('data/4mpresults.csv')
    results_16mp = pd.read_csv('data/16mpresults.csv')
    results_64mp = pd.read_csv('data/64mpresults.csv')

    results_4mp['resolution'] = '4'
    results_16mp['resolution'] = '16'
    results_64mp['resolution'] = '64'

    results = pd.concat([results_16mp, results_4mp, results_64mp])
    return results

def get_labeled_results():
    metrics_4mp = pd.read_csv('data/4mp-sahi-labeled-results.csv')
    curves_4mp = pd.read_json('data/4mp-sahi-labeled-results.json')
    metrics_16mp = pd.read_csv('data/16mp-sahi-labeled-results.csv')
    curves_16mp = pd.read_json('data/16mp-sahi-labeled-results.json')
    metrics_64mp = pd.read_csv('data/64mp-labeled-results.csv')
    curves_64mp = pd.read_json('data/64mp-labeled-results.json')
    
    metrics_4mp['resolution'] = '4'
    metrics_16mp['resolution'] = '16'
    metrics_64mp['resolution'] = '64'
    curves_4mp['resolution'] = '4'
    curves_16mp['resolution'] = '16'
    curves_64mp['resolution'] = '64'

    

    metrics = pd.concat([metrics_4mp, metrics_16mp, metrics_64mp])
    curves = pd.concat([curves_4mp, curves_16mp, curves_64mp])

    return (metrics, curves)