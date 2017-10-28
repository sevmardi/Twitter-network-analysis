import networkx as nx
import numpy as np

def to_edgelist(inputfile):
	data = np.genfromtxt(inputfile+".in", dtype=str, delimiter='\n')
	edge_list = np.array(["Source", "Target"])
	sub_list = np.zeros((0,2))
	sublist_len = 0
	
	for row in data:
		rowArray = row.split('\t')
		user1 = rowArray[1]
		
		# Find the number of mentioned users in this tweet #
		for i in np.arange(row.count('@')):
			index = row.find('@')
			if index > 0:
				j=0
				
				# Look for the first non-number and non-character #
				while index+j < len(row) and row[index+j] != ' ' and row[index+j] != ':' and row[index+j] != '!' and row[index+j] != ')' and row[index+j] != ';' and row[index+j] != '.':
					j += 1
				
				# Parse mentioned username without the @ character #
				user2 = row[index+1:index+j]
				print(sub_list.shape)
				sub_list = np.vstack((sub_list, [user1, user2]))
				sublist_len += 1

				if sublist_len == 1000:
					edge_list = np.vstack((edge_list, sub_list))
					sub_list = np.zeros((0,2))
					sublist_len = 0
				
				# Continue iterating #
				row = row[index+1:]
	edge_list = np.vstack((edge_list, sub_list))
	print(edge_list)
	np.savetxt("edgelist-" + inputfile+".csv", edge_list, fmt='%s')

def main():
	to_edgelist("data/small-tweets")

if __name__ == "__main__":
	main()