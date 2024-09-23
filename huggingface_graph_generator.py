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
    for dataset in datasets_ref:
        """
        Average detections have an index of 0
        Average confidence have an index of 1
        """
        graph_model_data(dataset, "Average Detections", 0, model_stats)
        graph_model_data(dataset, "Average Confidence", 1, model_stats)
if __name__ == "__main__":
    generate_graph('/home/tsir/MachineLearning/capstone_project/models_performance_unlabelled.csv')