from test import visualization
from networkx.classes.function import nodes
import pandas as pd
from pandas.io.formats.format import set_eng_float_format
import random
import matplotlib.pyplot as plt
import networkx as nx 
import matplotlib.animation as animation
from statistics import mean
import numpy as np

plt.rcParams['figure.dpi'] = 150
plt.rcParams['animation.embed_limit'] = 217277560

###  Set the parameters and Initial Values
days = 7  # Total days of Simulation (Iteration Times) 
influential_user_num = 5   # Number of the most influential users
color_dict = {"S":"blue","I":"red","R":"green"}   # Display colors: blue for non-infected, red for infected
visited = []
# read Users and Engagement+React Score from csv data
df = pd.read_csv('Csv/Enga_Reac_Score.csv', delimiter=',')
user = pd.read_csv('Csv/user.csv', header=None).values.tolist()
user = [i[0] for i in user ]
enga_reac_score = df[['Engage+React_Score']].values.tolist()
enga_reac_score = [i[0] for i in enga_reac_score ]


def calPropaRate(user, enga_reac_score):
    '''
    Calculate the propagation rate in users network
    
    Parameters
    --------
    user: [List] all users
    enga_reac_score: [List] all engagement+react scores of each user
    
    Return
    -------
    rate: [Dictionary] propagation rate of each user -- {'user': rate}
    '''

    rate = {}
    repost = 3000; like = 250000 
    for i in range(len(user)):
        rate[user[i]] =  (repost/like) * (enga_reac_score[i]/mean(enga_reac_score))
    return rate

def random_users(user):
    '''
    Generate users randomly, used for comparative experiment
    
    Parameters
    --------
    user: [List] all users
    
    Return
    -------
    rd_users: [List] randomly generated users
    '''

    rd_users = []
    for _ in range(influential_user_num):
        r = random.randint(0, len(user))
        rd_users.append(user[r])
    return rd_users


def updateNodeState(G, node, infeRate, visited):
    '''
    Update the state of neighbors of one node in the network
    
    Parameters
    --------
    G: [Object] graph of users network
    node: [String] selected node whose state to be update 
    infeRate: [Dictionary] propagation rate of each user -- {'user': rate}
    visited: [List] users already visited, they won't infected others 

    Return
    -------
    new_add: [List] newly infected users, who haven't been visited  
    '''

    new_add = []
    if G.nodes[node]["state"] == "I": # followers
        ## find followers of the user
        for neigh in G.neighbors(node):
            # If the neighbor already visited, we won't consider him into new_add infectors
            if neigh in visited:  
                continue
            # Add the neighbors according to propagation rate(i.e. probability)
            p = random.random()
            if p <= infeRate[int(node)]:
                G.nodes[neigh]["state"] = "I"
                new_add.append(neigh)
    return new_add
           

def updateNetworkState(G, infeRate, ini_Infectors, visited):
    '''
    Update all nodes in the network during one iteration (one day)
    
    Parameters
    --------
    G: [Object] graph of users network
    infeRate: [Dictionary] propagation rate of each user -- {'user': rate}
    ini_Infectors: [List] initial infected nodes before updating
    visited: [List] (Before updating) Infected users already visited, they won't influence others next time 

    Return
    ------- 
    new_Infec: [List] updated infected nodes after one interation
    visited_new: [List] (After updating) Infected users already visited, they won't influence others next time 
    '''
    
    new_Infec = []
    for node in ini_Infectors: # Transver the whole network, update state of all nodes
        new_add_infe = updateNodeState(G, node, infeRate, visited)
        new_Infec.extend(new_add_infe)
        for i in new_Infec:
            if i not in visited:
                visited.append(i)
    visited_new = visited
    return new_Infec, visited_new


def countSIR(G):
    '''
    Calculate the number of infectors and non-infectors
    
    Parameters
    --------
    G: [Object] graph of users network

    Return
    ------- 
    S, I: [Integer] number of infectors and non-infectors
    '''

    S = 0;I = 0
    for node in G:
        if G.nodes[node]["state"] == "S":
            S = S + 1
        elif G.nodes[node]["state"] == "I":
            I = I + 1
    return S,I

