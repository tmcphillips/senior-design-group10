import pandas as pd
from pandas.plotting import scatter_matrix
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

def scatter_nba(df):
    matplotlib.rc('figure', figsize=(10, 5))
    scatter_plot = scatter_matrix(
        df,
        figsize  = [20, 20],
        marker   = ".",
        s        = 0.6,
        diagonal = "kde"
    )

    for ax in scatter_plot.ravel():
        ax.set_xlabel(ax.get_xlabel(), fontsize = 20, rotation = 90)
        ax.set_ylabel(ax.get_ylabel(), fontsize = 20, rotation = 0)

    plt.savefig("nba_graphs/nba-data-scattermatrix.png")

def pairwise_nba(df):
    cols = ['pts','fgm','fga','fg%','3pm','3pa' ,'3p%','ftm','fta','ft%', 'oreb','dreb','reb','ast','stl','blk','tov','eff']
    pp = sns.pairplot(df[cols], size=1.8, aspect=1.8, diag_kind="kde")

    fig = pp.fig 
    fig.subplots_adjust(top=0.93, wspace=0.3)
    t = fig.suptitle('NBA Attributes Pairwise Plots', fontsize=14)
    fig.savefig("nba_graphs/pairwise_nba.png")

def correlation_heat_map_nba(df):
    f, ax = plt.subplots(figsize=(10, 6))
    corr = df.corr()
    hm = sns.heatmap(round(corr,2), annot=True, ax=ax, cmap="coolwarm",fmt='.2f',
                    linewidths=.05)
    f.subplots_adjust(top=0.93)
    t= f.suptitle('NBA Attributes Correlation Heatmap', fontsize=14)
    f.savefig("nba_graphs/heatmap_nba.png")

if __name__ == "__main__":
    df = pd.read_csv("clean_nba_data")
    scatter_matrix(df)
    pairwise_nba(df)
    correlation_heat_map_nba(df)
