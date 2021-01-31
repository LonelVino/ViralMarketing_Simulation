import networkx as nx
import numpy as np
import pandas as pd


user=pd.read_csv('Csv/user.csv', header=None)
user=user.values.tolist()
follower=pd.read_csv('Csv/follower.csv', header=None)
follower=follower.values.tolist()
follower_raw = []
num_edges = 0
file_read = np.loadtxt('TXT/follower_raw.txt', dtype=list, delimiter=';')
for row in file_read:
    list_0 = row[0].split(",")
    for _ in list_0:
        num_edges += 1

#TODO: verify
new_list = []; dup = 0
for i in user:
    if i not in new_list:
        new_list.append(i) 
    elif i in new_list:
        dup = i
if len(new_list)==len(user):
    print('There is not a duplicated element！')
else:
    print('There is a duplicated element, user_id:{}！'.format(dup))


print('number of users:', len(user),'\n', 'number of follower:', len(follower),'\n', 'number of all followers:', num_edges)
G = nx.read_adjlist('Csv/adjlst_2.csv')
print(nx.info(G))   # Information of the graph

if len(follower) == len(user):
    print('Nodes of this graph is correct')
else:
    print('Number of follower does not equal to the number of users')

if num_edges ==  len(G.edges()):
    print('Edges of this graph is correct')
else:
    print("Edges of this graph doesn't equal to sum(number of followers of each user)")