def Simulation(Graph, days, infeRate, ini_Infectors, SI_list, is_random=False):
    '''
    Simulation for days (Iteration Times), update state of all users 
    
    Parameters
    --------
    Graph: [Object] graph of users network
    days: [Integer] total days of Simulation (Iteration Times) 
    infeRate: [Dictionary] propagation rate of each user -- {'user': rate}
    ini_Infectors: [List] initial infected nodes before updating
                          (most influential or randomly selected)
    SI_list: [List] number of infectors and non-infectors before simulation
                    (most influential or randomly selected)
    is_random: [Boolean] if the users is randomly selected, Ture-random, False-otherwise 

    Return
    ------- 
    SI_list: [List] number of infectors and non-infectors after simulation
    '''
    
    global visited
    if is_random:
        print('\n\nSimulation with random selected users:\n')
    else:    
        print('\n\nSimulation with most influential users:\n')

    position = nx.spring_layout(Graph) # set the layout of this network  
    fig, ax = plt.subplots(nrows=2, ncols=4, figsize=(24, 16)) # set the size of the pic (24X16)
    for t in range(0,days):
        ini_Infectors, visited = updateNetworkState(Graph,infeRate, ini_Infectors, visited)  
        SI_list.append(list(countSIR(Graph)))  # calculate the number of infectors and non-infectors
        print('Day-{}, there are {} influenced users, {} non-influenced user !'.format(t, SI_list[t][1], SI_list[t][0]))
        
        if is_random:
            visualization_Network(ax, t, Graph, position, is_random=True)
        else:
            visualization_Network(ax, t, Graph, position) 
    if is_random:
        plt.suptitle("Propagation Network with Random Selected Users")
    else:    
        plt.suptitle("Propagation Network with Most Influential Users")       
    plt.show()     
    visited = []
    return SI_list


def get_node_color(G): 
    '''
    Get color of each node
    
    Parameters
    --------
    G: [Object] graph of users network

    Return
    ------- 
    color_list: [List] color of each node
    '''

    color_list = []
    for node in G:
        #  map state to the color_dict 
        color_list.append(color_dict[G.nodes[node]["state"]])
    return color_list 


def visualization_Network(ax, t ,Graph, position, is_random=False):
    '''
    Network Visualization of simulation
    
    Parameters
    --------
    days: [Integer] total days of Simulation (Iteration Times) 
    Graph: [Object] graph of users network
    position: [Dictionary] positions keyed by node (Layout of network)
    is_random: [Boolean] if the users is randomly selected, Ture-random, False-otherwise 
    '''

    ### Plot the subgraph of propagation network 
    plt.axis("off") # shutoff the axis
    if t < len(ax[0]):
        i = 0; j = t
    else:
        i = 1; j = t - len(ax[0])
    ax[i][j].set_title("day" + str(t), fontsize=12)      
    plt.box(False) # set picture without box(border)
    nx.draw(Graph, node_size=1, width = 0.0001, 
            node_color = get_node_color(Graph), 
            pos = position,ax=ax[i][j], edge_color = "#D8D8D8")

def visualization_Line(SI_list, is_random=False):
    '''
    Line Chart Visualization of simulation
    
    Parameters
    --------
    SI_list: [List] number of infectors and non-infectors before simulation
    is_random: [Boolean] if the users is randomly selected, Ture-random, False-otherwise 
    '''

    ###  Plot the line chart, x-axis:Time(Days), y-axis:Number of Users
    df = pd.DataFrame(SI_list,columns=["S","I"])
    fig2, ax2 = plt.subplots(figsize=(24, 16)) # set the size of the pic (24X16)
    if is_random:
        ax2.set_title("Propagation Line Chart with Random Selected Users")
    else:
        ax2.set_title("Propagation Line Chart with Most Influential Users") 
    df.plot(figsize=(24, 16),color=[color_dict.get(x) for x in df.columns], ax=ax2)
    
    # Set the axis range
    plt.xlim((1, 8)); plt.ylim((0,3047))
    # Set axis name
    plt.xlabel('Time/days'); plt.ylabel('Number of users')
    # Set axis scale
    my_x_ticks = np.arange(1,8,1)
    plt.xticks(my_x_ticks)


