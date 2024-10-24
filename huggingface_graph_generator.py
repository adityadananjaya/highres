import pandas as pd
import matplotlib.pyplot as plt

def graph_model_data(dataset_name, stat, stat_idx, model_stats):
    """
    Produce the graphs
    Params
        dataset_name : String
        stat : String
            the statistic the graph is being generated over
        stat_idx : Int
            column containing the relevant statistics
        model_stats : dictionary
            the parsed data
    """
    models = []
    values = []

    # Obtain data
    for model in model_stats:
        models.append(model)
        values.append(model_stats[model][dataset_name][stat_idx])

    # Plot 
    plt.bar(models, values, color=['red', 'blue'], width=0.5)
    plt.title(stat + " over " + dataset_name + " dataset")
    plt.xlabel('Models')
    plt.ylabel(stat)
    # Save plots as images
    plt.savefig(stat + "_" + dataset_name + ".png")

def graph_trend(stat, stat_idx, model_stats):
    """
    Produce a trend over each dataset
    Params
        stat : String
            the statistic the graph is being generated over
        stat_idx : Int
            column containing the relevant statistics
        model_stats : dictionary
            the parsed data
    """
    models = []

    # Obtain models
    for model in model_stats:
        models.append(model)

    max_value = 0

    plt.figure()

    # Plot
    for model in models:
        values = []
        datasets = []
        for dataset in model_stats[model]:
            datasets.append(dataset)
            values.append(model_stats[model][dataset][stat_idx])
            if model_stats[model][dataset][stat_idx] > max_value:
                max_value = model_stats[model][dataset][stat_idx]
        plt.plot(datasets, values, label = model)

    plt.legend()
    plt.xlim(min(datasets), max(datasets))
    plt.ylim(0, max_value + 10*max_value/(max_value+10))
    plt.title(stat + " over compressions" )
    plt.xlabel("Compressions (%)")
    plt.ylabel(stat)
    plt.savefig(stat + "_" + "trend" + ".png")

def generate_graph(csv):
    """
    Generates graphs using matplotlib of the results
    Params
        csv : String
            data for the graphs
    """
    # Open CSV
    df = pd.read_csv(csv)
    model_stats = {}
    datasets_ref = []
    # Read CSV contents
    for index, row in df.iterrows():
        model_name = row['model']
        dataset = row['dataset']
        avg_detections_idx = float(row['average_detections'])
        avg_confidence_idx = float(row['average_confidence'])
        # Keep track of the datasets used
        if dataset not in datasets_ref:
            datasets_ref.append(dataset)
        # Create list of data
        val_ls = [avg_detections_idx, avg_confidence_idx]
        # Check if model is in model_stats
        if model_name not in model_stats:
            model_stats[model_name] = {}
            model_stats[model_name][dataset] = val_ls
        else:
            if dataset not in model_stats[model_name]:
                model_stats[model_name][dataset] = val_ls

    # for dataset in datasets_ref:
    #     """
    #     Average detections have an index of 0
    #     Average confidence have an index of 1
    #     """
    #     graph_model_data(dataset, "Average Detections", 0, model_stats)
    #     graph_model_data(dataset, "Average Confidence", 1, model_stats)

    graph_trend("Average Detections", 0, model_stats)
    graph_trend("Average Confidence", 1, model_stats)


def metrics_graph_generator(csv):
    """
    Generates graphs using matplotlib of the results
    Params
        csv : String
            data for the graphs
    """
    # Open CSV
    df = pd.read_csv(csv)
    model_stats = {}
    # Read CSV contents
    for index, row in df.iterrows():
        model_name = row['model']
        compression = row['compression']
        ap = row['AP']
        ar = row['AR']
        # Create list of data
        val_ls = [ap, ar]
        # Check if model is in model_stats
        if model_name not in model_stats:
            model_stats[model_name] = {}
            model_stats[model_name][compression] = val_ls
        else:
            if compression not in model_stats[model_name]:
                model_stats[model_name][compression] = val_ls

        graph_trend("Average Precision", 0, model_stats)
        graph_trend("Average Recall", 1, model_stats)

if __name__ == "__main__":
    generate_graph('/home/tsir/MachineLearning/capstone_project/models_performance_unlabelled.csv')
    metrics_graph_generator('/home/tsir/MachineLearning/capstone_project/huggingface_metrics.csv')