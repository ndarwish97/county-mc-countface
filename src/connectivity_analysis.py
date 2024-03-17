import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import pdist, squareform
from sklearn.neighbors import NearestNeighbors
import pickle


def calculate_distances(centroids):
    """
    Calculate the pairwise Euclidean distances between points.

    :param centroids: numpy.ndarray, array of point coordinates.
    :return: numpy.ndarray, distance matrix.
    """
    # Compute the pairwise distances between points
    return pdist(centroids)


def plot_distance_histogram(distances, bins=100):
    """
    Plot a histogram of the distances.

    :param distances: numpy.ndarray, array of pairwise distances between points.
    :param bins: int, number of bins for the histogram.
    """
    plt.hist(distances, bins=bins)
    plt.title('Distance Histogram')
    plt.xlabel('Distance')
    plt.ylabel('Frequency')
    plt.show()


def plot_k_nearest_neighbors_histogram(centroids, k):
    """
    Plot a histogram of the distances to the k-nearest neighbors of each point.

    :param centroids: numpy.ndarray, array of point coordinates (2D).
    :param k: int, the number of nearest neighbors to consider.
    """
    # Create the k-NN model
    neigh = NearestNeighbors(n_neighbors=k + 1)  # k+1 because the point itself is included
    neigh.fit(centroids)

    # Find the k-nearest neighbors for each point
    distances, _ = neigh.kneighbors(centroids)

    # Exclude the distance to the point itself (which is 0)
    distances = distances[:, 1:]  # Take all rows and start from the second column

    # Flatten the array of distances and plot histogram
    plt.hist(distances.flatten(), bins=100)
    plt.title('Distance Histogram '+ str(k) + ' nearest neighbors')
    plt.xlabel('Distance')
    plt.ylabel('Frequency')
    plt.show()


# Example usage in if __name__ == "__main__":
if __name__ == "__main__":
    # open the centorids in '../outputs/example_centroids.pkl'
    with open('../outputs/example_centroids.pkl', 'rb') as f:
        centroids = pickle.load(f)

    # Calculate distances between centroids
    distances = calculate_distances(centroids)

    # Plot the distance histogram
    #plot_distance_histogram(distances)

    # Plot the distance histogram of the k-nearest neighbors
    plot_k_nearest_neighbors_histogram(centroids, 1)
    plot_k_nearest_neighbors_histogram(centroids, 2)
    plot_k_nearest_neighbors_histogram(centroids, 3)
    plot_k_nearest_neighbors_histogram(centroids, 10)