def graph_draw(i,G,pos,ax,infeRate, ini_Infectors): 
    '''
    Drawing each frame in the animation, save the animation as Gif 
    
    Parameters
    --------
    i: [Integer] first few frames
    G: [Object] graph of users network
    pos: [Dictionary] positions keyed by node (Layout of network)
    ax: [Object] draw the graph in the specified Matplotlib axes.
    infeRate: [Dictionary] propagation rate of each user -- {'user': rate}
    ini_Infectors: [List] initial infected nodes before updating
    visited: [List] (Before updating) Infected users already visited, they won't influence others next time 
    '''

    global visited
    visited = []
    ax.axis("off")
    ax.set_title("day " + str(i) + " blue(non-infectors)，red(infectors)")
    plt.box(False)
    if i == 0: # In the first frame, plot the network
        nx.draw(G, node_size=1, width=0.0001, node_color = get_node_color(G), edge_color = "#D8D8D8",pos = pos, ax=ax)
    else: # In Other frames, update each nodes
        updateNetworkState(G, infeRate, ini_Infectors, visited)
        nx.draw_networkx_nodes(G, pos = pos, node_size=3, node_color='#b41f1f', node_shape='o', ax=ax) 
    plt.close()


def init(is_random=False):
    '''
    Generate Graph according to adjacency list, initialize state of all users (non_infected or infected)

    Parameters
    --------
    is_random: [Boolean] if the users is randomly selected, Ture-random, False-otherwise 

    Return
    ------- 
    [Graph, ini_Infectors, rd_Infectors] [List] 
      - Graph [Object]  graph of users network
      - ini_infectors [List]  initial most influential users
      - rd_infectors [List]  randomly selected users
    '''

    Graph = nx.read_adjlist('Csv/adjlst_2.csv')  # Generate Graph according to adjacency list
    # Initialize non-infected users
    for node in Graph:
        Graph.nodes[node]["state"] = "S"
    # Initialize infected users
    rd_list = random_users(user)
    rd_Infectors = []
    ini_list = user[:influential_user_num]   # THE MOST INFLUENTIAL USERS
    ini_Infectors = []        
    
    if is_random:
        # Initial infected(random selected) users
        for i in rd_list:
            i = str(i)
            for node in Graph.nodes:
                if node.startswith(i):
                    Graph.nodes[node]["state"] = "I"
                    rd_Infectors.append(node)
    else:
        # Initialize infected(most influential) users
        for i in ini_list:
            i = str(i)
            for node in Graph.nodes:
                if node.startswith(i):
                    Graph.nodes[node]["state"] = "I"
                    ini_Infectors.append(node)
    return [Graph, ini_Infectors, rd_Infectors]


if __name__ == "__main__":
    ### Generate users from csv file
    df = pd.read_csv('Csv/Score_ranking.csv', delimiter=',')
    user = df['User_id'].values.tolist()

    ### initialize users (state of users)
    List_ini = init(); Graph_ini = List_ini[0]; ini_Infectors = List_ini[1]
    List_rd = init(is_random=True); Graph_rd = List_rd[0]; rd_Infectors = List_rd[2]
    print(List_ini, List_rd)

    ###  Run simulation for days, Update the state of each nodes
    SI_list = []; rd_SI_list = []     # record number of infected users and non-infected users 
    # Calculate the rate of being infected
    infeRate = calPropaRate(user, enga_reac_score)  
    SI_list = Simulation(Graph_ini, days, infeRate, ini_Infectors, SI_list)   # most influential users
    rd_SI_list = Simulation(Graph_rd, days, infeRate, rd_Infectors, rd_SI_list, is_random=True)  # randomly selected users

    ### Visualization
    position = nx.spring_layout(Graph_ini) # set the layout of this network    
    visualization_Line(SI_list, is_random=True) 
    visualization_Line(rd_SI_list) 

'''
    ###  Save the animation of network as Gif 
    #initialize users (state of users)
    Graph_ini = init()[0]; Graph_rd = init(is_random=True)[0]
    SI_list = []; rd_SI_list = []     # record number of infected users and non-infected users     
    # generate animation of network 
    fig, ax = plt.subplots(figsize=(24, 16)) # set the size of the pic (24X16)
    ani = animation.FuncAnimation(fig, graph_draw, frames= range(0,days),
            fargs=(Graph_ini,position,ax,infeRate, ini_Infectors),  interval=1000)
    ani.save('assets/Propagation_animation_7d.gif', writer='imagemagick')
    rd_ani = animation.FuncAnimation(fig, graph_draw, frames= range(0,days),
            fargs=(Graph_rd,position,ax,infeRate, rd_Infectors),  interval=1000)
    rd_ani.save('assets/Random_Propagation_animation_7d.gif', writer='imagemagick')
'''