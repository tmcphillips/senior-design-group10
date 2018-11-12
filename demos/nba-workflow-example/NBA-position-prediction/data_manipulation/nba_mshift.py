# create clusters and visualize our data from stats.nba.com
from sklearn.cluster import MeanShift
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from itertools import cycle

def nba_mshift(df):
    X = df.as_matrix(columns=df.columns[1:23])

    ms = MeanShift(bin_seeding=False)
    ms.fit(X)
    labels = ms.labels_
    cluster_centers = ms.cluster_centers_

    labels_unique = np.unique(labels)
    n_clusters_ = len(labels_unique)

    clusters_estimate = "number of estimated clusters : %d" % n_clusters_

    plt.figure(1)
    plt.clf()

    colors = cycle('bgrcmykbgrcmykbgrcmykbgrcmyk')
    for k, col in zip(range(n_clusters_), colors):
        my_members = labels == k
        cluster_center = cluster_centers[k]
        plt.plot(X[my_members, 0],X[my_members, 1], col + '.')
        plt.plot(cluster_center[0], cluster_center[1], 'o', markerfacecolor=col,
                markeredgecolor='k', markersize=14)
    plt.title('Estimated number of clusters: %d' % n_clusters_)
    plt.savefig("nba_graphspca_data_mshift.png")

    return clusters_estimate

if __name__ == "__main__":
    df = pd.read_csv("nba_data")
    nba_mshift(df)
