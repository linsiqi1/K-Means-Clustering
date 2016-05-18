# Name: 		Siqi Lin
# Instructor: 	Maksym Morawski
# Class: 		CMSC 471
# Assignment: 	Project 4
# Reference: http://matplotlib.org/examples/shapes_and_collections/scatter_demo.html
#            http://stanford.edu/~cpiech/cs221/handouts/kmeans.html
#            http://docs.scipy.org/doc/numpy-1.10.1/reference/generated/numpy.random.rand.html
#            http://www.real-statistics.com/multivariate-statistics/cluster-analysis/k-means-cluster-analysis/
#            http://matplotlib.org/examples/pylab_examples/scatter_star_poly.html
from __future__ import print_function
import sys, getopt
import random
import collections
import matplotlib.colors as colors
import matplotlib.pyplot as plt
import numpy as np


def read_file(filename):

    coord = []
    infile = open(filename, 'r')
    for line in infile:
        line = line.split()
        coord.append((float(line[0]), float(line[1])))

    np_coord = np.asarray(coord)
    return np_coord


def get_min_max(coord):
    x_coord = []
    y_coord = []

    for i in coord:
        x_coord.append(i[0])
        y_coord.append(i[1])

    x_min = min(x_coord)
    y_min = min(y_coord)
    x_max = max(x_coord)
    y_max = max(y_coord)

    return x_min, x_max, y_min, y_max

def get_rand_centroids(clusters, coord):

    centroids = []
    x_min, x_max, y_min, y_max = get_min_max(coord)
    for i in range(0,clusters):
        point = (random.uniform(x_min, x_max), random.uniform(y_min, y_max))
        centroids.append(point)

#    print("centroids",centroids)
    np_centroids = np.asarray(centroids)
    return np_centroids


def set_cluster(coord, centroids):

    cluster = [0]*len(coord)
    num_plots = len(coord)
    num_cluster = len(centroids)
    
    for i in range(0, num_plots):
        current_dis = 99999
        for j in range(0, num_cluster):
            #use a distance function to set the most appropriate cluster
            distance = (((centroids[j][0]-coord[i][0])**2) + ((centroids[j][1]-coord[i][1])**2))**(0.5)
            if(distance < current_dis):
                current_dis = distance
                cluster[i] = j
                
    np_cluster = np.asarray(cluster)
    
    return np_cluster

def set_centroids(coord, np_centroids,cluster):
    
    num_cluster = len(np_centroids)
    centroids = []
    
    
    while(num_cluster):
        label = num_cluster - 1
        label_count = 0
        x_total = 0
        y_total = 0
        cluster_empty = True
        # Calculate the sum of the coordinates in one cluster
        for i in range(0, len(cluster)):
            if(cluster[i] == label):
                x_total = x_total + coord[i][0]
                y_total = y_total + coord[i][1]
                # keep track of the total number of points in a cluster
                label_count = label_count + 1
                cluster_empty = False
        # Calculate the average point if cluster has points
        if(cluster_empty == False):
            centroids.append((x_total/label_count, y_total/label_count))
        else:
            #cluster is empty, reinitialize a random centroids
            x_min, x_max, y_min, y_max = get_min_max(coord)
            centroids.append((random.uniform(x_min, x_max), random.uniform(y_min, y_max)))
        num_cluster = num_cluster - 1
        
    return centroids
    
def k_means(coord, centroids, clusters):
    
    k_means_done = False
    num_iteration = 0
    max_iteration = 300
    # Keep looping until a right centroid is found
    while(not k_means_done and num_iteration < max_iteration):
        num_iteration = num_iteration + 1
        prev_clusters = clusters
        #find centroid
        centroids = set_centroids(coord, centroids, prev_clusters)
        #set clusters for each coord based on the new centroid
        clusters = set_cluster(coord,centroids)
        if(np.array_equal(prev_clusters,clusters)):
            k_means_done = True
        
    return centroids, clusters

def output_graph(coord, centroids, clusters, num_clusters):
    
    x_coord = []
    y_coord = []
    
    # Divide the coordinates into x and y coordiantes
    for i in coord:
        x_coord.append(i[0])
        y_coord.append(i[1])
    np_x = np.asarray(x_coord)
    np_y = np.asarray(y_coord)
      


    colors_option = []
    
    for i in range(num_clusters):
        colors_option.append('#'+'%06X' % random.randint(0, 0xFFFFFF))      

    np_centroids = np.asarray(centroids)
    while(num_clusters): 
        for i in range(len(coord)):
            if(clusters[i] == num_clusters-1):
                plt.scatter(np_x[i],np_y[i],color=colors.hex2color(colors_option[num_clusters-1]),s=6,alpha=0.5)
        #plot the centroids
        plt.scatter(np_centroids[num_clusters-1][0],np_centroids[num_clusters-1][1],
                   color=colors.hex2color(colors_option[num_clusters-1]), marker='>', s=150)
        num_clusters = num_clusters - 1

    plt.show()

def main():
    
    coord = []
    
    
    if len(sys.argv) != 3:
        print('Usage: python Clustering.py <numberOfClusters> <input file>')
    else:

        coord= read_file(sys.argv[2])
        num_clusters = int(sys.argv[1])
        centroids = get_rand_centroids(num_clusters, coord)    
        cluster_groups = set_cluster(coord, centroids)
    
        centroids, cluster_groups = k_means(coord,centroids,cluster_groups)
        output_graph(coord,centroids,cluster_groups, num_clusters)
    
main()

