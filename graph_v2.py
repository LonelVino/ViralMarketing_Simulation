import networkx as nx
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


### Read data from accounts Csv file
df = pd.read_csv('Csv/instagram_accounts_joli_del.csv',
delimiter=";" )
# information of the dataframe - "id_suer id_follower"
df1 = df[['id_user','id_followers']]

### Generate the graph according to the users
G = nx.read_adjlist('Csv/adjlst_2.csv')
A = np.array(nx.adjacency_matrix(G).todense())  # adjacemncy matrix 
print('size of Adjacency matrix:(', len(A), ',', len(A[0]), ')')
# np.savetxt('Csv/adjmat.csv', A, fmt='%d')  # save the adjacency matrix into csv file

### Plot the graph
nx.draw(G,node_size=1.5, width = 0.0003)
plt.show()

### Save users into csv file
df = pd.read_csv('Csv/instagram_accounts_joli_del.csv', delimiter=";" )
df1 = df[['id_user','id_followers']]
user = df1['id_user'].values.tolist()
# np.savetxt('Csv/user.csv', user, fmt='%d')   # save the users into csv file

### Save followers into csv file 
follower_raw = []
file_read = np.loadtxt('TXT/follower_raw.txt', dtype=list, delimiter=';')

for row in file_read:
    list_0 = row[0].split(",")
    list_0 = [int(i) for i in list_0]
    follower_raw.append(list_0)

follower = []
for i in range(len(follower_raw)):
    for j in follower_raw[i]:
        if j not in follower:
            follower.append(j)
# np.savetxt('Csv/follower.csv', follower, fmt='%d')   # save the followers into csv file
