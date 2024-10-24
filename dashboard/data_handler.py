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

def load_datasets(data):
    metrics_list = []
    curves_list = []
    for dir, res in data:
        if dir.endswith(".csv"):
            metrics = pd.read_csv(dir)
            metrics['resolution'] = res
            metrics_list.append(metrics)
        elif dir.endswith(".json"):
            curves = pd.read_json(dir)
            curves['resolution'] = res
            curves_list.append(curves)

    metrics_concat = pd.concat(metrics_list)
    curves_concat = pd.concat(curves_list)

    return (metrics_concat, curves_concat)


def get_labeled_results():

    metrics, curves = load_datasets([
        ('data/4mp-sahi-labeled-results.csv', '4'),
        ('data/4mp-sahi-labeled-results.json', '4'),
        ('data/16mp-sahi-labeled-results.csv', '16'),
        ('data/16mp-sahi-labeled-results.json', '16'),
        ('data/64mp-labeled-results.csv', '64'),
        ('data/64mp-labeled-results.json', '64'),
        ('data/16mp-labeled-results-compressed-70.csv', '16 Compressed By 70%'),
        ('data/16mp-labeled-results-compressed-70.json', '16 Compressed By 70%'),
        ('data/16mp-labeled-results-compressed-80.csv', '16 Compressed By 80%'),
        ('data/16mp-labeled-results-compressed-80.json', '16 Compressed By 80%'),
        ('data/16mp-labeled-results-compressed-90.csv', '16 Compressed By 90%'),
        ('data/16mp-labeled-results-compressed-90.json', '16 Compressed By 90%'),
        ('data/64mp-labeled-results-uncompressed-trained.csv', '64'),
        ('data/64mp-labeled-results-uncompressed-trained.json', '64'),
        ('data/64mp-labeled-results-70.csv', '64 Compressed By 70%'),
        ('data/64mp-labeled-results-70.json', '64 Compressed By 70%'),
        ('data/64mp-labeled-results-80.csv', '64 Compressed By 80%'),
        ('data/64mp-labeled-results-80.json', '64 Compressed By 80%'),
        ('data/64mp-labeled-results-90.csv', '64 Compressed By 90%'),
        ('data/64mp-labeled-results-90.json', '64 Compressed By 90%')

    ])

    return (metrics, curves)