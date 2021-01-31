import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import math

### Read data from csv file about post and convert it to list
df = pd.read_csv('Csv/instagram_posts_all.csv',
delimiter="," )
df1 = df[['id_user','id_post','views','likes','comments','reposts','id_post_origin','link_clicks','donation_tag','donation_val','house_buy']]
user = df1['id_user'].values.tolist()
post = df1['id_post'].values.tolist()
view = df1['views'].values.tolist()
like = df1['likes'].values.tolist()
comment = df1['comments'].values.tolist()
repost = df1['reposts'].values.tolist()
post_origin = df1['id_post_origin'].values.tolist()
link = df1['link_clicks'].values.tolist()
donation_tag = df1['donation_tag'].values.tolist()
donation_val = df1['donation_val'].values.tolist()
house_buy = df1['house_buy'].values.tolist()


p = []
g = []
### Get engagement index from views, likes, comments and reposts
for i in range(0,len(user)):
    p.append(math.log(view[i]+1)+2*math.log(like[i]+1)+3*math.log(comment[i]+1)+4*math.log(repost[i]+1))
    g.append(p[i])
    for j in range(0,len(user)):
        if  post_origin[i]==post[j]:  # The original author should get a part of the engagement index from the reprinter’s engagement index
            g[j]=g[j]+0.1*p[i]
gmax = max(g)
### Calculate the engagement score
enga = []
for i in range(0,len(user)):
    enga.append(g[i]/gmax)  #All the engagement index should be divided by the max value to make it comparable to centrality index and reactive index

### Calculate the reaction score
reac=[]
for i in range(0,len(user)):
    if not link[i] and not donation_tag[i]:
        reac.append(0)
    elif link[i] and not donation_tag[i]:
        reac.append(1)
    elif link[i] and donation_tag[i]:
        reac.append(1+2+10*math.log(donation_val[i]/10+1))

reac_max = max(reac)  # Get reactive index accoding to different conditions
for i in range(0,len(user)):
    reac[i]=reac[i]/reac_max   # All the reactive index should be divided by the max value to make it comparable to centrality index and engagement index


### Get scores for the engagement index part and reactive index part
score=[]
for i in range(0,len(user)):
    score.append(0.3*enga[i]+0.1*reac[i])


G = nx.read_adjlist('Csv/adjlst_2.csv')
'''
These two lines of code are useful, but it takes much time to run because there are 3067 nodes in our graph
So we choose to save the result and read it 
'''
#BW_centrality = nx.betweenness_centrality(G)
#print(BW_centrality)
# # Save the result of betweenness centrality, it only need to be run once
#np.savetxt('Csv/BW_centrality.csv', BW_centrality)  

### Read the data of user and Betweeness Centrality of each user
id_user = pd.read_csv('Csv/user.csv', header = None)
file_read = pd.read_csv('Csv/BW_centrality.csv', delimiter=",", header=None)
BW_centrality = file_read.values.tolist()[0]
BW_centrality = [ i/max(BW_centrality) for i in BW_centrality]  #All the betweenness centrality should be divided by the max value to make it comparable to reactive and engagement index
 
### Calculate the final score of all nodes, combine the score and corresponded user into a dictionary
score_dict = {}
for i in range(0,len(user)):
    j = user.index(id_user[0][i])
    score[j] = score[j] + 0.6 * BW_centrality[i]
    score_dict[id_user[0][i]] = round(score[j], 6)
#Sort the score
sorted_score = sorted(score_dict.items(), key=lambda item:item[1], reverse=True)
#Get the user_id of most 100 influential users
print('THE MOST 100 INFLUENTIAL USERS (user_id, score): \n ', sorted_score[:100])


### save the score ranking into csv file
user_rank = [int(i[0]) for i in sorted_score]
Score_rank = [float(i[1]) for i in sorted_score]
dataframe = pd.DataFrame({'User_id': user_rank, 'Score': Score_rank})
# dataframe.to_csv("Csv/Score_ranking.csv", index=False, sep=',') # index: show the row name or not，default=True
# this line of code is used to output the csv file, it only need to be run once

### draw the graph
nx.draw(G, node_size=1, width=0.0001)
nx.draw_networkx_nodes(G, pos=nx.spring_layout(G), node_size=3, node_color='#b41f1f', node_shape='o')
plt.show()
