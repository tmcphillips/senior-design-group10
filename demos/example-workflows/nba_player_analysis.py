import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cluster import MeanShift
from sklearn.decomposition import PCA

import visualize_nba
from nba_mshift import nba_mshift
from nba_reducer import dimension_reducer

# @BEGIN main
# @IN nba_data
# @OUT mean_shift_visualization @URI file:nba_graphs/mean_shift_cluster_plot.png
# @OUT prediction_score @URI file:nba_analysis_output.txt
# @OUT scatter_plot @URI file:nba_graphs/nba-data-scattermatrix.png
# @OUT pair_wise_plot @URI file:nba_graphs/pairwise_nba.png
# @OUT correlation_heatmap @URI file:nba_graphs/heatmap_nba.png
def main():
    with open("nba_analysis_output.txt", "a") as analysis_output:
        df = pd.read_csv("extracted_nba_position_data/nba_data")

        # @BEGIN pca_analysis
        # @IN nba_data
        # @OUT pair_wise_plot
        dimension_reducer(df)
        # @END pca_analysis

        # @BEGIN mshift
        # @IN nba_data
        # @OUT mshift_graph
        analysis_output.write(nba_mshift(df))
        # @END mshift

        # @BEGIN scatter_matrix
        # @IN nba_data
        # @OUT scatter_matrix
        visualize_nba.scatter_matrix(df)
        # @END scatter_matrix

        # @BEGIN scatter_plot
        # @IN nba_data
        # @OUT scatter_plot
        visualize_nba.scatter_nba(df)
        # @END scatter_plot

        # @BEGIN correleation_heat_map
        # @IN nba_data
        # @OUT correlation_heat_map
        visualize_nba.correlation_heat_map_nba(df)
        # @END correlation_heat_map
main()
# @END main
