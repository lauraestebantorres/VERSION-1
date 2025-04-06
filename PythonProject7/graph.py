from matplotlib import patches
from node import Node
from segment import Segment
import matplotlib.pyplot as plt
# Importing required libraries and classes.
# `matplotlib` is used for graphical plotting.
# `Node` and `Segment` classes are imported from their respective modules for graph representation.


class Graph:
   # This class represents a graph, consisting of nodes and segments connecting them.
   def __init__(self):
       # Initializes the graph with empty lists for nodes and segments.
       self.nodes = []
       self.segments = []

   def GetNodeByName(self, name):
       for node in self.nodes:
           if node.name == name:
               return node
       return None


def AddNode(g, n):
   # Adds a node 'n' to the graph 'g'.
   # If the node already exists in the graph, returns False. Otherwise, adds the node and returns True.
   if n in g.nodes:
       return False
   else:
       g.nodes.append(n)
       return True


def AddSegment(g, segment_id, name1, name2):
   # Adds a segment to the graph 'g' by connecting nodes with names 'name1' and 'name2'.
   # Also updates the neighbors list of the origin node.
   n1 = n2 = None
   for n in g.nodes:
       if n.name == name1:
           n1 = n  # Finds the origin node.
       if n.name == name2:
           n2 = n  # Finds the destination node.


   if n1 is None or n2 is None:
       # Returns False if either node is not found in the graph.
       return False
   else:
       s = Segment(n1, n2)  # Creates the segment using the origin and destination nodes.
       s.id = segment_id  # Assigns an ID to the segment.
       g.segments.append(s)  # Adds the segment to the graph.
       n1.neighbors.append(n2)  # Updates the neighbor list of the origin node.
       return True
def DeleteNode(g, name):
    node_to_remove = g.GetNodeByName(name)
    if node_to_remove is None:
        return False

    # Eliminar todos los segmentos conectados a este nodo
    g.segments = [s for s in g.segments if s.origin != node_to_remove and s.destination != node_to_remove]

    # Eliminar este nodo de la lista de vecinos de otros nodos
    for node in g.nodes:
        if node_to_remove in node.neighbors:
            node.neighbors.remove(node_to_remove)

    # Eliminar el nodo de la lista de nodos del grafo
    g.nodes.remove(node_to_remove)

    return True
def DeleteSegment(g, segment_id):
    for segment in g.segments:
        if segment.id == segment_id:
            segment.origin.neighbors.remove(segment.destination)
            g.segments.remove(segment)
            return True
    return False


def GetClosest(g, x, y):
   # Finds and returns the node closest to the given coordinates (x, y) in the graph 'g'.
   if not g.nodes:
       return None  # Returns None if the graph has no nodes.


   closest_node = None
   min_distance = float('inf')  # Initializes the minimum distance to infinity.


   for node in g.nodes:
       # Calculates the Euclidean distance between the given point and each node.
       distance = ((node.x - x) ** 2 + (node.y - y) ** 2) ** 0.5


       if distance < min_distance:
           min_distance = distance
           closest_node = node  # Updates the closest node if a shorter distance is found.


   return closest_node


def Plot(g):
   # Plots the entire graph, including nodes, segments, and costs of the segments.
   for segment in g.segments:
       # Draws each segment as a line connecting the origin and destination nodes.
       plt.plot([segment.origin.x, segment.destination.x],
                [segment.origin.y, segment.destination.y], 'blue')


       # Calculates the midpoint of the segment to display its cost.
       midpoint_x = segment.origin.x + (segment.destination.x - segment.origin.x) / 2
       midpoint_y = segment.origin.y + (segment.destination.y - segment.origin.y) / 2
       plt.text(midpoint_x, midpoint_y, round(segment.cost, 2))  # Displays the segment cost.


       # Adds an arrow to indicate the direction of the segment.
       plt.arrow(segment.origin.x, segment.origin.y,
                 segment.destination.x - segment.origin.x,
                 segment.destination.y - segment.origin.y,
                 head_width=0.5, head_length=0.5, fc='blue', ec='blue', length_includes_head=True)


   # Draws all the nodes in the graph.
   for node in g.nodes:
       plt.plot(node.x, node.y, marker='o', linestyle='', color='black', markersize=5)
       plt.text(node.x, node.y, node.name, horizontalalignment='left', verticalalignment='bottom', color='red',
                fontsize=7)


   # Adds labels, title, and grid to the plot.
   plt.xlabel('X')
   plt.ylabel('Y')
   plt.title("Graph with Direction Indicated at Segment End")
   plt.grid()
   plt.show()


