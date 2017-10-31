import networkx as nx
import numpy as np
import cPickle as pickle
# import _pickle as pickle
from timeit import default_timer as timer
from graph_tool.all import *
from operator import itemgetter
from collections import Counter
import math
import csv


csv_twitter_small_dataset = "csv/twitter-small.csv"
csv_graph_tool_twitter_small_dataset = 'csv/csv_graph_tool_twitter-small.csv'

csv_twitter_large_dataset = "csv/twitter-large.csv"
csv_graph_tool_twitter_large_dataset = 'csv/csv_graph_tool_twitter-large.csv'


def closeness_centrality(Graph, vp_source_username):
    close = graph_tool.centrality.closeness(Graph)
    c_list = []

    for user in Graph.vertices():
        if close[user] > 0:
            c_list += [(vp_source_username[user], close[user])]

    c_list = sorted(c_list, key=itemgetter(1), reverse=True)[:20]

    # print('Closness')
    for i in range(len(c_list)):
        print(c_list[i][0])
    print('\n')


def betweenness_centrality(Graph, vp_source_username):
    betweenness = graph_tool.centrality.betweenness(Graph)

    b_list = []

    print('Betweenness')

    for user in Graph.vertices():
        if betweenness[0][user] > 0:
            b_list += ([vp_source_username[user], betweenness[0][user]])

    b_list = sorted(b_list, key=itemgetter(1), reverse=True)[:20]

    for i in range(len(b_list)):
        print(b_list[i][0])
    print('\n')


def in_degree_centrality(file):
    parser = parse_file_to_digraph(file)
    idg = nx.in_degree_centrality(parser)
    idc_list = []

    for user in idg:
        idc_list += [(user, idg[user])]

    print('In Degree Centrality')

    idc_list = sorted(idc_list, key=itemgetter(1), reverse=True)[:20]

    for i in range(len(idc_list)):
        print(idc_list[i][0])


def out_degree_centrality(file):
    parser = parse_file_to_digraph(file)
    odg = nx.out_degree_centrality(parser)

    odc_list = []
    for user in odg:
        odc_list += [(user, odg[user])]
    print('Out Degree Centrality')

    odc_list = sorted(odc_list, key=itemgetter(1), reverse=True)[:20]

    for i in range(len(odc_list)):
        print(odc_list[i][0])

    print('\n')


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


def main():

    # small = parse_file_to_digraph(csv_twitter_small_dataset)
    # in_degree_centrality(small)

    # large = parse_file_to_digraph(csv_twitter_large_dataset)
    # in_degree_centrality(large)

    G = Graph()
    start_time = timer()
    vp_source_username = G.new_vertex_property("string")
    vp_target_username = G.new_vertex_property("string")
    vp_weight = G.new_vertex_property("int")
    vp_timestamp = G.new_vertex_property("int")

    with open(csv_graph_tool_twitter_small_dataset, 'r') as file:
        reader = csv.reader(file, delimiter=',', quotechar='|')

        reader.next()  # skip header

        for c in reader:
            src_id = c[0]
            target_id = c[1]
            src_name = c[2]
            target_name = c[3]

            G.add_edge(src_id, target_id)

            vp_source_username[G.vertex(src_id)] = src_name
            vp_target_username[G.vertex(target_id)] = target_name

        out_degree_centrality(csv_twitter_small_dataset)


if __name__ == '__main__':
    main()
