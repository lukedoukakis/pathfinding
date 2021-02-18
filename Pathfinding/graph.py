

class Node:
    def get_id(self):
        """
        Returns a unique identifier for the node (for example, the name, the hash value of the contents, etc.), used to compare two nodes for equality.
        """
        return ""
    def get_neighbors(self):
        """
        Returns all neighbors of a node, and how to reach them. The result is a list Edge objects, each of which contains 3 attributes: target, cost and name, 
        where target is a Node object, cost is a numeric value representing the distance between the two nodes, and name is a string representing the path taken to the neighbor.
        """
        return []
    def __eq__(self, other):
        return self.get_id() == other.get_id()
        
class Edge:
    """
    Abstraction of a graph edge. Has a target (Node that the edge leads to), a cost (numeric) and a name (string), which can be used to print the edge.
    """
    def __init__(self, target, cost, name):
        self.target = target 
        self.cost = cost
        self.name = name

class GeomNode(Node):
    """
    Representation of a finite graph in which all nodes are kept in memory at all times, and stored in the node's neighbors field.
    """
    def __init__(self, name):
        self.name = name
        self.neighbors = []
    def get_neighbors(self):
        return self.neighbors
    def get_id(self):
        return self.name
        
class InfNode(Node):
    """
    Infinite graph, in which every node represents an integer, and neighbors are generated on demand. Note that Nodes are not cached, i.e. if you
    request the neighbors of node 1, and the neighbors of node 3, both will contain the node 2, but they will be using two distinct objects. 
    """
    def __init__(self, nr):
        self.nr = nr
    def get_neighbors(self):
        result = [Edge(InfNode(self.nr-1),1,("%d - -1 - %d"%(self.nr,self.nr-1))), Edge(InfNode(self.nr+1),1,("%d - +1 - %d"%(self.nr,self.nr+1))), Edge(InfNode(self.nr*2),1,("%d - *2 - %d"%(self.nr,self.nr*2)))]
        if self.nr%2 == 0:
            result.append(Edge(InfNode(self.nr//2),1,("%d - /2 - %d"%(self.nr,self.nr//2))))
        return result
    def get_id(self):
        return self.nr


def make_geom_graph(nodes, edges):
    """
    Given a list of nodes and edges (with distances), creates a dictionary of Node objects 
    representing the graph. Note that the resulting graph is directed, but each edge will be 
    replaced with *two* directed edges (to and from).
    """
    result = {}
    for c in nodes:
        result[c] = GeomNode(c)
    for (a,b,d) in edges:
        result[a].neighbors.append(Edge(result[b], d, "%s - %s"%(a,b)))
        result[b].neighbors.append(Edge(result[a], d, "%s - %s"%(b,a)))
    return result
    
Austria = make_geom_graph(
    ["Graz", "Vienna", "Salzburg", "Innsbruck", "Munich", "Bregenz", "Linz", "Eisenstadt", "Klagenfurt", "Lienz", "Bruck"],
    [("Graz", "Bruck", 55.0),
     ("Graz", "Klagenfurt", 136.0),
     ("Graz", "Vienna", 200.0),
     ("Graz", "Eisenstadt", 173.0),
     ("Bruck", "Klagenfurt", 152.0),
     ("Bruck", "Salzburg", 215.0),
     ("Bruck", "Linz", 195.0),
     ("Bruck", "Vienna", 150.0),
     ("Vienna", "Eisenstadt", 60.0),
     ("Vienna", "Linz", 184.0),
     ("Linz", "Salzburg", 123.0),
     ("Salzburg", "Munich", 145.0),
     ("Salzburg", "Klagenfurt", 223.0),
     ("Klagenfurt", "Lienz", 145.0),
     ("Lienz", "Innsbruck", 180.0),
     ("Munich", "Innsbruck", 151.0),
     ("Munich", "Bregenz", 180.0),
     ("Innsbruck", "Bregenz", 190.0)])

Skyrim = make_geom_graph(
    ["Solitude", "Dawnstar", "Winterhold", "Morthal", "Windhelm", "Markarth", "Whiterun", "Falkreath", "Riften"],
    [("Solitude", "Dawnstar", 70.0),
     ("Solitude", "Morthal", 65.0),
     ("Solitude", "Markarth", 50.0),
     ("Dawnstar", "Winterhold", 25.0),
     ("Dawnstar", "Morthal", 35.0),
     ("Winterhold", "Windhelm", 25.0),
     ("Morthal", "Markarth", 52.0),
     ("Morthal", "Whiterun", 32.0),
     ("Morthal", "Windhelm", 60.0),
     ("Windhelm", "Whiterun", 58.0),
     ("Windhelm", "Riften", 70.0),
     ("Markarth", "Whiterun", 68.0),
     ("Markarth", "Falkreath", 60.0),
     ("Whiterun", "Riften", 75.0),
     ("Whiterun", "Falkreath", 40.0),
     ("Falkreath", "Riften", 77.0)])
     
AustriaHeuristic = { 
   "Graz":       {"Graz": 0.0,   "Vienna": 180.0, "Eisenstadt": 150.0, "Bruck": 50.0,  "Linz": 225.0, "Salzburg": 250.0, "Klagenfurt": 125.0, "Lienz": 270.0, "Innsbruck": 435.0, "Munich": 375.0, "Bregenz": 450.0},
   "Vienna":     {"Graz": 180.0, "Vienna": 0.0,   "Eisenstadt": 50.0,  "Bruck": 126.0, "Linz": 175.0, "Salzburg": 285.0, "Klagenfurt": 295.0, "Lienz": 400.0, "Innsbruck": 525.0, "Munich": 407.0, "Bregenz": 593.0},
   "Eisenstadt": {"Graz": 150.0, "Vienna": 50.0,  "Eisenstadt": 0.0,   "Bruck": 171.0, "Linz": 221.0, "Salzburg": 328.0, "Klagenfurt": 335.0, "Lienz": 437.0, "Innsbruck": 569.0, "Munich": 446.0, "Bregenz": 630.0},
   "Bruck":      {"Graz": 50.0,  "Vienna": 126.0, "Eisenstadt": 171.0, "Bruck": 0.0,   "Linz": 175.0, "Salzburg": 201.0, "Klagenfurt": 146.0, "Lienz": 287.0, "Innsbruck": 479.0, "Munich": 339.0, "Bregenz": 521.0},
   "Linz":       {"Graz": 225.0, "Vienna": 175.0, "Eisenstadt": 221.0, "Bruck": 175.0, "Linz": 0.0,   "Salzburg": 117.0, "Klagenfurt": 311.0, "Lienz": 443.0, "Innsbruck": 378.0, "Munich": 265.0, "Bregenz": 456.0},
   "Salzburg":   {"Graz": 250.0, "Vienna": 285.0, "Eisenstadt": 328.0, "Bruck": 201.0, "Linz": 117.0, "Salzburg": 0.0,   "Klagenfurt": 201.0, "Lienz": 321.0, "Innsbruck": 265.0, "Munich": 132.0, "Bregenz": 301.0},
   "Klagenfurt": {"Graz": 125.0, "Vienna": 295.0, "Eisenstadt": 335.0, "Bruck": 146.0, "Linz": 311.0, "Salzburg": 201.0, "Klagenfurt": 0.0,   "Lienz": 132.0, "Innsbruck": 301.0, "Munich": 443.0, "Bregenz": 465.0},
   "Lienz":      {"Graz": 270.0, "Vienna": 400.0, "Eisenstadt": 437.0, "Bruck": 287.0, "Linz": 443.0, "Salzburg": 321.0, "Klagenfurt": 132.0, "Lienz": 0.0,   "Innsbruck": 157.0, "Munich": 298.0, "Bregenz": 332.0},
   "Innsbruck":  {"Graz": 435.0, "Vienna": 525.0, "Eisenstadt": 569.0, "Bruck": 479.0, "Linz": 378.0, "Salzburg": 265.0, "Klagenfurt": 301.0, "Lienz": 157.0, "Innsbruck": 0.0,   "Munich": 143.0, "Bregenz": 187.0},
   "Munich":     {"Graz": 375.0, "Vienna": 407.0, "Eisenstadt": 446.0, "Bruck": 339.0, "Linz": 265.0, "Salzburg": 132.0, "Klagenfurt": 443.0, "Lienz": 298.0, "Innsbruck": 143.0, "Munich": 0.0,   "Bregenz": 165.0},
   "Bregenz":    {"Graz": 450.0, "Vienna": 593.0, "Eisenstadt": 630.0, "Bruck": 521.0, "Linz": 456.0, "Salzburg": 301.0, "Klagenfurt": 465.0, "Lienz": 332.0, "Innsbruck": 187.0, "Munich": 165.0, "Bregenz": 0.0}}

SkyrimHeuristic = { 
   "Solitude":   {"Solitude": 0.0, "Dawnstar": 30.0, "Winterhold": 52.0, "Morthal": 20.0,  "Windhelm": 62.0, "Markarth": 44.0, "Whiterun": 44.0, "Falkreath": 59.0, "Riften": 92.0},
   "Dawnstar":   {"Solitude": 30.0, "Dawnstar": 0.0, "Winterhold": 21.0, "Morthal": 24.0,  "Windhelm": 34.0, "Markarth": 69.0, "Whiterun": 34.0, "Falkreath": 61.0, "Riften": 71.0},
   "Winterhold": {"Solitude": 52.0, "Dawnstar": 21.0, "Winterhold": 0.0, "Morthal": 43.0,  "Windhelm": 22.0, "Markarth": 89.0, "Whiterun": 43.0, "Falkreath": 72.0, "Riften": 64.0},
   "Morthal":    {"Solitude": 20.0, "Dawnstar": 24.0, "Winterhold": 43.0, "Morthal": 0.0,  "Windhelm": 46.0, "Markarth": 45.0, "Whiterun": 23.0, "Falkreath": 41.0, "Riften": 72.0},
   "Windhelm":   {"Solitude": 62.0, "Dawnstar": 34.0, "Winterhold": 22.0, "Morthal": 46.0,  "Windhelm": 0.0, "Markarth": 90.0, "Whiterun": 34.0, "Falkreath": 62.0, "Riften": 42.0},
   "Markarth":   {"Solitude": 44.0, "Dawnstar": 69.0, "Winterhold": 89.0, "Morthal": 45.0,  "Windhelm": 90.0, "Markarth": 0.0, "Whiterun": 58.0, "Falkreath": 50.0, "Riften": 105.0},
   "Whiterun":   {"Solitude": 44.0, "Dawnstar": 34.0, "Winterhold": 43.0, "Morthal": 23.0,  "Windhelm": 34.0, "Markarth": 58.0, "Whiterun": 0.0, "Falkreath": 29.0, "Riften": 49.0},
   "Falkreath":  {"Solitude": 59.0, "Dawnstar": 61.0, "Winterhold": 72.0, "Morthal": 41.0,  "Windhelm": 62.0, "Markarth": 50.0, "Whiterun": 29.0, "Falkreath": 0.0, "Riften": 59.0},
   "Riften":     {"Solitude": 92.0, "Dawnstar": 71.0, "Winterhold": 64.0, "Morthal": 72.0,  "Windhelm": 42.0, "Markarth": 105.0, "Whiterun": 49.0, "Falkreath": 59.0, "Riften": 0.0}}
 
