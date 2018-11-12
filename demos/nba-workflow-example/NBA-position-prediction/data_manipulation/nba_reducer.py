import numpy as np
from sklearn.decomposition import PCA
import pandas as pd
import matplotlib.pyplot as plt

def dimension_reducer(df):
    X = np.array([[-1, -1], [-2, -1], [-3, -2], [1, 1], [2, 1], [3, 2]])
    pca = PCA(n_components=18)

    X = df.as_matrix(columns=df.columns[1:23])
    y = df.as_matrix(columns=df.columns[:1]).ravel()
    X_r = pca.fit(X).transform(X)

    print(df.shape)

    print(pca.explained_variance_ratio_)  
    print(pca.singular_values_)  
    plot_pca(X_r, y)
    return X_r, y

def plot_pca(X, y):
    plt.figure()
    target_names = ['G', 'F', 'F-C', 'F-G', 'G-F', 'C-F', 'C']    
    colors = ['navy', 'turquoise', 'darkorange', 'blue', 'red', 'purple', 'green']
    lw = 2

    for color, i, target_name in zip(colors, [0, 1, 2, 3, 4, 5, 6], target_names):
        plt.scatter(X[y == i, 0], X[y == i, 1], color=color, alpha=.8, lw=lw,
                    label=target_name)
    plt.legend(loc='best', shadow=False, scatterpoints=1)
    plt.title('PCA of NBA dataset')
    plt.savefig("nba_graphs/nba_pca.png")
if __name__ == "__main__":
    df = pd.read_csv("extracted_nba_position_data/clean_nba_data")
    dimension_reducer(df)
