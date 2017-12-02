## Shapley Value based Top K Influential Nodes Selection

from random import random, shuffle
import operator

# This is an example graph. You can try your own graphs too.
# See the next cell
graph = {
    0:(1,3),
    1:(0,2,3,4),
    2:(1,4),
    3:(0,1,5,6),
    4:(1,2,6,7,8),
    5:(3,6),
    6:(3,4,5,7),
    7:(4,6),
    8:(4,9,11),
    9:(8,10),
    10:(9,11,12),
    11:(8,10),
    12:(10,14),
    13:(14,),
    14:(12,13)
}

# the adjacency matrix derived from the graph
# The weights of nodes are given by:
# w(i,j) = 1/d(i), where d(i) is the cardinality 
# or the number of neighbours of i
n = len(graph)
adj_mat = [[0 for j in range(n)] for i in range(n)]
for i in range(n):
    for j in range(n):
        if j in graph[i]:
            adj_mat[i][j] = 1.00/len(graph[i])

# Try your own graph
print 'Do you want to try your own graph?'
print 'Write yes or no'
ans = raw_input()
if ans == 'yes':
    adj_mat = []
    print 'How many nodes does your graph have?'
    n = int(raw_input())
    print 'Ok. Give me your adjacency matrix.'
    print 'If a node is not connected put 0 instead'
    print 'The diagonal elements should all be 0'
    for i in range(n):
        adj_mat.append(map(int, raw_input().split()))
    graph = {i:[] for i in range(n)}
    for i in range(n):
        for j in range(n):
            if not adj_mat[i][j] == 0:
                graph[i].append(j)
print '\nadjacency matrix:'
for i in range(n):
    print adj_mat[i]
print '\ngraph:'
for key in graph:
    print key, graph[key]

## global variables

# number of times the experiment is repeated 
R = 10000

n = len(graph)

# a polynomial in n, It is the number of sample
# permutations of the set of nodes.
# Ideally it should be n!, but we approximate it
# with a polynomial of n, lest the problem will
# be NP-Hard
t = 2*n + 3

# a list to maintain which nodes are active
active_nodes = [False for i in range(n)]

# randomly assigned thresholds to nodes
theta = [random() for i in range(n)]

def thresh_f(i):
    """
    returns the value of threshold function for node i
    it is the sum of weights of all active neighbours 
    of i
    """
    s = len(graph[i])
    t = 0
    for j in graph[i]:
        if active_nodes[j] == True:
            t += adj_mat[i][j]
    return t

def deactivate_all():
    """
    Deactivates all nodes
    We have to do this for every iteration in 
    calcuation of Marginal Contribution
    """
    global active_nodes
    active_nodes = [False for i in range(n)]

def v(i):
    """
    Returns the contribution of node i
    It is equal to the number of nodes that get activated
    due to the activation of node i. If a node is already
    activated, its contribution is zero
    """
    global active_nodes
    
    # Check whether the node is already active
    if active_nodes[i] == True:
        return 0
    
    active_nodes[i] = True
    contrib = 0
    
    for j in graph[i]:
        if thresh_f(j) >= theta[j] and active_nodes[j] == False:
            active_nodes[j] = True
            contrib += 1 + v(j)
            
    return contrib

def Shapley():  
    """
    Returns Shapley values of all nodes by taking
    a randomly generated sample of permuations of
    nodes.
    """
    global active_nodes
    global theta
    
    # phi contains the shapley values of nodes
    phi = [0 for i in range(n)]
    
    # MC, i.e., marginal contribution of each node
    # which reflects the change in coverage due to
    # the addition of node i in the set of initilly
    # activated nodes
    MC = [0 for i in range(n)]
    
    # randomly select t permutations from n! possible
    # permutations of nodes
    for j in range(t):
        temp = [0 for i in range(n)]
        
        # repeat the experiment R times (take the average)
        for r in range(R):
            theta = [random() for i in range(n)]
            deactivate_all()
            k = [i for i in range(n)]
            shuffle(k)
            for i in k:
                temp[i] += v(i)
                
        # Add the contribution for each permuation
        for i in range(n):
            MC[i] += temp[i]*1.00/R
            
    for i in range(n):
        phi[i] = (MC[i]*1.00)/t
    return phi

# Calculate the Shapley values of nodes
# This step might take some time due to
# large number of iterations R or 
# large number of nodes
print '\nPlease wait...\n'
shapley_values = Shapley()

x = {i+1: shapley_values[i] for i in range(n)}
rank = sorted(x.items(), key=operator.itemgetter(1), reverse=True)

print '\nThe rank list of nodes based on Shapley Values'
for key, value in rank:
    print "node = %3d\t Shapley value = %f"%(key, value)

### Choosing the Top-k nodes
print 'Enter the number of influential nodes you want to get (< n)'
k = int(raw_input())     # Change this with the desired number of influential nodes

def is_adj(i, topknodes):
    for node in topknodes:
        if i in graph[node-1]:
            return True
    return False

topknodes = []
i = 0
count = 0
while count < k and not i == n:
    if rank[i][0] not in topknodes and not is_adj(rank[i][0], topknodes):
        topknodes.append(rank[i][0])
        count += 1
    i += 1
i = 0
if not count == k:
    while not count == k:
        if rank[i][0] not in topknodes:
            topknodes.append(rank[i][0])
            count += 1
        i += 1

print '\nTop K nodes:'
print topknodes
