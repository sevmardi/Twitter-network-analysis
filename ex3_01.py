from ttp import ttp
from datetime import datetime, time
import networkx as nx
import sys
import csv


# https://stackoverflow.com/questions/7626643/python-tweet-parsing
raw_data_twitter_test = 'data/test-tweets.in'
csv_small_test = "csv/twitter-small-test.csv"

raw_data_twitter_small = 'data/twitter-small.in'
csv_small = "csv/twitter-small.csv"
csv_graph_tool_small = "csv/csv_graph_tool_twitter-small.csv"

raw_data_twitter_large = 'data/twitter-larger.in'
csv_large = 'csv/twitter-large.csv'
csv_graph_tool_large = 'csv/csv_graph_tool_twitter-large.csv'



# Example how to user twitter text parser
# p = ttp.Parser()
# result = p.parse("@burnettedmond, you now support #IvoWertzel's tweet parser! https://github.com/edburnett/")
# print(result.reply)


def create_adjacency_list(file):
    p = ttp.Parser()
    adj_list = {}
    tweet_counter = 0
    with open(file, 'r') as tweets:
        for line in tweets:
            line = line.rstrip('\n')
            tweet = line.split("\t")

            timestamp = int(datetime.strptime(tweet[0], "%Y-%m-%d %H:%M:%S").strftime("%s"))
            username = tweet[1]
            result = p.parse(tweet[2], html=False).users

            if len(result) > 0:
                if username not in adj_list:
                    adj_list[username] = {}

                for i in result:
                    if i not in adj_list[username]:
                        adj_list[username][i] = {}
                        adj_list[username][i]['timestamps'] = [timestamp]
                    else:
                        adj_list[username][i]['timestamps'] += [timestamp]

                    adj_list[username][i]['timestamps'].sort()
                    adj_list[username][i]['first_mention'] = adj_list[
                        username][i]['timestamps'][0]
                    adj_list[username][i]['number_of_mentions'] = len(
                        adj_list[username][i]['timestamps'])

    return adj_list


def create_edge_list(adjust_list, filename):
    """
    Create edge list in which can be used in gephi.
    """
    edge_list = []

    for user in adjust_list:
        for mention_user in adjust_list[user]:
            weight = adjust_list[user][mention_user]['number_of_mentions']
            timestamp = adjust_list[user][mention_user]['first_mention']
            edge_list += [(user, mention_user, weight, timestamp)]

    with open(filename, 'w') as edge_list_file:
        csv_out = csv.writer(edge_list_file)
        csv_out.writerow(['Source', 'Target', 'Weight', 'Timestamp'])
        for row in edge_list:
            csv_out.writerow(row)

# TODO Needs refactoring.
def create_graph_edge_list(adjust_list, filename):
    """
    A helper function to create edge list for graph-tool
    """
    users = []

    for usr in adjust_list:
        users += [usr]
        for mention_user in adjust_list[usr]:
            users += [mention_user]

    users = list(set(users))
    tple = []

    for i in range(len(users)):
        tple += [(users[i], i)]

    U_dict = {}

    for j in tple:
        U_dict[j[0]] = j[1]

    edge_lst = []

    for usr in adjust_list:
        for mention_user in adjust_list[usr]:
            weight = adjust_list[usr][mention_user]['number_of_mentions']
            timestamp = adjust_list[usr][mention_user]['first_mention']
            edge_lst += [(U_dict[usr], U_dict[mention_user],
                          usr, mention_user, weight, timestamp)]
    with open(filename, 'w') as file:
        csv_out = csv.writer(file)
        csv_out.writerow(['Source','Target','Source-Username','Target-Username','Weight','Timestamp']);

        for row in edge_lst:
            csv_out.writerow(row)


if __name__ == '__main__':
    small_adjacency_list = create_adjacency_list(raw_data_twitter_test)
    create_edge_list(small_adjacency_list, csv_small_test)
    # create_graph_edge_list(small, csv_graph_tool_small)


    # large = create_adjacency_list(raw_data_twitter_large)
    # create_edge = create_edge_list(large, csv_large)
    # create_graph_edge_list(large, csv_graph_tool_large)
