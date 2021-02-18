import graph

def default_heuristic(n):
    """
    Default heuristic for A*. Do not change, rename or remove!
    """
    return 0

def bfs(start, goal):
    """
    Breadth-First search algorithm. The function is passed a start graph.Node object and a goal predicate.
    
    The start node can produce neighbors as needed, see graph.py for details.
    
    The goal is represented as a function, that is passed a node, and returns True if that node is a goal node, otherwise False. 
    
    The function should return a 4-tuple (path,distance,visited,expanded):
        - path is a sequence of graph.Edge objects that have to be traversed to reach a goal state from the start
        - distance is the sum of costs of all edges in the path 
        - visited is the total number of nodes that were added to the frontier during the execution of the algorithm 
        - expanded is the total number of nodes that were expanded, i.e. removed from the frontier to add their neighbors
    """
    return search(start, -1, goal, 'bfs')
    
def dfs(start, goal):
    """
    Depth-First search algorithm. The function is passed a start graph.Node object, a heuristic function, and a goal predicate.
    
    The start node can produce neighbors as needed, see graph.py for details.
    
    The goal is represented as a function, that is passed a node, and returns True if that node is a goal node, otherwise False. 
    
    The function should return a 4-tuple (path,distance,visited,expanded):
        - path is a sequence of graph.Edge objects that have to be traversed to reach a goal state from the start
        - distance is the sum of costs of all edges in the path 
        - visited is the total number of nodes that were added to the frontier during the execution of the algorithm 
        - expanded is the total number of nodes that were expanded, i.e. removed from the frontier to add their neighbors
    """
    return search(start, -1, goal, 'dfs')
    
def greedy(start, heuristic, goal):
    """
    Greedy search algorithm. The function is passed a start graph.Node object, a heuristic function, and a goal predicate.
    
    The start node can produce neighbors as needed, see graph.py for details.
    
    The heuristic is a function that takes a node as a parameter and returns an estimate for how far that node is from the goal.    
    
    The goal is also represented as a function, that is passed a node, and returns True if that node is a goal node, otherwise False. 
    
    The function should return a 4-tuple (path,distance,visited,expanded):
        - path is a sequence of graph.Edge objects that have to be traversed to reach a goal state from the start
        - distance is the sum of costs of all edges in the path 
        - visited is the total number of nodes that were added to the frontier during the execution of the algorithm 
        - expanded is the total number of nodes that were expanded, i.e. removed from the frontier to add their neighbors
    """
    return search(start, heuristic, goal, 'greedy')
    

def astar(start, heuristic, goal):
    """
    A* search algorithm. The function is passed a start graph.Node object, a heuristic function, and a goal predicate.
    
    The start node can produce neighbors as needed, see graph.py for details.
    
    The heuristic is a function that takes a node as a parameter and returns an estimate for how far that node is from the goal.    
    
    The goal is also represented as a function, that is passed a node, and returns True if that node is a goal node, otherwise False. 
    
    The function should return a 4-tuple (path,distance,visited,expanded):
        - path is a sequence of graph.Edge objects that have to be traversed to reach a goal state from the start
        - distance is the sum of costs of all edges in the path 
        - visited is the total number of nodes that were added to the frontier during the execution of the algorithm 
        - expanded is the total number of nodes that were expanded, i.e. removed from the frontier to add their neighbors
    """
    return search(start, heuristic, goal, 'astar')

# encompassing search algorithm
def search(start, heuristic, goal, type):
    nodedict = {}
    edgedict = {}
    path = []
    expandednodes = []
    frontier = [start]
    expanded, visited, length = 0,0,0

    # run while the queue is not empty (and less than 10000 nodes visited to avoid running forever)
    while frontier and visited < 10000:

        # based on type parameter, pop the next node from either the top or bottom of the frontier, appropriately sorting first if necessary
        if type == 'bfs':
            current = frontier.pop(0)
        elif type == 'dfs':
            current = frontier.pop()
        elif type == 'greedy':
            # sort based on heuristic
            frontier.sort(key=lambda node: heuristic(node), reverse=False)
            current = frontier.pop(0)
        elif type == 'astar':
            # sort based on heuristic + length to current node
            frontier.sort(key=lambda node: heuristic(node) + getpathlength(start, node, edgedict, nodedict), reverse=False)
            current = frontier.pop(0)

        expanded += 1
        expandednodes.append(current)

        # expand current node
        neighborEdges = current.get_neighbors()
        for edge in neighborEdges:
            neighborNode = edge.target

            # skip neighbor if it's been expanded already
            if not neighborNode in expandednodes:
                nodedict[neighborNode.get_id] = current
                edgedict[neighborNode.get_id] = edge

                # if goal has been found in the neighbors, retrace our path to get there and return
                if goal(neighborNode):
                    current = neighborNode
                    while(current != start):
                        edge = edgedict[current.get_id]
                        path.insert(0, edge)
                        length += edge.cost
                        current = nodedict[current.get_id]
                    return path, length, visited, expanded

                # else, add node to frontier
                frontier.append(neighborNode)
                visited += 1
              
    return path, -1, visited, expanded



