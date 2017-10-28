import re
from collections import Counter
import csv

hMap = dict()


def foundMention(str):
    "returns true if it finds a mention"
    p=re.compile('@[a-zA-z0-9_]{1,15}')
    m = p.findall(str)
    return m
    
def buildFile():
    "outputs a csv file with the graph on hMap with the columns source, target, weight and timestamp, which is the timestamp for the first time the target user was mentioned by the source user"
    spamwriter = csv.writer(open('twitter-large.csv', 'wb'), delimiter=',')
    spamwriter.writerow(["Source", "Target", "Weight", "TimeStamp"])
    for key in hMap:
        timestampedusers = []
        mentionedusers = [(user, tweet[0]) for tweet in hMap[key] for user in tweet[1]]
        countedUsers = Counter(pair[0] for pair in mentionedusers)
        for pair in mentionedusers:
            if not any(pair[0] in pair2 for pair2 in timestampedusers):
                timestampedusers.append(pair)
        for pair in timestampedusers:
            spamwriter.writerow([key, pair[0], countedUsers[pair[0]], pair[1]])




def get_timestamp():
    result = {}
    for key in hMap:
        for i in hMap[key]:
                for j in i[1]:
                    if j not in result:
                        result[j] = i[0]
    return result


with open("data/twitter-larger.in") as f:
    print "opened"
    for line in f:
        mentions = foundMention(line)
        if mentions:
            linelist = re.split(r'\t+', line.rstrip('\t'))
            mentions = [mention[1:] for mention in mentions]
            tweet = [linelist[0], mentions]
            if linelist[1] in hMap:
                hMap[linelist[1]].append(tweet)
            else:
                hMap[linelist[1]] = [tweet]


    buildFile()
