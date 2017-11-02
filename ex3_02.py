import sys
import networkx as nx
# import _pickle as pickle
import csv
import numpy as np
from graph_tool.all import *
# import cPickle as pickle


raw_twitter_small_dataset = 'data/twitter-small.in'
csv_twitter_small_dataset = "csv/twitter-small.csv"
csv_graph_tool_twitter_small_dataset = 'csv/csv_graph_tool_twitter-small.csv'


raw_twitter_large_dataset = 'data/twitter-large.in'
csv_twitter_large_dataset = "csv/twitter-large.csv"
csv_graph_tool_twitter_large_dataset = 'csv/csv_graph_tool_twitter-large.csv'


def number_of_edges(graph, title):
    print('Number of Edges')
    print(title + ": " + str(nx.number_of_edges(graph)))
    print('\n')


def number_of_nodes(graph, title):
    print("Number of Nodes")
    print(title + ": " + str(nx.number_of_nodes(graph)))
    print('\n')


def network_density(graph, title):
    print('Network Density')
    print(title + ': ' + str(nx.density(graph)))
    print('\n')


def in_degree_distribution(DiGraph, title, filename):
    in_degrees = DiGraph.in_degree().values()
    bin_count = np.bincount(np.array(in_degrees))
    dump(bin_count, filename)
    print("In Degree Distribution " + title + " \n")
    # print(bin_count)
    # print("\n")


def out_degree_distribution(DiGraph, title, filename):
    out_degree = DiGraph.out_degree().values()
    bin_count = np.bincount(np.array(out_degree))
    dump(bin_count, filename)
    print("Out Degree Distribution " + title + " \n")
    print(bin_count)
    print("\n")


def number_of_weakly_connected_components(graph, title):
    print("Number of weakly connected components")
    print(title + ": " + str(nx.number_weakly_connected_components(graph)))
    print("\n")


def number_of_strongly_connected_components(graph, title):
    print('Number of strongly connected components')
    print(title + ": " + str(nx.number_strongly_connected_components(graph)))


def get_largest_component(graph, title, filename):
    number_of_edges(graph, title)
    number_of_nodes(graph, title)
    network_density(graph, title)
    in_degree_distribution(graph, title, filename)
    out_degree_distribution(graph, title, filename)


def save_large_comp(graph, filename):
    """
    Save the largest file
    """
    nx.write_weighted_edgelist(graph, filename, delimiter=",")


def aprox_distance_distribution(graph, filename):
    l = graph_tool.topology.label_largest_component(graph)
    u = graph_tool.topology.GraphView(graph, vfilt=l)

    dist = graph_tool.stats.distance_histogram(u)

    dump(dist[0], filename)
    print("Distance Distribution:")
    print(dist[0])
    print("\n")


def parse_file_to_digraph(filename):
    """
    Create a Di graph. 
    """
    dg = nx.DiGraph()
    with open(filename, 'r') as files:
        for line in files:
            line = line.rstrip('\n')
            v = line.split(",")

            dg.add_edge(v[0], v[1], {'weight': v[2], 'timestamp': v[3]})

    return dg


def parse_file_to_graph_tool_digraph(filename):
    """
    """
    g = Graph()

    with open(filename, 'r') as file:
        file_reader = csv.reader(file, delimiter=',', quotechar='|')

        next(file_reader)

        for i in file_reader:
            g.add_edge(i[0], i[1])

    return g


def dump(picle, filename):
    pickle.dump(picle, open(filename, 'wb'))


def main():
    # small_to_graph_tool = parse_file_to_graph_tool_digraph(csv_graph_tool_twitter_small_dataset)
    # aprox_distance_distribution(small_to_graph_tool, 'pickles/Small_Distance_Histogram.pickle')

    small = parse_file_to_digraph(csv_twitter_small_dataset)
    # number_of_nodes(small, "Small Network")
    # number_of_edges(small, 'Small Network')
    # network_density(small, "network Density")
    # number_of_weakly_connected_components(small, "Small Network")
    # number_of_strongly_connected_components(small, "Small Network")

    # smallest = max(nx.weakly_connected_component_subgraphs(small), key=len)
    # get_largest_component(smallest, "Smallest Component - Small Network", 'pickles/Largest_Small_In_Degree_Distribution.pickle')

    # in_degree_distribution(small, "Small network", "pickles/Small_In_Degree_Distribution.pickle")
    # out_degree_distribution(small, "Small network", "pickles/Small_Out_Degree_Distribution.pickle")

    # Large
    large = parse_file_to_digraph(csv_twitter_large_dataset)
    # number_of_nodes(large, "Large Network")
    # number_of_edges(large, 'Large Network')
    # network_density(large, "network Density")
    # number_of_weakly_connected_components(large, "Large Network")
    # number_of_strongly_connected_components(large, "Large Network")

    largest = max(nx.weakly_connected_component_subgraphs(large), key=len)
    get_largest_component(largest, "Largest Component large Network",
                          'pickles/Largest_large_In_Degree_Distribution.pickle')
    # in_degree_distribution(large, "large network", "pickles/large_In_Degree_Distribution.pickle")
    # out_degree_distribution(large, "large network", "pickles/Small_Out_Degree_Distribution.pickle")


if __name__ == '__main__':
    main()