# gets the path length taken to a node by retracing the nodes and edges it came from
def getpathlength(_start, _goal, _edgedict, _nodedict):
    length = 0
    current = _goal
    while(current != _start):
        edge = _edgedict[current.get_id]
        length += edge.cost
        current = _nodedict[current.get_id]
    return length


def run_all(name, start, heuristic, goal):
    print("running test", name)
    print("Breadth-First Search")
    result = bfs(start, goal)
    print_path(result)
    
    print("\nDepth-First Search")
    result = dfs(start, goal)
    print_path(result)
    
    print("\nGreedy Search (default heuristic)")
    result = greedy(start, default_heuristic, goal)
    print_path(result)
    
    print("\nGreedy Search")
    result = greedy(start, heuristic, goal)
    print_path(result)
    
    print("\nA* Search (default heuristic)")
    result = astar(start, default_heuristic, goal)
    print_path(result)
    
    print("\nA* Search")
    result = astar(start, heuristic, goal)
    print_path(result)
    
    print("\n\n")

def print_path(result):
    (path,cost,visited_cnt,expanded_cnt) = result
    print("visited nodes:", visited_cnt, "expanded nodes:",expanded_cnt)
    if path:
        print("Path found with cost", cost)
        for n in path:
            print(n.name)
    else:
        print("No path found")
    print("\n")

def main():
    """
    You are free (and encouraged) to change this function to add more test cases.
    
    You are provided with three test cases:
        - pathfinding in Austria, using the map shown in class. This is a relatively small graph, but it comes with an admissible heuristic. Below astar is called using that heuristic, 
          as well as with the default heuristic (which always returns 0). If you implement A* correctly, you should see a small difference in the number of visited/expanded nodes between the two heuristics.
        - pathfinding on an infinite graph, where each node corresponds to a natural number, which is connected to its predecessor, successor and twice its value, as well as half its value, if the number is even.
          e.g. 16 is connected to 15, 17, 32, and 8. The problem given is to find a path from 1 to 2050, for example by doubling the number until 2048 is reached and then adding 1 twice. There is also a heuristic 
          provided for this problem, but it is not admissible (think about why), but it should result in a path being found almost instantaneously. On the other hand, if the default heuristic is used, the search process 
          will take a noticeable amount (a couple of seconds).
        - pathfinding on the same infinite graph, but with infinitely many goal nodes. Each node corresponding to a number greater 1000 that is congruent to 63 mod 123 is a valid goal node. As before, a non-admissible
          heuristic is provided, which greatly accelerates the search process. 
    """
    target = "Bregenz"
    def atheuristic(n):
        return graph.AustriaHeuristic[target][n.get_id()]
    def atgoal(n):
        return n.get_id() == target
    
    run_all("Austria", graph.Austria["Eisenstadt"], atheuristic, atgoal)


    target = "Riften"
    def atheuristic(n):
        return graph.SkyrimHeuristic[target][n.get_id()]
    def atgoal(n):
        return n.get_id() == target
    
    run_all("Skyrim", graph.Skyrim["Solitude"], atheuristic, atgoal)

    
    
    target = 2050
    def infheuristic(n):
        return abs(n.get_id() - target)
    def infgoal(n):
        return n.get_id() == target
    
    run_all("Infinite Graph (simple)", graph.InfNode(1), infheuristic, infgoal)
    

    def multiheuristic(n):
        return abs(n.get_id()%123 - 63)
    def multigoal(n):
        return n.get_id() > 1000 and n.get_id()%123 == 63
    
    run_all("Infinite Graph (multi)", graph.InfNode(1), multiheuristic, multigoal)
    

if __name__ == "__main__":
    main()