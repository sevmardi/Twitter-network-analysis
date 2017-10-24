from ttp import ttp
from datetime import datetime, time
import networkx as nx
import sys
import csv


# https://stackoverflow.com/questions/7626643/python-tweet-parsing

data = 'data/twitter-small.in'
saver = "csv/twitter-small.csv"
csv_graph_tool = "csv/csv_graph_tool_twitter-small.csv"

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

            timestamp = int(datetime.strptime(
                tweet[0], "%Y-%m-%d %H:%M:%S").strftime("%s"))
            username = tweet[1]
            usrs = p.parse(tweet[2], html=False).users

            if len(usrs) > 0:
                if username not in adj_list:
                    adj_list[username] = {}

                for i in usrs:
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
    lst = create_adjacency_list(data)
    create_graph_edge_list(lst, csv_graph_tool)
