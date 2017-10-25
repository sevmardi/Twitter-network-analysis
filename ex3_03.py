import networkx as nx
import numpy as np
# import cPickle as pickle
import _pickle as pickle


raw_twitter_small_dataset = 'data/twitter-small.in'
csv_twitter_small_dataset = "csv/twitter-small.csv"
csv_graph_tool_twitter_small_dataset = 'csv/csv_graph_tool_twitter-small.csv'


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


def in_degree_centrality(file):
    print(nx.in_degree_centrality(file))


def out_degree_centrality(file):
    print(nx.out_degree_centrality(file))


def closeness_centrality(file):
    print(nx.closeness_centrality(file))


def dump(picle, filename):
    pickle.dump(picle, open(filename, 'wb'))

def main():
	small = parse_file_to_digraph(csv_twitter_small_dataset)
	in_degree_centrality(small)

if __name__ == '__main__':
    main()
