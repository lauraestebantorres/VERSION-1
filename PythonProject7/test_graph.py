from graph import *


# Function to create the first graph
def CreateGraph_1():
   G = Graph()
   AddNode(G, Node("A", 1, 20))
   AddNode(G, Node("B", 8, 17))
   AddNode(G, Node("C", 15, 20))
   AddNode(G, Node("D", 18, 15))
   AddNode(G, Node("E", 2, 4))
   AddNode(G, Node("F", 6, 5))
   AddNode(G, Node("G", 12, 12))
   AddNode(G, Node("H", 10, 3))
   AddNode(G, Node("I", 19, 1))
   AddNode(G, Node("J", 13, 5))
   AddNode(G, Node("K", 3, 15))
   AddNode(G, Node("L", 4, 10))
   AddSegment(G, "AB", "A", "B")
   AddSegment(G, "AE", "A", "E")
   AddSegment(G, "AK", "A", "K")
   AddSegment(G, "BA", "B", "A")
   AddSegment(G, "BC", "B", "C")
   AddSegment(G, "BF", "B", "F")
   AddSegment(G, "BK", "B", "K")
   AddSegment(G, "BG", "B", "G")
   AddSegment(G, "CD", "C", "D")
   AddSegment(G, "CG", "C", "G")
   AddSegment(G, "DG", "D", "G")
   AddSegment(G, "DH", "D", "H")
   AddSegment(G, "DI", "D", "I")
   AddSegment(G, "EF", "E", "F")
   AddSegment(G, "FL", "F", "L")
   AddSegment(G, "GB", "G", "B")
   AddSegment(G, "GF", "G", "F")
   AddSegment(G, "GH", "G", "H")
   AddSegment(G, "ID", "I", "D")
   AddSegment(G, "IJ", "I", "J")
   AddSegment(G, "JI", "J", "I")
   AddSegment(G, "KA", "K", "A")
   AddSegment(G, "KL", "K", "L")
   AddSegment(G, "LK", "L", "K")
   AddSegment(G, "LF", "L", "F")
   return G




def CreateGraph_2():
   # Function to create the second graph with custom nodes and segments
   G = Graph()  # Initializes an empty graph object


   # Adding nodes to the graph. Each node is created with a name and (x, y) coordinates.
   AddNode(G, Node("M", 5, 25))  # Adds node "M" at (5, 25)
   AddNode(G, Node("N", 10, 22))  # Adds node "N" at (10, 22)
   AddNode(G, Node("O", 15, 25))  # Adds node "O" at (15, 25)
   AddNode(G, Node("P", 20, 20))  # Adds node "P" at (20, 20)
   AddNode(G, Node("Q", 6, 6))  # Adds node "Q" at (6, 6)
   AddNode(G, Node("R", 12, 8))  # Adds node "R" at (12, 8)
   AddNode(G, Node("S", 18, 10))  # Adds node "S" at (18, 10)
   AddNode(G, Node("T", 15, 3))  # Adds node "T" at (15, 3)


   # Adding segments to the graph. Each segment connects two nodes with a unique ID.
   AddSegment(G, "MN", "M", "N")  # Adds a segment between "M" and "N"
   AddSegment(G, "MO", "M", "O")  # Adds a segment between "M" and "O"
   AddSegment(G, "NP", "N", "P")  # Adds a segment between "N" and "P"
   AddSegment(G, "NO", "N", "O")  # Adds a segment between "N" and "O"
   AddSegment(G, "PR", "P", "R")  # Adds a segment between "P" and "R"
   AddSegment(G, "QS", "Q", "S")  # Adds a segment between "Q" and "S"
   AddSegment(G, "RT", "R", "T")  # Adds a segment between "R" and "T"
   AddSegment(G, "TS", "T", "S")  # Adds a segment between "T" and "S"
   AddSegment(G, "RQ", "R", "Q")  # Adds a segment between "R" and "Q"
   AddSegment(G, "SR", "S", "R")  # Adds a segment between "S" and "R"


   Plot(G)  # Plots the graph to visualize its nodes and segments




# Main program to test graphs
print("Probando el grafo...")  # Testing output for the graph


G1 = CreateGraph_1()  # Creates the first predefined graph
Plot(G1)  # Plots the first graph
PlotNode(G1, "C")  # Highlights node "C" and its neighbors
n = GetClosest(G1, 15, 5)  # Finds the closest node to coordinates (15, 5)
print(n.name)  # Expected output: "J", which is the closest node
n = GetClosest(G1, 8, 19)  # Finds the closest node to coordinates (8, 19)
print(n.name)  # Expected output: "B", which is the closest node


print("Probando el segundo grafo...")  # Testing the second graph
G2 = CreateGraph_2()  # Creates and plots the second custom graph


print("Testing LoadGraphFromFile...")  # Testing graph loading from a file
G = LoadGraphFromFile("graph_data.txt")  # Loads a graph from a file
Plot(G)  # Plots the graph loaded from the file