def PlotNode(g, name):
   # Plots a single node and its neighbors.
   target_node = None
   for node in g.nodes:
       if node.name == name:
           target_node = node  # Finds the target node by name.
           break


   if target_node is None:
       # If the node doesn't exist, displays a message and returns.
       print(f"Node '{name}' does not exist in the graph.")
       return


   # Creates a new plot for the target node and its neighbors.
   plt.figure()
   for node in g.nodes:
       plt.plot(node.x, node.y, marker='o', linestyle='', color='black', markersize=5)
       plt.text(node.x, node.y, node.name, horizontalalignment='left', verticalalignment='bottom', color='red')


   for neighbor in target_node.neighbors:
       for segment in g.segments:
           if (segment.origin == target_node and segment.destination == neighbor) or \
                   (segment.origin == neighbor and segment.destination == target_node):
               # Draws the segment connecting the target node and its neighbor in blue.
               plt.plot([segment.origin.x, segment.destination.x],
                        [segment.origin.y, segment.destination.y], 'blue')
               plt.arrow(segment.origin.x, segment.origin.y,
                         segment.destination.x - segment.origin.x,
                         segment.destination.y - segment.origin.y,
                         head_width=0.5, head_length=0.5, fc='blue', ec='blue', length_includes_head=True)


               # Displays the segment cost at the midpoint.
               midpoint_x = (segment.origin.x + segment.destination.x) / 2
               midpoint_y = (segment.origin.y + segment.destination.y) / 2
               plt.text(midpoint_x, midpoint_y, round(segment.cost, 2))


   # Adds labels, title, and grid to the plot.
   plt.xlabel('X')
   plt.ylabel('Y')
   plt.title(f"Graph with nodes and segments for node '{name}'")
   plt.grid()
   plt.show()


def LoadGraphFromFile(file_path):
   # Loads a graph from a text file with nodes and segments data.
   g = Graph()
   try:
       with open(file_path, 'r') as file:
           mode = None  # Determines whether nodes or segments are being read.
           for line in file:
               line = line.strip()
               if not line:
                   continue
               if line.startswith("Nodes:"):
                   mode = "nodes"  # Indicates the nodes section is being processed.
                   continue
               elif line.startswith("Segments:"):
                   mode = "segments"  # Indicates the segments section is being processed.
                   continue


               if mode == "nodes":
                   # Processes a line in the nodes section.
                   name, x, y = line.split(',')
                   AddNode(g, Node(name, float(x), float(y)))
               elif mode == "segments":
                   # Processes a line in the segments section.
                   segment_id, origin_name, destination_name = line.split(',')
                   AddSegment(g, segment_id, origin_name, destination_name)
       return g
   except FileNotFoundError:
       # Handles the case where the file is not found.
       print(f"Error: File '{file_path}' not found.")
       return None
   except Exception as e:
       # Handles any other errors that occur during file processing.
       print(f"Error loading graph: {e}")
       return None


def DeleteSegment(g, segment_id):
    segment_to_delete = None
    for segment in g.segments:
        if segment.id == segment_id:
            segment_to_delete = segment
            break

    if segment_to_delete:
        g.segments.remove(segment_to_delete)
        # También quitamos al destino como vecino del origen si estaba
        if segment_to_delete.destination in segment_to_delete.origin.neighbors:
            segment_to_delete.origin.neighbors.remove(segment_to_delete.destination)
        return True
    return False
